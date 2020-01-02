import imagect.api.viewmgr as vmm
import imagect.api.actmgr as actmgr
import imagect.api.app as app
import imagect.api.mainwin as mainwin
import imagect.config as config
# from rx.scheduler.mainloop import QtScheduler
from rx import operators as ops
import concurrent.futures
import asyncio

import rx
import time

from traits.api import *
from traitsui.api import *


def doImageProc(proc, ParaKlass):
    def fun():

        ret = False

        # 如果有参数模板
        if ParaKlass:
            p = ParaKlass()
            # todo width and height
            ret = p.configure_traits(kind="modal")

            # 给定参数模板，但被用户放弃
            if not ret:
                return

        vm = vmm.get()
        v = vm.currentView()
        ip = vm.currentImagePlus()
        index = ip.getCurrentSliceIndex()
        sslice = ip.getCurrentSlice().copy()

        mainwin.get().showMessage("Running")

        def comp():
            if not ParaKlass:
                d = proc(sslice)
            else:
                d = proc(sslice, p)

            # update ui
            def cb():
                ip.updateCurrentSlice(d)
                mainwin.get().showMessage("Complete")

            app.get().asyncio_loop().call_soon_threadsafe(cb)

        if config.RUN_THREAD:
            app.get().asyncio_loop().run_in_executor(
                app.get().threadpool(), comp
            )
        else:
            comp()

    return fun


def doImageProcInt(proc, ParaKlass):
    def fun():

        vm = vmm.get()
        v = vm.currentView()
        ip = vm.currentImagePlus()
        index = ip.getCurrentSliceIndex()
        sslice = ip.getCurrentSlice().copy()

        def proc_data(p):
            def comp():
                d = proc(sslice, p)

                def cb():
                    ip.updateSlice(index, d)
                    mainwin.get().showMessage("Complete")

                app.get().asyncio_loop().call_soon_threadsafe(cb)

            if config.RUN_THREAD:
                app.get().asyncio_loop().run_in_executor(
                    app.get().threadpool(), comp
                )
            else:
                comp()

        class IntHandler(Controller):

            _changed = False

            def setattr(self, info, object, name, value):
                Handler.setattr(self, info, object, name, value)
                self.apply(object)

            def object__updated_changed(self, info):
                if info.initialized:
                    info.ui.title += "*"
                    self.apply(info.object)

            def apply(self, o):
                # self._changed = True
                proc_data(o)

            def closed(self, info, is_ok):
                if is_ok:
                    proc_data(info.object)
                else:
                    if self._changed:
                        ip.updateSlice(index, sslice)

        mainwin.get().showMessage("Running")
        intpara = ParaKlass()
        intpara.configure_traits(
            handler=IntHandler
        )

    return fun


def proc_interactive(id: str, text: str, index=0, ParaKlass=None, shortcut=None):
    def add(callable):
        a = actmgr.createAction(id, title=text, callable=doImageProcInt(callable, ParaKlass), index=index,
                                shortcut=shortcut)
        actmgr.addAct(a)

    return add


def proc_with_para(id: str, text: str, index=0, ParaKlass=None, shortcut=None):
    def add(callable):
        a = actmgr.createAction(id, title=text, callable=doImageProc(callable, ParaKlass), index=index,
                                shortcut=shortcut)
        actmgr.addAct(a)

    return add


def log(msg):
    app.get().asyncio_loop().call_soon_threadsafe(mainwin.get().showMessage, msg)
    # rx.just(msg).subscribe(
    #     on_next=mainwin.get().showMessage,
    #     on_error=print,
    # )
