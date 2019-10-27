

from zope.interface import Interface, Attribute
from zope.component import getUtility
from traits.api import Instance, List, HasTraits, UUID, Property
# from traitsui.api import *
from imagect.api.dataset import DataSet
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import uuid

class Viewer(QtGui.QMainWindow) :
    """
    sid : sessionid == datasetid
    """

    did = UUID()

    sid = UUID()

    vid = UUID()

    slice_data = Instance(np.ndarray)

    vol_data = Instance(DataSet)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(False)
        self.vid = uuid.uuid4()
        self.vol_data = None
        self.slice_data = None

    def setImageData(self, data : DataSet) :
        pass


class Session(HasTraits):

    sid = Property() 

    did = Property()

    data = DataSet()

    # views = List(Viewer)

    # traits_view = View(
    #     Item(name="views"),
    #     Item(name="data", editor=InstanceEditor(), style='custom',),
    #     buttons=[OKButton, CancelButton],
    #     #statusbar = [StatusItem(name="title")],
    #     dock="vertical",
    #     title="Session"
    # )
    def __init__(self) :
        super().__init__()
        self.views = []
        

    def _get_did(self) :
        return self.data.did

    def _get_sid(self) :
        return self.data.did


    def remove(self, vid) :
        index = 0
        while index < len(self.views) :
            if self.views[index].vid == vid :
                del(self.views[index])
                print("remove viewer vid={}".format(vid))
            index += 1

    def insert(self, v) :
        vs = list(filter(lambda o : o.vid == v.vid, self.views))
        v.sid = self.sid
        assert v.did == self.did 
        if len(vs) == 0:
            self.views.append(v)


class ISessionMgr(Interface) :
    """
    ViewMgr
    """
    def createSession(ds) :
        pass

    def insertVolSession(ds) :
        pass

    def setCurrent(sid, vid) :
        pass

    def getCurrent():
        """
        return (sid, vid)
        """
        pass 

    def currentView() -> Viewer :
        pass

    def currentDataSet() -> DataSet :
        pass 

    def currentSession() -> Session :
        pass

    def currentStack() :
        pass

    def resetCurrentView(v) :
        """
        用户界面操作，点击后重置当前窗口，根据当前窗口更新界面显示信息
        """
        pass

    def insert(s) -> bool :
        """
        insert session
        """
        pass

    def getSession(sid) -> Session :
        pass

    def getView(sid, vid) -> Viewer :
        pass

    def getDataset(sid) -> DataSet :
        pass 

    

from zope.component import getUtility
def get():
    return getUtility(ISessionMgr)


if __name__ == "__main__":
    ds = Session()
    ds.configure_traits()