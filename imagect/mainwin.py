

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

@interface.implementer(IMainWin)
class MainWin(object) :

    """
    implements IMainWin
    """

    def window(self):
        return 0

    def menubar(self):
        return 1

def test() :
    """
    test fun
    """
    pass 

if __name__ == "__main__":
    mw = MainWin()
    print(mw.window())
    