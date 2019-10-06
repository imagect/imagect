from skimage import filters
from skimage import restoration
from skimage.morphology import disk

import time
import imagect.api.image as image
from traits.api import *

def demoTimeOut() :
    to = 10
    t = 0        
    while t < to :
        image.log( "progress={}%".format( t*100.0 / to))
        time.sleep(1)
        t += 1

class SmoothPara(HasTraits):
    width = Int(1)

@image.proc_with_para("image.Smooth", "Smooth", index =1, para=SmoothPara, shortcut="Shift+Ctrl+S")
def smooth(data, p) :
    return filters.gaussian(data, p.width)


@image.proc_with_para("image.Median", "median", index =1)
def smooth(data) :
    return filters.median(data, disk(1))   

class RestorationPara(HasTraits):
    weight = Float(0.1)

@image.proc_with_para("image.Restoration", "Restoration", para=RestorationPara, index =1)
def smooth(data, p) :
    return restoration.denoise_tv_chambolle(data, weight=p.weight)   

 