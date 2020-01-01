from rx.subject import Subject
import qtpy
import imagect.qtools as qtools

qAppInited = Subject()
qAppStopped = Subject()

mainWinShowed = Subject()
mainWinHide = Subject()

gui_scheduler = qtools.QtUiScheduler(qtpy.QtCore, qtools.qtApp)
