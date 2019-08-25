from zope.interface import Interface, Attribute
from zope.component import getUtility
from typing import List

class IOpener(Interface) :
    """
    file opener
    """

    def id() -> str :
        pass

    def suffix() -> List[str] :
        pass

    