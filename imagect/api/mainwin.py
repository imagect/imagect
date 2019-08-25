from zope import interface
from zope.component import getUtility

class IMainWin(interface.Interface) :

    """
    mainwin of the app
    """

    def window() :
        """
        window
        """
        pass

    def menuBar() :
        """
        menubar
        """
        pass

    def console() :
        """
        console 
        """
        pass

def get() :
    return getUtility(IMainWin)
