

from zope.interface import Interface, Attribute
from zope.component import getUtility
from traits.api import *
from traitsui.api import *
from imagect.api.dataset import DataSet
from pyqtgraph.Qt import QtCore, QtGui

class ViewMeta(HasTraits):
    pass


class View(QtGui.QMainWindow) :
    """
    sid : sessionid == datasetid
    """
    def __init__(self):
        super().__init__()
        self.sid = ""
    
    pass


class Session(HasTrait):

    data = Instance(DataSet)

    views = List(View)


class IViewMgr(Interface) :
    """
    ViewMgr
    """

    def currentView() -> View :
        pass

    def currentDataSet() -> DataSet :
        pass 

    def currentSession() -> Session :
        pass

    def resetCurrentView(v) :
        """
        用户界面操作，点击后重置当前窗口，根据当前窗口更新界面显示信息
        """
        pass