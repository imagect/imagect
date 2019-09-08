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
        s = "print({})".format(text)
        self.execute(s)        

    def execute(self, command) :
        """
        execute python statement in console
        """
        import PyQt5.QtWidgets 
        PyQt5.QtWidgets.QApplication.clipboard().setText(command)
        getWin().console().paste()
        # getWin().console()._append_plain_text(command)
        getWin().console().execute(source=command)


from imagect.api.actmgr import addActFetch, addActFun, renameAct
@addActFun("help.console.init", "init console", index =2, shortcut="F1")
def testRecent():
    get().execute("import imagect.api.util as it")
    
@addActFun("help.console.welcome", "welcome message", index =1)
def testRecent():
    get().printText("welcome")

renameAct("help.console", "Console", index =11)