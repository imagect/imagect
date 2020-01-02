from imagect.api.console import IConsole, get
from zope.interface import implementer
from imagect.api.mainwin import IMainWin
from imagect.api.mainwin import get as getWin


@implementer(IConsole)
class Console(object):
    """
    embeding a python console in app
    """

    def clear(self):
        """
        clears the terminal
        """
        getWin().console()._control.clear()

    def printText(self, text: str):
        """
        show text in console
        """
        s = "print({})".format(text)
        self.execute(s)

    def execute(self, command):
        """
        execute python statement in console
        """
        import PyQt5.QtWidgets
        # PyQt5.QtWidgets.QApplication.clipboard().setText(command)
        # getWin().console().paste()
        # getWin().console()._append_plain_text(command)
        # command += "\n"
        getWin().console().execute(source=command)


from imagect.api.actmgr import addActFun, renameAct


@addActFun("help.console.welcome", "welcome message", index=1)
def testRecent():
    get().printText("welcome")


renameAct("help.console", "Console", index=11)
