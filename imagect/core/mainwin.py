
from imagect.api.mainwin import IMainWin
from zope import interface

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
    