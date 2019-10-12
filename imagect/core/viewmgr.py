
import imagect.api.viewmgr
from imagect.api.viewmgr import ISessionMgr, View, Session
from zope import interface
from . import view
from traits.api import HasTraits, List, Instance
from traitsui.api import View, Item, OKButton, CancelButton, InstanceEditor
import numpy as np

@interface.implementer(ISessionMgr)
class SessionMgr(HasTraits):

    sess = List(Session)
    current = Instance(Session)
    current_tack = Instance(np.ndarray)
    current_view = Instance(object)

    traits_view = View(
        Item(name="sess"),
        Item(name="current", editor=InstanceEditor(), style='custom',),
        buttons=[OKButton, CancelButton],
        #statusbar = [StatusItem(name="title")],
        dock="vertical",
        title="Session"
    )

    def __init__(self) :
        pass

    def createSession(self, ds) :

        s = Session()        
        s.data = ds

        v = view.SliceView()
        v.did = ds.did 
        v.sid = s.sid

        self.current_tack = ds.getStack(int(ds.stack/2))
        v.setImageData( self.current_tack )

        s.views.append(v)
        v.show()

        self.current = s
        self.current_view = v
        self.sess.append(s)

    def currentView(self)  :
        if self.current :
            return self.current_view
        return None

    def currentStack(self):
        if self.current :
            return self.current_tack
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
        