from .filter_plugin import FilterPlugIn, PlugInFlag
from threading import RLock
import threading
from imagect.api.actmgr import IAction, addAct
import imagect.api.viewmgr as vmm
import rx
import rx.operators as ops
from imagect.qtools import gui_scheduler, thread_pool_scheduler

runner_para = dict()
runner_para_lock = RLock()


def get_para_of(klass):
    para = None
    with runner_para_lock:
        if klass in runner_para:
            para = runner_para[klass]
    return para


class FilterPlugInRunner(object):

    def __init__(self, filter_plugin: FilterPlugIn):
        self.filter_plugin = filter_plugin
        self.arg = None
        self.imp = None

    def checkImagePlus(self, imp, flags):

        return True

    def setup(self):
        # self
        imp = vmm.get().currentImagePlus()

        # get filter capacity
        flags, arg = self.filter_plugin.setup(get_para_of(self.filter_plugin.__class__), imp)
        if flags & PlugInFlag.NOTHING:
            return False

        # check whether the PlugInFilter can handle this image type
        if not self.checkImagePlus(imp, flags):
            return False

        # image not required
        if flags & PlugInFlag.NO_IMAGE_REQUIRED:
            imp = None

        roi = None
        if imp is not None:
            roi = imp.getRoi()

        self.arg = arg
        self.imp = imp

        return True

    def run(self):
        self.filter_plugin.run(self.arg, self.imp)

    # 记录前正在运行的执行器
    runners = dict()
    runners_lock = RLock()

    @staticmethod
    def push(runner):
        with FilterPlugInRunner.runners_lock:
            i = id(runner)
            if i in FilterPlugInRunner.runners:
                return
            else:
                FilterPlugInRunner.runners[i] = runner

    @staticmethod
    def pop(runner):
        with FilterPlugInRunner.runners_lock:
            i = id(runner)
            FilterPlugInRunner.runners.pop(i)


def run_filter(klass):
    filter = klass()

    def print_thread_id(x):
        print("thread id = {}".format(threading.get_ident()))
        return x

    def run_filter_imp(fr):
        print("run filter in thread pool, thread id = {}, begin".format(threading.get_ident()))
        FilterPlugInRunner.push(fr)
        fr.run()
        FilterPlugInRunner.pop(fr)
        print("run filter in thread pool, thread id = {}, end".format(threading.get_ident()))


    def get_result(x):
        print("get result thread id = {}".format(threading.get_ident()))
        print("get result {}".format(x))

    print("gui thread id = {}".format(threading.get_ident()))
    rx.just(filter).pipe(
        ops.map(lambda f: FilterPlugInRunner(f)),
        ops.filter(lambda r: r.setup()),
        ops.subscribe_on(gui_scheduler),
        ops.observe_on(thread_pool_scheduler),
    ).pipe(
        ops.map(run_filter_imp),
    ).pipe(
        ops.observe_on(gui_scheduler)
    ).subscribe(on_next=lambda f: get_result(f), on_error=print)


def register_filter(klass):
    def cb():
        return run_filter(klass)

    index = 0
    if hasattr(klass, "index"):
        index = klass.index

    shortcut = None
    if hasattr(klass, "shortcut"):
        shortcut = klass.shortcut

    icon = ""
    if hasattr(klass, "icon"):
        icon = klass.icon

    act = IAction(
        icon=icon,
        id=klass.id,
        title=klass.title,
        index=index,
        shortcut=shortcut
    )

    act.callable = cb
    addAct(act)
    return klass
