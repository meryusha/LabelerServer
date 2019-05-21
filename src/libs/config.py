import os
from datetime import datetime
from yacs.config import CfgNode as CN

global CFG

CFG = CN()

# General Parameters
CFG.GPU = -1

# Logging parameters
CFG.logging = CN()
CFG.logging.loglevel = "INFO"
CFG.logging.loggingPath = "log"
