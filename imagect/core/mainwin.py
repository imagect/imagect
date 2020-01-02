import imagect.api.mainwin
import imagect
import os.path
from imagect.api.mainwin import IMainWin
import imagect.api.actmgr
from imagect.api.actmgr import addAct, addActFun, addActWdg, renameAct, IAction, register_action
import imagect.api.app as app
from zope import interface
from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar, QLabel, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# qtconsole
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager


def make_jupyter_widget_with_kernel():
    """
    Start a kernel, connect to it, and create a RichJupyterWidget to use it
    """
    kernel_manager = QtInProcessKernelManager(kernel_name='python3')
    kernel_manager.start_kernel(show_banner=True)
    kernel = kernel_manager.kernel
    kernel.io_loop = app.get().asyncio_loop()

    kernel_client = kernel_manager.client()
    kernel_client.start_channels()

    jupyter_widget = RichJupyterWidget(gui_completion="droplist")
    jupyter_widget.kernel_manager = kernel_manager
    jupyter_widget.kernel_client = kernel_client
    return jupyter_widget


@interface.implementer(IMainWin)
class MainWin(QMainWindow):
    """
    implements IMainWin
    """

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self._jupyter_widget = make_jupyter_widget_with_kernel()
        self.setCentralWidget(self._jupyter_widget)
        app.get().qt_app().aboutToQuit.connect(self.shutdown_kernel)

        self.statusBar()

        self.toolBarFile = QToolBar(self)

        # def resizeHeight(wdg, height) :
        #     size = wdg.size()
        #     size.setHeight(height)
        #     wdg.resize(size) 

        # def showjw() :
        #     if not self._jupyter_widget.isVisible() or self._jupyter_widget.isMinimized() :
        #         self.showNormal()
        #         self._jupyter_widget.raise_()
        #     else:
        #         self._jupyter_widget.hide()

        ctb = self.toolBarFile.addAction("Console")
        ctb.setIcon(imagect.icon("console.png"))
        self.addToolBar(self.toolBarFile)

        self.resize(600, 600)

    def window(self):
        return self

    def menuBar(self):
        return super().menuBar()

    def console(self):
        return self._jupyter_widget

    def showMessage(self, msg):
        self.statusBar().showMessage(msg)

    def shutdown_kernel(self):
        self._jupyter_widget.kernel_client.stop_channels()
        self._jupyter_widget.kernel_manager.shutdown_kernel()


from zope.component import getUtility


def get():
    return getUtility(IMainWin)


@addActFun("file.example.msg", text="&Message", index=1)
def apptest():
    win = get()
    win.showMessage("Test Message")


@addActWdg("file.example.wdg", text="Show Widget", index=3)
class ActWdg(QSpinBox):
    def __init__(self, parent):
        super().__init__(parent)


@addActFun("file.example.print", text="Print Actions", index=4)
def appPrint():
    mngr = imagect.api.actmgr.get()
    acts = mngr.queryAll()
    for a in acts:
        print("id={}, title={}".format(a.id, a.title))


renameAct("file.example", "Examples", index=12)


@addActFun("file.exit", text="&Exit", index=10)
def appexit():
    app.getQtApp().exit()
