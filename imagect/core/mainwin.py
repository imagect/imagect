
from imagect.api.mainwin import IMainWin
import imagect.api.actmgr
import imagect.core.actmgr
from imagect.api.actmgr import addAct, addActFun, addActWdg, renameAct
import imagect.api.ctapp as ctapp
from zope import interface
from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar, QLabel, QSpinBox
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

@addActFun("file.exit", text="&Exit", index=10)
def appexit():
    app = ctapp.get().exit()

@addActFun("file.exampe.msg", text="&Message", index=1)
def apptest():
    win = get()
    win.showMessage("Test Message")

@addActWdg("file.exampe.wdg", text="Show Widget", index = 3)
class ActWdg(QSpinBox) :
    def __init__(self, parent):
        super().__init__(parent)  

@addActFun("file.exampe.print", text="Print Actions", index = 4)
def appPrint():
    mngr = imagect.api.actmgr.get()
    acts = mngr.queryAll()
    for a in acts:
        print("id={}, title={}".format(a.id, a.title))

renameAct("file.exampe", "Examples", index =12)
