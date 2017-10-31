# define.py

# This file

# [[ Describe the logic or idea of how this file works]]


import logging, os

def create_logger(selectedDBName):
    import os
    fileCheck = False
    for root, dirs, files in os.walk(os.getcwdu()):
        for file in files:
            if file.endswith(".log"):
                if file.__contains__(selectedDBName):
                    selectedDBName = file
                    fileCheck = True
                    break
        if fileCheck:
            break
    if not fileCheck:
        logFileFullPath = os.getcwdu() + "/wamdam_log_" + selectedDBName +".log"
        logfile = open(logFileFullPath, "w")
        content = "\nWaMDaM: The Water Management Data Model 1.0\nemail: amabdalah@aggiemail.usu.edu\n\n"
        logfile.write(content)
        logfile.flush()
        logfile.close()
    else:
        logFileFullPath = os.getcwdu() + "/" + selectedDBName

    logger0 = logging.getLogger(__name__)
    logger0.setLevel(logging.INFO)

    handler = logging.FileHandler(logFileFullPath)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger0.addHandler(handler)
    return logger0
logger = None
dbName = ""
version = 1.0
datasetName = ""