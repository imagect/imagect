
from zope.interface import implementer
from zope.component import getGlobalSiteManager
from collections import defaultdict
from traits.api import *
from traitsui.api import *
from traitsui.menu import OKButton, CancelButton
import numpy as np
import imagect.api.datasample as dsample
from zope.interface import Interface, Attribute
from zope.component import getUtility
import uuid
from rx.subject import Subject
import imagect

# TODO dataset input
# TODO dataset management
# TODO add datameta for dataset, describe source and reader

sampleId = "784c59df-acb8-4d4e-b2e5-fa926264c79e"

class DataMeta(HasTraits):
    path = String()
    category = String()
    reader = Type()


class DataSet(HasTraits):

    """
    DataSet

    dtype : numpy.dtype

    """
    did = UUID(can_init=True)

    types = List([
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

    #data = Instance(np.ndarray, transient=True)

    crrentStackIndex = Int()

    stackUpdated = Instance(Subject)

    def __init__(self, fakedata=False):

        self.meta = DataMeta()
        self.id = uuid.uuid4()
        self.currentStackIndex = 0

        if fakedata:
            data = dsample.vol()
            s, w, h = data.shape
            data.resize((s, w, h, 1))
            self.data = data
        #
        self.stackUpdated = Subject()

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

    def getCurrentStack(self) :
        return self.getStack(self.currentStackIndex)

    def updateCurrentStack(self, sliceData) :
        self.updateStack(self.currentStackIndex, sliceData)

    def updateStack(self, index, sliceData) :
        """
        更新一个切片的数据
        """
        shape = sliceData.shape 
        assert self.stack > index and index > -1
        copy = sliceData
        if len(shape) == 2 :
            assert self.channel == 1
            assert self.height == shape[0]
            assert self.width == shape[1]
            copy = sliceData.reshape((shape[0],shape[1],1))
        elif len(shape) == 3:
            assert self.channel == shape[2]

        # print(copy.dtype)
        # print(self.data.dtype)
        # imagect.showImage(copy.astype(self.data.dtype))

        self.data[index] = copy.astype(self.data.dtype)
        self.stackUpdated.on_next(index)

    def asSlice(self) :
        """
        以(height, width, channel)的格式导出数据
        """
        assert self.stack == 1
        return self.data.reshape(self.height,self.width,self.channel)

    def asGray(self) :
        """
        以(height, width)的格式导出数据
        """
        assert self.stack == 1
        assert self.channel == 1
        return self.data.reshape(self.height, self.width)

    traits_view = View(
        Group(
            Item(name="did"),
            Item(name="dtype"),
            Item(name="shape"),
            Item(name="stack"),
            Item(name="height"),
            Item(name="width"),
            Item(name="channel"),
            Item(name="meta", editor=InstanceEditor(), style='custom',),
            label="Property",
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

        meta = DataMeta()
        meta.category = "vol"
        ds.meta = meta
        return ds

    @staticmethod
    def fromRGB(data):
        assert len(data.shape) == 3
        h, w, c = data.shape
        d = data.reshape((1, h, w, c))
        ds = DataSet()
        ds.data = d
        
        meta = DataMeta()
        meta.category = "rgb"
        ds.meta = meta
        return ds

    @staticmethod
    def fromGray(data):
        assert len(data.shape) == 3
        h, w = data.shape
        d = data.reshape((1, h, w, 1))
        ds = DataSet()
        ds.data = d        
        
        meta = DataMeta()
        meta.category = "gray"
        ds.meta = meta
        return ds

    @staticmethod
    def fromSample(name="vol"):
        create = {
            "vol": dsample.vol,
            "hydrogen": dsample.hydrogen,
            "chessboard" : dsample.chessboard
        }
        if name in create:
            return DataSet.fromVol(create[name]())
        else:
            return DataSet.fromVol(dsample.vol())

class IDataMgr(Interface):

    """
    DataMngr
    """

    def get(id: str) -> DataSet:
        """
        fetch data by id
        """
        pass

    def add(ds: DataSet):
        """
        fetch 
        """
        pass

    def remove(id: str):
        """
        remove
        """
        pass

    def queryAll():
        """
        query
        """
        pass


def get():
    return getUtility(IDataMgr)

def sample() :
    mgr = get()
    data = mgr.get(sampleId)
    if data is None :
        data = DataSet.fromSample()
        mgr.add(data)
    return data

# TODO data manager
@implementer(IDataMgr)
class DataMgr(HasTraits):

    """
    data manager
    """

    datas = Dict()  # key_trait=UUID, value_trait=DataSet)

    def get(self, id: str):
        if id in self.datas:
            return self.datas[id]
        else:
            return None

    def add(self, ds):
        if ds.did in self.datas:
            assert False
        self.datas[ds.did] = ds

    def remove(self, id: str):
        if id in self.datas:
            del self.datas[id]

    def queryAll(self):
        """
        query
        """
        return [k for k in self.datas.keys()]


gsm = getGlobalSiteManager()
try:
    mgr = get()
except:
    mgr = DataMgr()
    gsm.registerUtility(mgr, IDataMgr)


if __name__ == "__main__":
    ds = DataSet(fakedata=True)
    #ds.meta = DataMeta()
    ds.configure_traits()
