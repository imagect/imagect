
import imagect.api.viewmgr
from imagect.api.dataset import DataSet
from imagect.api.viewmgr import ISessionMgr, Viewer, Session
from zope import interface
from . import view
from pyqtgraph.Qt import QtCore, QtGui
from traits.api import HasTraits, List, Instance, UUID, Property
from traitsui.api import View, Item, OKButton, CancelButton, InstanceEditor
import numpy as np

@interface.implementer(ISessionMgr)
class SessionMgr(HasTraits):

    current_sid = Property()
    current_vid = Property()
    current_view = Instance(Viewer)

    traits_view = View(
        Item(name="sess"),
         buttons=[OKButton, CancelButton],
        #statusbar = [StatusItem(name="title")],
        dock="vertical",
        title="Session"
    )

    class EventEator(QtCore.QObject):
        def eventFilter(self, obj, evnt):
            if isinstance(evnt, (QtGui.QFocusEvent, QtGui.QCloseEvent)):
                t = self.target(obj)
                if t is not None:
                    if isinstance(evnt, QtGui.QCloseEvent):
                        imagect.api.viewmgr.get().closeView(t.sid, t.vid)

                    if isinstance(evnt, QtGui.QFocusEvent) :
                        if evnt.gotFocus() :
                            imagect.api.viewmgr.get().resetCurrentView(t)

            return super().eventFilter(obj,evnt)

        def target(self, obj):
            if not isinstance(obj, QtGui.QWidget):
                return None

            pw = obj
            while pw is not None:
                if isinstance(pw, Viewer):
                    return pw
                pw = pw.parentWidget()
            return None


    def __init__(self) :
        super().__init__()
        self.sess = []
        self.eator = SessionMgr.EventEator()
        QtGui.QGuiApplication.instance().installEventFilter(self.eator)


    def createSession(self, ds) :

        s = Session()        
        s.data = ds
        
        #todo : create other view according to ds.meta
        v = view.SliceView()
        v.did = ds.did 
        v.sid = s.sid
        v.setImageData( ds.getStack(int(ds.stack/2)) )
        s.insert(v)
        print("view created vid = {}".format(str(v.vid)))
        print("session created sid={}".format(str(s.sid)))
        return (s,v)

    def insertVolSession(self, ds) :
        s,v = self.createSession(ds)
        v.show()
        self.insert(s)

    def _get_current_sid(self) :
        return self.current_view.sid 

    def _get_current_vid(self) :
        return self.current_vid.vid

    def setCurrent(self, sid, vid) :
        s = self.getSession(sid) 
        v = self.getView(sid, vid)
        self.resetCurrentView(v)

    def getCurrent(self):
        """
        return (sid, vid)
        """
        return (self.current_sid, self.current_vid)

    def currentView(self)  :
        return self.current_view

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
        self.current_view = v
        if v : 
            print("current view ={}".format(v.vid))

    def closeView(self, sid, vid) :
        s = self.getSession(sid)
        if not s :
            return 

        if s :
            s.remove(vid)
        if len(s.views) == 0:
            index = 0
            while index < len(self.sess) :
                if self.sess[index].sid == sid :
                    del(self.sess[index])
                    print("remove session sid = {}".format(sid))
                index += 1

    def insert(self, s) :
        res = self.getSession(s.sid)
        if res :
            return False 
        else :
            self.sess.append(s)
            if len(s.views) > 0:
                v = s.views[0]
                self.current_view = v
            return True


    def getSession(self, sid) -> Session :
        res = list(filter( lambda s : s.sid == sid, self.sess))
        return res[0] if len(res) == 1 else None

    def getView(self, sid, vid) -> Viewer :        
        ss = list(filter( lambda s : s.sid == sid, self.sess))
        if len(ss) == 0:
            return None
        vv = list(filter( lambda v : v.vid == vid, ss.views))
        return vv[0] if len(vv) == 1 else None

    def getDataset(self, sid) -> DataSet :
        s = self.getSession(sid)
        if s :
            return s.data 
        else :
            return None 
    