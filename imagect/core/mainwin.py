
from imagect.api.mainwin import IMainWin
import imagect.api.actmgr
import imagect.core.actmgr
from imagect.api.actmgr import addAct, addFun
import imagect.api.ctapp as ctapp
from zope import interface
from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


@interface.implementer(IMainWin)
class MainWin(QMainWindow) :

    """
    implements IMainWin
    """

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.resize(500, 60)
        self.statusBar()
        self.toolBarFile = QToolBar(self)
        self.addToolBar(self.toolBarFile)

    def window(self):
        return self

    def menuBar(self):
        return super().menuBar()

    def showMessage(self, msg) :
        self.statusBar().showMessage(msg)


from zope.component import getUtility
def get() :
    return getUtility(IMainWin)

@addFun("file.exit", text="&Exit")
def appexit():
    app = ctapp.get().exit()


@addFun("file.test", text="&Test")
def apptest():
    win = get()
    win.showMessage("Test Message")

@addFun("file.test.fun1", text="&Test")
def apptest():
    win = get()
    win.showMessage("Test Message")

@addFun("file.test.fun2", text="&Test")
def apptest():
    win = get()
    win.showMessage("Test Message")

@addFun("file.test.fun3", text="&Test")
def apptest():
    win = get()
    win.showMessage("Test Message")


class ExitAction(QAction):
    def __init__(self, parent=None):
        super().__init__(QIcon(), "&Exit", parent=parent)
        app = ctapp.get()
        self.triggered.connect(app.exit)

class TestMsgAction(QAction):
    def __init__(self,  parent=None):
        super().__init__(QIcon(), "Test", parent=parent)

        def show() :
            win = get()
            win.showMessage("Test Message")
        self.triggered.connect(show)