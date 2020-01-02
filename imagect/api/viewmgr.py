

from zope.interface import Interface, Attribute
from zope.component import getUtility
from traits.api import Instance, List, HasTraits, UUID, Property
from imagect.api.dataset import DataSet
from imagect.ic.image_plus import ImagePlus
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import uuid

class Viewer(QtGui.QMainWindow) :

    did = UUID()

    iid = UUID()

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


class IImagePlusMgr(Interface) :
    """
    ViewMgr
    """
    def createImagePlus(ds) :
        pass

    def insertVolImagePlus(ds) :
        pass

    def setCurrent(iid, vid) :
        pass

    def getCurrent():
        """
        return (iid, vid)
        """
        pass 

    def currentView() -> Viewer :
        pass

    def currentImagePlus() -> ImagePlus :
        pass

    # def currentSlice() :
    #     pass

    def resetCurrentView(v) :
        """
        用户界面操作，点击后重置当前窗口，根据当前窗口更新界面显示信息
        """
        pass

    def insert(s) -> bool :
        """
        insert imageplus
        """
        pass

    def getImagePlus(iid) -> ImagePlus :
        pass

    def getView(iid, vid) -> Viewer :
        pass

    # def getDataset(iid) -> DataSet :
    #     pass

    

from zope.component import getUtility
def get():
    return getUtility(IImagePlusMgr)


if __name__ == "__main__":
    ds = ImagePlus()
    ds.configure_traits()