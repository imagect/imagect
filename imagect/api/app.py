from zope import interface 
from zope.component import getUtility
import os.path 

class IApp(interface.Interface) :
    """
    App Interface for imagect
    """

    def mainwin() :
        """
        IMainWin
        """
        pass

    def asyncio_loop():
        """
        loop for ayncio
        """
        pass

    def rx_scheduler():
        """
        scheduler from qt ui loop
        """
        pass

    
    def rx_threadpool(self):
        """
        thread pool scheduler
        """
        pass

    def showMsg(title : str, msg : str):
        """
        show message box
        """
        pass

    def appDir() -> str:
        """
        application dir
        """
        pass

    def appDataDir() -> str:
        """
        appDataDir dir
        """
        pass


def get() :
    return getUtility(IApp)

def getLoop() :
    return get().asyncio_loop()

def getScheduler() :
    return get().rx_scheduler()
