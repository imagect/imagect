import imagect.api.viewmgr as vmm
import imagect.api.actmgr as actmgr
import imagect.api.app as app
import imagect.api.mainwin as mainwin
import imagect.config as config
from rx.scheduler.mainloop import QtScheduler
from rx import operators as ops

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
            ret = p.configure_traits(kind="modal")

            # 给定参数模板，但被用户放弃
            if not ret:
                return

        vm = vmm.get()
        v = vm.currentView()
        dataset = vm.currentDataSet()
        stack = vm.currentStack().copy()

        mainwin.get().showMessage("Running")

        def comp(f):
            if not ParaKlass:
                return proc(f)
            else:
                return proc(f, p)

        def on_next(d):
            dataset.updateCurrentStack(d)
            mainwin.get().showMessage("Complete")

        if config.RUN_THREAD:
            rx.just(stack).pipe(
                ops.observe_on(app.get().rx_threadpool()),
                ops.map(comp),
                ops.observe_on(app.get().rx_scheduler()),
            ).subscribe(
                on_next,
                on_error=print,
            )
        else:
            rx.just(stack).pipe(
                ops.map(comp),
            ).subscribe(
                on_next,
                on_error=print,
            )

    return fun


def doImageProcInt(proc, ParaKlass):
    def fun():

        vm = vmm.get()
        v = vm.currentView()
        dataset = vm.currentDataSet()
        index = dataset.currentStackIndex
        stack = vm.currentStack().copy()

        def proc_data(p):
            def comp(f):
                return proc(f, p)

            def on_next(d):
                dataset.updateStack(index, d)
                mainwin.get().showMessage("Complete")

            if config.RUN_THREAD:
                rx.just(stack).pipe(
                    ops.observe_on(app.get().rx_threadpool()),
                    ops.map(comp),
                    # ops.observe_on(app.get().rx_scheduler()),
                    # ops.subscribe_on(app.get().rx_scheduler()),
                ).subscribe(
                    on_next,
                    on_error=print,
                )
            else:
                rx.just(stack).pipe(
                    ops.map(comp),
                ).subscribe(
                    on_next,
                    on_error=print,
                )

        class IntHandler(Controller):

            _changed = False

            def setattr(self, info, object, name, value):
                Handler.setattr(self, info, object, name, value)
                self.apply(object)

            def object__updated_changed(self, info):
                if info.initialized:
                    info.ui.title += "*"

            def apply(self, o):
                self._changed = True
                proc_data(o)

            def closed(self, info, is_ok):
                if is_ok:
                    proc_data(info.object)
                else:
                    if self._changed:
                        dataset.updateStack(index, stack)

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
    rx.just(msg).subscribe(
        on_next=mainwin.get().showMessage,
        on_error=print,
    )
