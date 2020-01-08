from enum import Flag, auto


class PlugInFlag(Flag):
    NOTHING = auto()
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


class FilterPlugIn(object):

    def setup(self, arg, imp):
        """
        算法参数配置，交互操作，该函数在界面线程执行
        显示对话框，其中设定所需参数，
        :param arg:
        :param imp:
        :return: (算法的处理能力，算法的输入参数）
        """
        return PlugInFlag.NOTHING, None

    def run(self, arg, imp):
        """
        算法执行，该函数在后台线程执行
        :param arg:
        :param imp:
        :return:
        """
        pass


class SliceFilterPlugin(FilterPlugIn):

    def run(self, arg, imp):
        if hasattr(arg, "allLayer") and arg.allLayer:
            for l in range(imp.data.layer):
                s = imp.getSlice(l)
                ret, s = self.process_slice(s, arg, imp)
                if ret:
                    imp.updateSlice(l, s)
        else:
            s = imp.getCurrentSlice().copy()
            ret, s = self.process_slice(s, arg, imp)
            if ret:
                imp.updateCurrentSlice(s)

    def process_slice(self, slice, arg, imp):
        return True, slice


class StackFilterPlugin(FilterPlugIn):

    def run(self, arg, imp):
            s = imp.getStack().data.copy() #numpy ndarray
            ret, s = self.process_stack(s, arg, imp)
            if ret:
                imp.updateStack(s)

    def process_stack(self, stack, arg, imp):
        return True, stack


if __name__ == "__main__":
    print(PlugInFlag(2))
