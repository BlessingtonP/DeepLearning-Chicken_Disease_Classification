from cnnclassifier.entity.config_entity import TrainingConfig
import tensorflow as tf
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
    
    #Loads the entire model exactly as it was saved — architecture, weights, optimizer state, loss, and metrics.    
    #Runs the compile step automatically using whatever configuration was stored in the file.
    #VERY IMPORTANT -> DONT USE THE BELOW get_base_model() =>It loads and compiles automatically


    # def get_base_model(self):
    #     self.model = tf.keras.models.load_model(
    #         self.config.updated_base_model_path
    #     )


    #Loads only the model architecture and weights — skips reloading the old compile configuration (compile=False).
    #VERY IMPORTANT -> Below we load the model and then we compile it manually [With your chosen optimizer, loss, and metrics.]

    def get_base_model(self):


        # Load WITHOUT running the saved compile step
        self.model = tf.keras.models.load_model(self.config.updated_base_model_path, compile=False)

        # Now it's safe to inspect the loaded model (this runs when the method is called)
        try:
            print("Loaded model summary:")
            self.model.summary()
        except Exception as ex:
            print("Could not print summary:", ex)

        # Print raw loss/metrics info (may be a string or callable)
        try:
            print("Model.loss (raw):", self.model.loss)
        except Exception as ex:
            print("Could not read model.loss:", ex)

        try:
            print("Model.metrics (raw):", self.model.metrics)
        except Exception as ex:
            print("Could not read model.metrics:", ex)

        # Decide loss by checking your label format:
        # Your debug earlier showed y_batch shape (16, 2) -> one-hot -> categorical_crossentropy
        chosen_loss = "categorical_crossentropy"

        # Recompile with explicit, safe choices. Use configured learning rate if available
        lr = getattr(self.config, "params_learning_rate", 1e-4)
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
            loss=chosen_loss,
            metrics=["accuracy"]
        )
        print("Model recompiled successfully with loss=", chosen_loss, "and lr=", lr)

    
    def train_valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.20
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

        if self.config.params_is_augmentation:
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                **datagenerator_kwargs
            )
        else:
            train_datagenerator = valid_datagenerator

        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="training",
            shuffle=True,
            **dataflow_kwargs
        )

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)
        #Can use the Below API Also.
        # tf.keras.models.save_model(model, "my_model.keras")



    def train(self, callback_list: list):
        self.steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

        # debug sample
        x_batch, y_batch = next(self.train_generator)
        print("DEBUG: train batch types ->", type(x_batch), type(y_batch))
        print(" - x_batch is numpy array?", isinstance(x_batch, np.ndarray))
        print(" - y_batch is numpy array?", isinstance(y_batch, np.ndarray))
        print(" - x_batch dtype/shape:", getattr(x_batch, "dtype", None), getattr(x_batch, "shape", None))
        print(" - y_batch dtype/shape:", getattr(y_batch, "dtype", None), getattr(y_batch, "shape", None))
        # restore generator state if needed (ImageDataGenerator returns generator that supports next)

        self.model.fit(
            self.train_generator,
            epochs=self.config.params_epochs,
            steps_per_epoch=self.steps_per_epoch,
            validation_steps=self.validation_steps,
            validation_data=self.valid_generator,
           callbacks=callback_list
        )

        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )
