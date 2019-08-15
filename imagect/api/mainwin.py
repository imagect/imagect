

from zope import interface

class IMainWin(interface.Interface) :

    """
    mainwin of the app
    """

    def window() :
        """
        window
        """
        pass

    def menubar() :
        """
        menubar
        """
        pass
