from imagect.api.recent import IRecent
from zope import interface
from typing import List
import imagect.api.actmgr
import imagect.core.actmgr
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QAction
from imagect.api.actmgr import addActFetch, renameAct


@interface.implementer(IRecent)
def Recent(QObject) :
    """
    recent file manager
    """

    def push(self, file : str) :
        """
        add to top a the list

        if exist in the list, remove and then push to top
        """
        pass

    def clear(self):
        """
        clear the list
        """
        pass 

    def getFiles(self) -> List[str] :
        """
        return a list a files
        """
        pass 

    # def createAction(self) :

@addActFetch("file.recent", "Recent File", index=2)
def recentMenu(qact : QAction):
    return [QAction("Todo", qact), QAction("Recent 1", qact), QAction("Recent 2", qact)]