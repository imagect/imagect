from zope.interface import Interface, Attribute
from zope.component import getUtility

class IConsole(Interface) :

    """
    embeding a python console in app
    """

    def clear() :
        """
        clears the terminal
        """
        pass

    def printText(text: str) :
        """
        show text in console
        """
        pass

    def execute(command) :
        """
        execute python statement in console
        """
        pass

def get() :
    return getUtility(IConsole) 