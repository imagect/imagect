import os 
import os.path 
import sys

RUN_THREAD=True

SAMPLE_DATA_FOLDER = ""
if "IMAGECT_SAMPLE_DATA_FOLDER" in os.environ:
    SAMPLE_DATA_FOLDER = os.environ["IMAGECT_SAMPLE_DATA_FOLDER"]
SAMPLE_DATA_RAWDATA = os.path.join(SAMPLE_DATA_FOLDER, "lizong_640_640_800_uint16_0Head.raw.raw")
