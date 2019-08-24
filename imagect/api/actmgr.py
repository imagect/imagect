from zope.interface import Interface, Attribute
from zope.component import getUtility
from PyQt5.QtWidgets import QAction, QMenu, QWidgetAction
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import QObject
from typing import List
from collections import namedtuple

class IAction(object):
    
    def __init__(
        self,
        icon,
        id,
        pid,
        title,
        index = 0,
        callable = None,
        widget = None,
        fetch = None,
        shortcut = None
    ):
        super().__init__()
        self.icon = icon
        self.callable = callable
        self.id = id
        self.pid = pid
        self.title = title
        self.index = index
        self.widget = widget
        self.fetch = fetch
        self.shortcut = shortcut

    def __repr__(self):
        return "id={}, title={}".format(self.id, self.title)

# IAction = namedtuple("IAction",
#     ["icon", "callable", "id", "pid", "title", "index", "widget"]
# )

def createAction(id, title, callable = None, index =0, shortcut=None) :
    return IAction(
        icon="",
        id = id,
        pid = ".".join(id.split(".")[0:-1]),
        title = title,
        index=index,
        callable = callable,
        widget=None,
        shortcut = shortcut
    )

def createWAction(id, title, widget=None, index =0, shortcut=None) :
    return IAction(
        icon="",
        id = id,
        pid = ".".join(id.split(".")[0:-1]),
        title = title,
        index=index,
        callable = None,
        widget=widget,
        shortcut = shortcut
    )

def creatchFecthAction(id, title, fetch, index = 0, shortcut=None):
    return IAction(
        icon="",
        id = id,
        pid = ".".join(id.split(".")[0:-1]),
        title = title,
        index=index,
        callable = None,
        widget= None,
        fetch = fetch,
        shortcut = shortcut
    )

class IActMgr(Interface) :
    
    """
    Action Manager

    要包含所有的命令节点，每个命令节点包含一个菜单用于显示全部子命令
    """

    file = Attribute("""file menu""")

    edit = Attribute("""edit menu""")

    image= Attribute("""image menu""")

    test = Attribute("""test menu""")

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

    def renameAct(id: str, title: str, index = 0):
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

    if act.shortcut is not None:
        qact.setShortcut(act.shortcut)

    children = get().queryChildren(act.id)

    # action widget
    if act.widget :
        menu = QMenu()
        wact = QWidgetAction(menu)  
        wact.setDefaultWidget(act.widget(menu))

        menu.addAction(wact)   

        qact.setMenu(menu) 
        # wact.setText(act.title)
        # wact.setIcon(QIcon(act.icon))
        return qact

    # single action
    if act.callable is not None:
        def cb(checked) :
            print(act)
            print(qact.text())
            act.callable()
        qact.triggered.connect(cb)
        return qact

    # sub menu
    elif act.fetch is not None:   
        menu = QMenu()
        qact.setMenu(menu)

        def fresh():   
            acts = act.fetch(menu)
            for a in acts:
                menu.addAction(a)
            
        menu.aboutToShow.connect(fresh)
        menu.aboutToHide.connect(menu.clear)
        return qact  

    else :        
        menu = QMenu()
        qact.setMenu(menu)
  
        for a in children:
            qa = toQAction(a, qact)
            menu.addAction(qa) 

        return qact        

def renameAct(id : str, title :str, index = 0):
    get().renameAct(id, title, index)

def addAct(act : IAction):
    get().addAct(act)

def addActFun(id : str, text: str, index=0, shortcut=None):
    def add(callable):
        a = createAction(id, title=text, callable=callable, index=index, shortcut=shortcut)
        addAct(a)
    return add

def addActWdg(id: str, text: str, index=0, shortcut=None):
    def add(wdg_factory) :
        a = createWAction(id, title=text, widget=wdg_factory, index=index, shortcut=shortcut)
        addAct(a)
    return add

def addActFetch(id : str, title : str, index = 0, shortcut=None):
    def add(fetch) :
        a = creatchFecthAction(id, title=title, fetch=fetch, index=index, shortcut=shortcut)
        addAct(a)
    return add

if __name__ == "__main__" :
    act = createAction(id="file", title="titld", index=1)
    print(act)