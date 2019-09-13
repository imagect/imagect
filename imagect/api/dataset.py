
from traits.api import *
from traitsui.api import *
from traitsui.menu import OKButton, CancelButton
import numpy as np
import imagect.api.datasample as dsample
from zope.interface import Interface, Attribute
from zope.component import getUtility

# TODO dataset input
# TODO dataset management
# TODO add datameta for dataset, describe source and reader
# class DataMeta(HasTraits) :

#     path = String()
#     class Category(Enum) :
#         RGB  = 1
#         GRAY = 2
#         VOL  = 3

#     category = Int()
#     reader = String()

class DataSet(HasTraits):

    """
    DataSet

    dtype : numpy.dtype

    """
    id = UUID()

    possible_types = List([
        np.int8,
        np.uint8,
        np.int32,
        np.uint32,
        np.int64,
        np.uint64,
        np.float32,
        np.float64
    ])

    meta = DataMeta()

    dtype = Property()

    stack = Property()

    height = Property()

    width = Property()

    channel = Property()

    shape = Property()

    data = Instance(np.ndarray, transient=True)

    def __init__(self, fakedata=False):

        if fakedata:
            data = dsample.vol()
            s, w, h = data.shape
            data.resize((s, w, h, 1))
            self.data = data

    def astype(self, t):
        ds = DataSet()
        ds.data = self.data.astype(t)
        return ds

    def _get_dtype(self):
        return self.data.dtype

    def _set_dtype(self, type):
        self.data.astype(type)

    def _get_shape(self):
        return self.data.shape

    def _get_stack(self):
        shape = self.data.shape
        assert len(shape) == 4
        return shape[0]

    def _get_height(self):
        shape = self.data.shape
        assert len(shape) == 4
        return shape[1]

    def _get_width(self):
        shape = self.data.shape
        assert len(shape) == 4
        return shape[2]

    def _get_channel(self):
        shape = self.data.shape
        assert len(shape) == 4
        assert shape[3] == 1 or shape[3] == 3 or shape[3] == 4
        return shape[3]

    def getStack(self, s):
        assert s > -1 and s < self.stack
        s = self.data[s, :, :, :]
        if self.channel == 1:
            s = s.squeeze(axis=2)
        return s

    traits_view = View(
        VGroup(
            Item(name="id"),
            Item(name="dtype"),
            Item(name="shape"),
            Item(name="stack"),
            Item(name="height"),
            Item(name="width"),
            Item(name="channel"),
            label="DataSet Property",
            show_border=True
        ),
        buttons=[OKButton, CancelButton],
        #statusbar = [StatusItem(name="title")],
        dock="vertical",
        title="Dataset Property"
    )

    @staticmethod
    def fromVol(data):
        assert len(data.shape) == 3
        s, w, h = data.shape
        d = data.reshape((s, w, h, 1))
        ds = DataSet()
        ds.data = d
        return ds

    @staticmethod
    def fromRGB(data):
        assert len(data.shape) == 3
        h,w,c = data.shape
        d = data.reshape((1,h,w,c))
        ds = DataSet()
        ds.data = d
        return ds

    @staticmethod
    def fromGray(data):
        assert len(data.shape) == 3
        h,w = data.shape
        d = data.reshape((1,h,w,1))
        ds = DataSet()
        ds.data = d
        return ds

    @staticmethod
    def sample(name="vol"):
        create = {
            "vol": dsample.vol,
            "hydrogen": dsample.hydrogen
        }
        if name in create:
            return DataSet.fromVol(create[name]())
        else:
            return DataSet.fromVol(dsample.vol())

class IDataMgr(Interface) :

    """
    DataMngr
    """

    def get(id : str) -> DataSet :
        """
        fetch data by id
        """
        pass 

    def add(ds : DataSet) :
        """
        fetch 
        """
        pass

    def remove(id : str) :
        """
        remove
        """
        pass

    def queryAll():
        """
        query
        """
        pass

def get() :
    return getUtility(IDataMgr) 

#TODO data manager
from zope.interface import implementer 
from collections import defaultdict

@implementer(IDataMgr)
class DataMgr(HasTraits):

    """
    data manager
    """

    datas = Dict() #key_trait=UUID, value_trait=DataSet)

    def get(self, id : str) :
        if id in self.datas :
            return self.datas[id] 
        else :
            return None

    def add(self, ds):
        if ds.id in self.datas :
            assert False 
        self.datas[ds.id] = ds 

    def remove(self, id : str):
        if id in self.datas :
            del self.datas[id] 

    def queryAll(self):
        """
        query
        """
        return [k for k in self.datas.keys()]


from zope.component import getGlobalSiteManager
gsm = getGlobalSiteManager()
try:
    mgr = get()
except:
    mgr = DataMgr()    
    gsm.registerUtility(mgr, IDataMgr)
    

if __name__ == "__main__":
    ds = DataSet(fakedata=True)
    ds.configure_traits(kind="live")
    mgr.configure_traits(kind="live")

