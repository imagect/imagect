from imagect.api.console import IConsole, get
from zope.interface import implementer 
from imagect.api.mainwin import IMainWin
from imagect.api.mainwin import get as getWin

@implementer(IConsole)
class Console(object) :

    """
    embeding a python console in app
    """

    def clear(self) :
        """
        clears the terminal
        """
        getWin().console()._control.clear()

    def printText(self, text: str) :
        """
        show text in console
        """
        getWin().console()._append_plain_text(text)

    def execute(self, command) :
        """
        execute python statement in console
        """
        getWin().console()._execute(command,True)


from imagect.api.actmgr import addActFetch, addActFun, renameAct
@addActFun("test.console.init", "init console", index =2, shortcut="F5")
def testRecent():
    get().execute("import imagect.api.util as it")
    
@addActFun("test.console.welcome", "welcome message", index =1)
def testRecent():
    get().printText("welcome")

renameAct("test.console", "Console", index =11)