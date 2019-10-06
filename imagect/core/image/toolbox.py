import imagect.api.viewmgr as vmm
from imagect.api.actmgr import addActFun, renameAct
import imagect.api.app as app 
import imagect.api.mainwin as mainwin
from skimage import filters
import rx
from rx import operators as ops
from rx.subject import Subject
import time
import imagect.api.image as image

@image.proc("image.Smooth", "Smooth", index =1, shortcut="Shift+Ctrl+S")
def smooth(data) :
    to = 10
    t = 0        
    while t < to :
        image.log( "progress={}%".format( t*100.0 / to))
        time.sleep(1)
        t += 1
    return filters.gaussian(data, 1)


