
import imagect.api.viewmgr
from imagect.api.viewmgr import ISessionMgr, View, Session
from zope import interface
from . import view
from traits.api import HasTraits, List, Instance
import numpy as np

@interface.implementer(ISessionMgr)
class SessionMgr(HasTraits):

    sess = List(Session)
    current = Instance(Session)
    currentStack = Instance(np.ndarray)
    currentView = Instance(View)

    def __init__(self) :
        pass

    def createSession(self, ds) :

        s = Session()
        s.data = ds

        v = view.SliceView()

        self.currentStack = ds.getStack(int(ds.stack/2))
        v.setImageData( self.currentStack )

        s.views.append(v)
        v.show()

        self.current = s
        self.currentView = v
        self.sess.append(s)

    def currentView(self)  :
        if self.current :
            return self.currentView
        return None

    def currentStack(self):
        if self.current :
            return self.currentStack
        return None

    def currentDataSet(self)  :
        if self.current :
            return self.current.data 
        return None

    def currentSession(self)  :
        return self.current

    def resetCurrentView(self,v) :
        """
        用户界面操作，点击后重置当前窗口，根据当前窗口更新界面显示信息
        """
        pass
        