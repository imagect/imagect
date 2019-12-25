from enum import Flag, auto

class FilterFlag(Flag) :

    DOES_8G = auto()
    DOES_8C = auto()
    DOES_16 = auto()
    DOES_32 = auto()
    DOES_RGB = auto()
    DOES_ALL = DOES_8G | DOES_8C | DOES_16 | DOES_32 | DOES_RGB
    DOES_STACKS = auto()
    SUPPORTS_MASKING = auto()
    NO_CHANGES = auto()
    NO_UNDO = auto() 
    NO_IMAGE_REQUIRED = auto() 
    ROI_REQUIRED = auto()
    STACK_REQUIRED = auto()
    DONE = auto()
    CONVERT_TO_FLOAT = auto()
    SNAPSHOT = auto()
    PARALLELIZE_STACKS = auto()
    FINAL_PROCESSING = auto()
    KEEP_THRESHOLD = auto()
    PARALLELIZE_IMAGES = auto()
    NO_UNDO_RESET = auto()


class PlugInFilter(object) :

    pass

if __name__ == "__main__":
    print(FilterFlag(2))