from imagect.api.opener import IReader
from zope.interface import implementer
from typing import List
from traits.api import *
from traitsui.api import *
import numpy as np
from imagect.api.dataset import DataSet, DataMeta

class RawVolMeta(HasTraits):

    path = File("E:/CloudData/lizong_640_640_800_uint16_0Head.raw.raw")
    width = Int(640)
    height = Int(640)
    stack = Int(800)
    dtype = Enum(np.uint16, np.int16, np.uint32, np.int32)

    trait_view = View(
        Item(name="path", editor=FileEditor(dialog_style = "open")),
        Item(name="stack"),
        Item(name="height"),
        Item(name="width"),
        Item(name="dtype"),
        buttons=[OKButton, CancelButton],
        dock="vertical",
        title="Raw Data Property"
    )

@implementer(IReader)
class VolReader(HasTraits):

    path = File(exists = True)
    _id = Str()
    _suffix = ListStr()
    _category = Str()
    _name = Str()

    def __init__(self):
        self._id = "reader.vol.3d"
        self._suffix = ["raw"]

    def id(self) -> str:
        return self._id

    def suffix(self):
        return self._suffix

    def name(self) -> str:
        return self._name.str()

    def category(self) -> str:
        return self._category

    def read(self, path):
        pro = RawVolMeta()
        pro.path = path
        return VolReader.readFrom(pro)

    @staticmethod
    def readFrom(pro = None):
        if pro is None :
            pro = RawVolMeta()
        pro.configure_traits(kind="modal")
        pro.print_traits()
        if pro.path != "":
            data = np.memmap(pro.path,
                             dtype=pro.dtype,
                             mode="r",
                             shape=(
                                 pro.stack,
                                 pro.height,
                                 pro.width)
                             )
            s, w, h = data.shape
            data = data.reshape((s,w,h,1))
            ds = DataSet()
            ds.data = data
            ds.meta.path = pro.path
            ds.meta.reader = VolReader.__class__ #.name
            ds.meta.category = "vol"
            return ds
        return None

# add to menu

import imagect.api.dataset as ds
from imagect.api.actmgr import addActFun, renameAct
@addActFun("file.open.vol", "Raw Image", index =1, shortcut="F11")
def newimage() :
    sample = VolReader.readFrom(None)
    if sample is None :
        return

    ds.get().add(sample)

    import imagect.api.viewmgr as vm

    sm = vm.get()
    if sm :
        sm.createSession(sample)
renameAct("file.open", "Open")

if __name__ == "__main__":
    # VolReader.read()
    vr = VolReader()
    vr.read("")
