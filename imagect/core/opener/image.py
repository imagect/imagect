from imagect.api.opener import IOpener, IReader
from zope.interface import implementer 
from traits.api import *
from traitsui.api import *

from typing import List

from imagect.api.actmgr import addActFetch, addActFun, renameAct

@implementer(IReader)
class Gray2dImageReader(HasTraits) :
    """
    gray 2d image reader
    """

    path = File()
    _id = Str()
    _suffix = ListStr()
    _category = Str()
    _name = Str()

    def __init__(self) :
        self._id = "reader.gray.2d"
        self._suffix = ["jpg", "png", "bmp"]


    def id(self) -> str :
        return self._id

    def suffix(self) -> List[str] :
        return self._suffix

    def name(self) -> str :
        return self._name.str()

    def category(self) -> str:
        return self._category

    def read(path : str) :
        """
        read in a image
        """
        pass


@addActFun("help.traits.traitui", "show trait ui", index =1, shortcut="F4")
def testRecent(index=0):
    reader = Gray2dImageReader()     
    reader.configure_traits()


renameAct("help.traits", "Traits", index =12)