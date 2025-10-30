# DeepLearning-Chicken_Disease_ClassificationWorkflows

Update config.yaml
Update secrets.yaml [Optional]
Update params.yaml
Update the entity
Update the configuration manager in src config
Update the components
Update the pipeline
Update the main.py
Update the dvc.yaml

1] First we create a custom logging function in the src/__init__.py. Then we tried to execute and check this log functionality in the main.py

#from cnnclassifier import logger
#logger.info("Welcome to my custom Log")

2] For exception we didnot create custom Exception, we use BoxValueError for exception handling. Also we have all the genric functions in utils/common.py file

3] Next check the Pipeline above

4] Now Data Ingestion part. check config/config.yaml

5] Now to data ingestion part. First check research/01_data_ingestion.ipynb.
Update config/config.yaml.
To read the .yaml file => Update constants/__init__.py
For time being, in params.yaml => add this line, key : val

Convert the data ingestion part to Modular 
Create config_entity.py in the entity folder
Now update configuration.py in the src/config

Create data_ingestion.py in th components folder

Create stage_01_data_ingestion.py in the pipeline folder
    This will run this data_ingestion stage one by one.
        1. config/Confiugration
        2. Components
        
    The above is the pipeline, call that in the main.py


6] Now Prepare base Model. This is a classification based problem. use transfer learning approach.
    VG16

[Data valdation part] -is not required, because we have the data in the correct folder.

Update the config.yaml file
Then update the entity, config.entity
Now update the configuration.py
updata components.prepare_base_model.py
Create pipeling

7] Prepare callbacks. This is expecially for Classification based model. Some metedatas will be saved here also.
    Update the config.yaml
    Update the entity, config.entity
    Now update the configuration.py
    updata components - prepare_callbacks.py
    Create pipeline - For Preprare callbacks no Pipeline is required [BECAUSE THIS WILL HELP TO DO THE TRAINING]
    MAIN - No Main, just start do the training

8] Model Training
    Update the config.yaml
    Prepare the entity.
    Now configuration.py
    update components - training.py
    create pipeline - stage_03_training.py
    Main - 
Important :
    To see the tensorboard - 
        tensorboard --logdir artifacts/prepare_callbacks/tensorboard_log_dir
    Then ctrl + right click and open the local host site
    We can view the graphs, if we give more than 1 epoch.

9] DVC yaml
    dvc init
        This creates dvcignore file and dvc folder
    dvc repro
        To execute, the application

    Advantage is, it skips the part which is already executed.
    This does not builds from the scartch

    After compilation, this will generate a dvc.lock file -> This saves all the metadatas

10] Prediction











