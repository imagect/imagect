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
        # print("stack.hpe={}".format(stack.shape))
        # s = stack.shape
        # if s[2] ==1 :
            # stack = stack.reshape((s[0], s[1]))
        plt.imshow(stack)