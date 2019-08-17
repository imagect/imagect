from zope.interface import Interface, Attribute
from zope.component import getUtility
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from typing import List

class IActMgr(Interface) :
    
    """
    Action Manager

    要包含所有的命令节点，每个命令节点包含一个菜单用于显示全部子命令
    """

    file = Attribute("""file menu""")

    edit = Attribute("""edit menu""")

    image= Attribute("""image menu""")

    def topActions() -> List[QAction] :
        pass

    def addSubAct(parent : QAction, child :QAction):
        """
        add sub action  parent | child
        """
        pass

def get() :
    return getUtility(IActMgr) 

def addActionWithIcon(parent : QAction, cls, icon : QIcon, title: str):
    get().addSubAct(parent, cls(icon, title))

def addAction(parent : QAction, cls):
    get().addSubAct(parent, cls())


class AppAction(QAction):
    def __init__(self, QIcon, str, parent=None):
        return super().__init__(QIcon, str, parent=parent)

class ExtAction(AppAction):
    def __init__(self, QIcon, str, parent=None):
        return super().__init__(QIcon, str, parent=parent)

