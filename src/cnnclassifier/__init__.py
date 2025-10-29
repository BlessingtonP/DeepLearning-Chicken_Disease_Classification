#I am writing the custom log file here for a simplicity - If not i need to call (cnnclassifier.src.logger.logging)

#For this i can call (cnnclassifier.logger)

#After writing this log function - Then go to main.py file

import os
import sys
import logging

logging_str = '[%(asctime)s : %(levelname)s : %(module)s : %(message)s]'

log_dir = 'logs'
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)  #This prints the log in the terminal also
    ]
)

logger = logging.getLogger('cnnclassifierLogger')