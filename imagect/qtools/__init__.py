from .app import qtApp
from .event import CallbackEvent
from .event import EventSpy
from qtpy.QtCore import QEvent
import qtpy.QtCore
from rx.scheduler.threadpoolscheduler import ThreadPoolScheduler

from .rxtool import QtUiScheduler
QEvent.registerEventType(CallbackEvent.typeid)

gui_scheduler = QtUiScheduler(qtpy.QtCore, qtApp)

thread_pool_scheduler = ThreadPoolScheduler()

