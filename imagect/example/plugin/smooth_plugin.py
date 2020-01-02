from imagect.plugin.plugin import PlugIn, PlugInFlag
from imagect.plugin.plugin_runner import register_filter
from imagect.api.actmgr import renameAct
from traits.api import HasTraits, Int, Bool
import time
import threading
import imagect.ic as ic
import imagect

from skimage import filters


class SmoothPara(HasTraits):
    width = Int(10)
    sleep = Bool(True)


def demoTimeOut():
    to = 10
    t = 0
    while t < to:
        ic.setProgress(t * 100.0 / to)
        time.sleep(1)
        t += 1

@register_filter
class SmoothPlugin(PlugIn):
    id = "help.demo.smooth"
    title = "Smooth"
    index = 0
    icon = imagect.icon("console.png")
    shortcut = "Ctrl+N"

    def __init__(self):
        super().__init__()

    def setup(self, arg, imp):
        para = arg
        if arg is None:
            para = SmoothPara()
        ret = para.configure_traits(kind="modal")
        if not ret or not imp:
            return PlugInFlag.NOTHING, None

        print("Smooth setup: thread id = {}".format(threading.get_ident()))
        return PlugInFlag.DOES_32, para

    def run(self, arg, imp):
        if arg.sleep:
            print("sleeping {}s".format(10))
            demoTimeOut()

        s = imp.getCurrentSlice().copy()
        s = filters.gaussian(s, arg.width)
        imp.updateCurrentSlice(s)
        print("Smooth run: thread id = {}".format(threading.get_ident()))
        pass


renameAct("help.example.plugin", "Plugin")
