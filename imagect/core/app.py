
from imagect.api.app import IApp
import imagect.api.app as app
from zope import interface 
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QStandardPaths
from asyncqt import QEventLoop, QThreadExecutor
import asyncio
import concurrent
# from rx.scheduler.mainloop import QtScheduler
# from rx.scheduler import ThreadPoolScheduler

@interface.implementer(IApp)
class App(QApplication):

    """
    application
    """

    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("imagect")

        self.loop = QEventLoop(self)
        asyncio.set_event_loop(self.loop)

        self.thread_pool = concurrent.futures.ThreadPoolExecutor()

    def asyncio_loop(self):
        return self.loop

    def threadpool(self):
        return self.thread_pool

    def showMsg(self, title : str, msg : str):
        """
        show message box
        """
        QMessageBox.information(None, title, msg)
        pass

    def appDir(self) -> str :
        return self.applicationDirPath()

    def appDataDir(self) -> str :
        return QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)

