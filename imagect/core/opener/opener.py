
from zope.interface import implementer 
from collections import defaultdict
from imagect.api.opener import IOpener
import imagect.api.dataset as ds
import numpy as np
@implementer(IOpener)
class Opener(object) :

    pass

# add to menu
from imagect.api.actmgr import addActFun, renameAct
@addActFun("file.open.sample", "Sample", index =1, shortcut="F12")
def newimage() :
    sample = ds.DataSet.fromSample("chessboard").astype(np.float32)
    ds.get().add(sample)

    import imagect.api.viewmgr as vm

    sm = vm.get()
    if sm :
        sm.insertVolImagePlus(sample)



