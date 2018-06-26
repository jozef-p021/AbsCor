# -*- coding: utf-8 -*-
from __future__ import print_function

SIMULATION_SCRIPT_PATH = u"./bmg_raytrace.py"

JOB_LOCAL = 0
JOB_REMOTE = 1

PARAM_DET_X = u"DetX"
PARAM_DET_Y = u"DetY"
PARAM_DET_OFFSET_X = u"DetOffsetX"
PARAM_DET_OFFSET_Y = u"DetOffsetY"
PARAM_SAM_LENGHT = u"SamLength"
PARAM_SAM_RADIUS = u"SamRadius"
PARAM_SAM_ABSORPTION_LENGTH = u"SamAbsLength"
PARAM_SIM_SDD = u"SDD"
PARAM_SIM_PHOTONS = u"Photons"
PARAM_SIM_MAX_RUNNING_TIME = u"MaxRunTime"
PARAM_SIM_NODES = u"Nodes"
PARAM_SIM_PROCESSES = u"Processes"
PARAM_JOB_TYPE = u"JobTime"
PARAM_JOB_COMMAND = u"JobCommand"
PARAM_REMOTE_JOB_CONFIG = u"RemoteJobConfig"
PARAM_REMOTE_REPO_DIR = u"RemoteRepoDir"

PRESET_DETECTOR = u"detector"
PRESET_SAMPLE = u"sample"
PRESET_SIMULATION = u"simulation"

STATUS_INIT = "I"
STATUS_WAITING = "W"
STATUS_RUNNING = "R"
STATUS_FINISHED = "F"
STATUS_ERROR = "E"
STATUS_CANCELLED = "C"