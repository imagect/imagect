
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
@addActFun("file.new.vol", "Image", index =1, shortcut="F12")
def newimage() :
    sample = ds.DataSet.fromSample().astype(np.float32)
    ds.get().add(sample)
