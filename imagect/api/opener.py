from zope.interface import Interface, Attribute
from zope.component import getUtility
from typing import List

class IOpener(Interface) :
    """
    file opener
    """

    def open( path : str ) :
        """
        open a file, or a directory
        """
        pass 

    
class IReader(Interface) :

    def id() -> str :
        pass

    def suffix() -> List[str] :
        pass

    def name() -> str :
        pass

    def category() -> str:
        pass

    def read(path : str) :
        pass