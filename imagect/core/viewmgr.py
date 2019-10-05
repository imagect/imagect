
import imagect.api.viewmgr
from imagect.api.viewmgr import ISessionMgr, Session
from zope import interface
from . import view
from traits.api import HasTraits, List
from traitsui.api import *

@interface.implementer(ISessionMgr)
class SessionMgr(HasTraits):

    sess = List(Session)

    def __init__(self) :
        pass

    def createSession(self, ds) :

        s = Session()
        s.data = ds

        v = view.SliceView()
        v.setImageData( ds.getStack(int(ds.stack/2)))

        s.views.append(v)
        v.show()

        self.sess.append(s)

    def currentView(self)  :
        pass

    def currentDataSet(self)  :
        pass 

    def currentSession(self)  :
        pass

    def resetCurrentView(self,v) :
        """
        用户界面操作，点击后重置当前窗口，根据当前窗口更新界面显示信息
        """
        pass
        