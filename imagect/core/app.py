
from imagect.api.app import IApp
import imagect.api.app as app
from zope import interface 
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QStandardPaths
from asyncqt import QEventLoop, QThreadExecutor
import asyncio
import concurrent
from imagect.qtools import gui_scheduler, qtApp

@interface.implementer(IApp)
class App(object):

    """
    application
    """

    def __init__(self):
        super().__init__()

        qtApp.setApplicationName("imagect")

        self.loop = QEventLoop(qtApp)
        asyncio.set_event_loop(self.loop)

        self.thread_pool = concurrent.futures.ThreadPoolExecutor()

    def qt_app(self):
        return qtApp

    def asyncio_loop(self):
        return self.loop

    def threadpool(self):
        return self.thread_pool

    def gui_scheduler(self):
        return gui_scheduler

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

