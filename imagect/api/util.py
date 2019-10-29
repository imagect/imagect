import imagect.api.actmgr 
import imagect.api.app 
import imagect.api.mainwin 
import imagect.api.console
import imagect.api.dataset
import imagect.api.viewmgr


app = imagect.api.app.get()
mainwin = imagect.api.mainwin.get()
actmgr = imagect.api.actmgr.get()
recent = imagect.api.recent.get()
console = imagect.api.console.get()
datamgr = imagect.api.dataset.get()
viewmgr = imagect.api.viewmgr.get()


def showSlice() : 
    from matplotlib import pyplot as plt
    stack = viewmgr.currentStack()
    if stack is not None:
        plt.imshow(stack)

def showSliceAt(i) :
    from matplotlib import pyplot as plt
    ds = viewmgr.currentDataSet()
    if ds is not None:        
        plt.imshow(ds.getStack(i))
