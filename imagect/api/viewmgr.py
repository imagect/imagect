

from zope.interface import Interface, Attribute
from zope.component import getUtility
from traits.api import Instance, List, HasTraits, UUID, Property
from traitsui.api import *
from imagect.api.dataset import DataSet
from pyqtgraph.Qt import QtCore, QtGui


class Viewer(QtGui.QMainWindow) :
    """
    sid : sessionid == datasetid
    """

    did = UUID

    sid = UUID 

    vid = UUID
    
    pass


class Session(HasTraits):

    sid = Property() 

    did = Property()

    data = DataSet()

    views = List(Viewer)

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
        

    def _get_did(self) :
        return self.data.did

    def _get_sid(self) :
        return self.data.did


class ISessionMgr(Interface) :
    """
    ViewMgr
    """
    def createSession(ds) :
        pass

    def currentView() -> View :
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

from zope.component import getUtility
def get():
    return getUtility(ISessionMgr)


if __name__ == "__main__":
    ds = Session()
    ds.configure_traits()