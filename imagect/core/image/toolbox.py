from skimage import filters
from skimage import restoration
from skimage.morphology import disk

import time
import imagect.api.image as image
from traits.api import *


def demoTimeOut():
    to = 10
    t = 0
    while t < to:
        image.log("progress={}%".format(t * 100.0 / to))
        time.sleep(1)
        t += 1


class SmoothPara(HasTraits):
    width = Int(1)


@image.proc_interactive("image.Smooth", "Smooth", index=1, ParaKlass=SmoothPara, shortcut="F6")
def smooth(data, p):
    # demoTimeOut()
    return filters.gaussian(data, p.width)


@image.proc_with_para("image.Median", "median", index=1)
def median(data):
    return filters.median(data, disk(1))


class RestorationPara(HasTraits):
    weight = Float(0.1)


@image.proc_interactive("image.Restoration", "Restoration", ParaKlass=RestorationPara, index=1)
def denoise_tv_chambolle(data, p):
    return restoration.denoise_tv_chambolle(data, weight=p.weight)
