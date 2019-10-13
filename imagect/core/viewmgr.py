
import imagect.api.viewmgr
from imagect.api.dataset import DataSet
from imagect.api.viewmgr import ISessionMgr, Viewer, Session
from zope import interface
from . import view
from traits.api import HasTraits, List, Instance, UUID
from traitsui.api import View, Item, OKButton, CancelButton, InstanceEditor
import numpy as np

@interface.implementer(ISessionMgr)
class SessionMgr(HasTraits):

    sess = List(Session)

    current_sid = UUID
    current_vid = UUID
    current_view = Instance(Viewer)

    traits_view = View(
        Item(name="sess"),
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
        
        #todo : create other view according to ds.meta
        v = view.SliceView()
        v.did = ds.did 
        v.sid = s.sid
        v.setImageData( ds.getStack(int(ds.stack/2)) )
        s.views.append(v)
        return (s,v)

    def insertVolSession(self, ds) :
        s,v = self.createSession(ds)
        v.show()
        self.insert(s)

    def setCurrent(self, sid, vid) :
        s = self.getSession(sid) 
        v = self.getView(sid, vid)
        if s :
            self.current_sid = sid
        if v :
            self.current_vid = vid

    def getCurrent(self):
        """
        return (sid, vid)
        """
        return (self.current_sid, self.current_vid)

    def currentView(self)  :
        v = self.getView(self.current_sid, self.current_vid)
        return v

    def currentStack(self):
        v = self.getView(self.current_sid, self.current_vid)
        if v :
            return v.slice_data
        return None

    def currentDataSet(self)  :
        return self.getDataset(self.current_sid)

    def currentSession(self)  :
        return self.getSession(self.current_sid)

    def resetCurrentView(self,v) :
        """
        用户界面操作，点击后重置当前窗口，根据当前窗口更新界面显示信息
        """
        pass

    def insert(self, s) :
        res = self.getSession(s.sid)
        if res :
            return False 
        else :
            self.sess.append(s)
            if len(s.views) > 0:
                v = s.views[0]
                self.current_vid = v.vid
                self.current_sid = s.sid
            return True


    def getSession(self, sid) -> Session :
        res = [filter( lambda s : s.sid == sid, self.sess)]
        return res[0] if len(res) == 1 else None

    def getView(self, sid, vid) -> Viewer :        
        ss = [filter( lambda s : s.sid == sid, self.sess)]
        if len(ss) == 0:
            return None
        vv = [filter( lambda v : v.vid == vid, ss.views)]
        return vv[0] if len(vv) == 1 else None

    def getDataset(self, sid) -> DataSet :
        s = self.getSession(sid)
        if s :
            return s.data 
        else :
            return None 
    