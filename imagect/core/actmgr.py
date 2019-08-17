import imagect.api.actmgr
from imagect.api.actmgr import IActMgr, IAction, createAction
from zope.interface import implementer 
from typing import List
# from PyQt5.QtGui import QAction
from PyQt5.QtWidgets import QMenu, QAction
from collections import defaultdict

@implementer(IActMgr)
class ActMgr(object) :
    """
    ActMgr
    """

    def __init__(self, ):
        super().__init__()
        self.actions = {}
        self.groups = defaultdict(dict)
        self.file = createAction("file", "File")
        self.edit = createAction("edit", "Edit")
        self.image= createAction("image", "Image")
        for a in [self.file, self.edit, self.image] :
            self.addAct(a)

    def topActions(self) -> List[QAction] :
        return [self.file, self.edit, self.image]

    def addAct(self, act :IAction):
        """
        add sub action  parent | child
        """
        if not act.id in self.actions:
            if act.pid not in self.actions.keys():
                keys = act.pid.split(".")
                grandpa = ".".join(keys[:-1])
                pa = createAction(act.pid, act.pid)
                if grandpa == "" : # child.id == child.pid == ""
                    self.actions[pa.id] = pa
                else:
                    self.addAct(pa)
            self.actions[act.id] = act
            self.groups[act.pid][act.id] = act
        else :
            raise "duplicated Action id = {}".format(act.id)

    def remAct(self, id : str) :
        if id in self.actions:
            act = self.actions[id]
            self.actions.pop(id, None)
            self.groups[act.pid].pop(act.id)

    def queryChildren(self, pid : str):
        """
        todo: sort by index
        """
        return self.groups[pid].values()


from zope.component import getGlobalSiteManager
gsm = getGlobalSiteManager()
try:
    mgr = imagect.api.actmgr.get()
except:
    actmgr = ActMgr()    
    gsm.registerUtility(actmgr, IActMgr)