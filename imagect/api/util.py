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


def showSlice( i = -1) : 
    from matplotlib import pyplot as plt

    if i == -1 :
        stack = viewmgr.currentStack()
        if stack is not None:
            plt.imshow(stack)
    else :
        ds = viewmgr.currentDataSet()
        if ds is not None:        
            plt.imshow(ds.getStack(i))

