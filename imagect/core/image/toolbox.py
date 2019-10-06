import imagect.api.viewmgr as vmm
from imagect.api.actmgr import addActFun, renameAct
from skimage import filters

@addActFun("image.Smooth", "Smooth", index =1, shortcut="Shift+Ctrl+S")
def smooth() :
    vm = vmm.get()
    stack = vm.currentStack()
    d = filters.gaussian(stack, 1)
    v = vm.currentView()
    v.setImageData(d)



