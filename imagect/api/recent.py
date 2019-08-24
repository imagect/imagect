
from zope.interface import Interface, Attribute
from zope.component import getUtility
from typing import List

class IRecent(Interface):

    """
    push a file to recent file list
    """

    def push(file : str) :
        """
        add to top a the list
        """
        pass

    def clear():
        """
        clear the list
        """
        pass 

    def getFiles() -> List[str] :
        """
        return a list a files
        """
        pass 

        