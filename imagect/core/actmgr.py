from imagect.api.actmgr import IActMgr
from zope.interface import implementer 
from PyQt5.QtCore import QObject
from typing import List
# from PyQt5.QtGui import QAction
from PyQt5.QtWidgets import QMenu, QAction

@implementer(IActMgr)
class ActMgr(QObject) :
    """
    ActMgr
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.file = QAction("File",self)
        self.edit = QAction("Edit",self)
        self.image= QAction("Image", self)

    def topActions(self) -> List[QAction] :
        return [self.file, self.edit, self.image]

    def addSubAct(self, parent : QAction, child :QAction):
        """
        add sub action  parent | child
        """
        if parent in self.topActions() :
            child.setParent(parent)
            menu = parent.menu()
            if menu is None:
                parent.setMenu(QMenu())
                menu = parent.menu()

            menu.addAction(child)

        else :
            raise "Bad Action"
