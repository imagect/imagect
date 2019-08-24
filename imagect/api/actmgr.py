from zope.interface import Interface, Attribute
from zope.component import getUtility
from PyQt5.QtWidgets import QAction, QMenu, QWidgetAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject
from typing import List
from collections import namedtuple

class IAction(object):
    
    def __init__(
        self,
        icon,
        callable,
        id,
        pid,
        title,
        index,
        widget
    ):
        super().__init__()
        self.icon = icon
        self.callable = callable
        self.id = id
        self.pid = pid
        self.title = title
        self.index = index
        self.widget = widget

    def __repr__(self):
        return "id={}, title={}".format(self.id, self.title)

# IAction = namedtuple("IAction",
#     ["icon", "callable", "id", "pid", "title", "index", "widget"]
# )

def createAction(id, title, callable = None, index =0) :
    return IAction(
        icon="",
        callable = callable,
        id = id,
        pid = ".".join(id.split(".")[0:-1]),
        title = title,
        index=index,
        widget=None
    )

def createWAction(id, title, widget=None, index =0) :
    return IAction(
        icon="",
        callable = None,
        id = id,
        pid = ".".join(id.split(".")[0:-1]),
        title = title,
        index=index,
        widget=widget
    )

class IActMgr(Interface) :
    
    """
    Action Manager

    要包含所有的命令节点，每个命令节点包含一个菜单用于显示全部子命令
    """

    file = Attribute("""file menu""")

    edit = Attribute("""edit menu""")

    image= Attribute("""image menu""")

    def topActions() -> List[IAction] :
        pass

    def addAct(act : IAction):
        """
        add sub action  parent | child
        """
        pass

    def remAct(id :str):
        """
        remove action by id
        """
        pass

    def renameAct(id: str, title: str):
        """
        set action title
        """
        pass

    def queryChildren(self, pid : str) -> List[IAction]:
        """
        query actions by parent id
        """
        pass

    def queryAll(self) -> List[IAction] :
        """
        query all actions
        """
        pass

def get() :
    return getUtility(IActMgr) 

def toQAction(act : IAction, parent : QObject) :
    
    qact = QAction(QIcon(act.icon), act.title, parent=parent)

    # action widget
    if act.widget :
        qact = QAction(QIcon(act.icon), act.title, parent=parent)
        menu = QMenu()
        wact = QWidgetAction(menu)  
        wact.setDefaultWidget(act.widget(menu))

        menu.addAction(wact)   

        qact.setMenu(menu) 
        # wact.setText(act.title)
        # wact.setIcon(QIcon(act.icon))
        return qact

    children = get().queryChildren(act.id)

    # single action
    if act.callable is not None:
        def cb(checked) :
            print(act)
            act.callable()
        qact.triggered.connect(cb)
        return qact

    # sub menu
    else :   
        menu = QMenu()
        qact.setMenu(menu)

        def fresh():            
            for a in children:
                qa = toQAction(a, qact)
                menu.addAction(qa) 

        def aboutToShow(): 
            fresh()               
            # pass

        def aboutToHide():
            acts = menu.actions()            
            menu.clear()
            for a in acts:
                a.deleteLater()
            pass

        menu.aboutToShow.connect(aboutToShow)
        menu.aboutToHide.connect(aboutToHide)
        return qact         


def toQActionWithSubMenu(act : IAction, mngr: IActMgr, parent : QObject) :
    root = toQAction(act, parent)
    # children = mngr.queryChildren(act.id)
    # if len(children) > 0 or act.pid == "":
    #     submenu = QMenu(act.title, parent=None)
    #     submenu.setTitle(act.title)
    #     root.setMenu(submenu)
    #     for a in children :
    #         qact = toQActionWithSubMenu(a, mngr, root)
    #         submenu.addAction(qact)
    return root

def renameAct(id : str, title :str):
    get().renameAct(id, title)

def addAct(act : IAction):
    get().addAct(act)

def addActFun(id : str, text: str):
    def add(callable):
        a = createAction(id, title=text, callable=callable)
        addAct(a)
    return add

def addActWdg(id: str, text: str):
    def add(wdg_factory) :
        a = createWAction(id, title=text, widget=wdg_factory)
        addAct(a)
    return add

if __name__ == "__main__" :
    act = createAction(id="file", title="titld", index=1)
    print(act)