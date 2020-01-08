from .image_stack import ImageStack, DataMeta
from .image_plus import ImagePlus
from rx.subject import Subject
import imagect
import imagect.api.viewmgr as vmm
import imagect.api.mainwin as mainwin

qAppInited = Subject()
qAppStopped = Subject()

mainWinShowed = Subject()
mainWinHide = Subject()

imagePlusAdd = Subject()


def addImagePlus(imp) :
    imagePlusAdd.on_next(imp)
    

def getCurrentImagePlus():
    """
    get current image plus
    """
    return vmm.get().currentImagePlus()





def setProgress(progress):
    """

    """
    mainwin.get().showMessage("Progress {}%".format(progress))
