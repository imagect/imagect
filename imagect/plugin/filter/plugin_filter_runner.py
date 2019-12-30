from .plugin_filter import PlugInFilter, FilterFlag

from imagect import WindowManager


class PlugInFilterRunner(object):

    def __init__(self, theFilter: PlugInFilter, command, arg):
        # self
        imp = WindowManager.getCurrentImage()

        # get filter capacity
        flags = theFilter.setup(arg, imp)

        # check whether the PlugInFilter can handle this image type
        if not self.checkImagePlus(imp, flags, command):
            return

        # image not required
        if flags & FilterFlag.NO_IMAGE_REQUIRED :
            imp = None

        roi = None
        if imp is None:
            roi = imp.getRoi()

    def checkImagePlug(self, imp, flags, command):

        return True
