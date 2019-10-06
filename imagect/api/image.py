
import imagect.api.viewmgr as vmm
import imagect.api.actmgr as actmgr
import imagect.api.app as app 
import imagect.api.mainwin as mainwin
from rx.scheduler.mainloop import QtScheduler
from rx import operators as ops
import rx
import time

def doImageProc(proc, para) :
    def fun() :

        ret = False

        # 如果有参数模板
        if para :
            p = para()
            ret = p.configure_traits(kind="modal")
            
            # 给定参数模板，但被用户放弃
            if not ret :
                return
            
        vm = vmm.get()
        stack = vm.currentStack()
        
        mainwin.get().showMessage("Running")

        def comp(f) :
            if not para :
                return proc(f)
            else:
                return proc(f,p)
        
        def on_next(d) :    
            v = vm.currentView()
            v.setImageData(d)
            mainwin.get().showMessage("Complete")

        rx.just(stack).pipe(
            ops.observe_on(app.get().rx_threadpool()),
            ops.map(comp)         
        ).subscribe(
            on_next, 
            on_error=print, 
        )
    return fun

def proc(id : str, text: str, index=0, shortcut=None):
    def add(callable):
        a = actmgr.createAction(id, title=text, callable=doImageProc(callable), index=index, shortcut=shortcut)
        actmgr.addAct(a)
    return add

def proc_with_para(id : str, text: str, index=0, para=None, shortcut=None):
    def add(callable):
        a = actmgr.createAction(id, title=text, callable=doImageProc(callable, para), index=index, shortcut=shortcut)
        actmgr.addAct(a)
    return add

def log(msg) :
    rx.just( msg ).subscribe(
        on_next   = mainwin.get().showMessage,
        on_error  = print,
    )