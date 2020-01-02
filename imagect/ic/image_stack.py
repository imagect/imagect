from traits.api import HasTraits, UUID, List, String, Type, Int, Property, Instance
from traitsui.api import View, Group, Item, InstanceEditor, OKButton, CancelButton
import numpy as np
import imagect.api.datasample as dsample
import uuid

"""

image stack
    shape = (layer, height, width, channel)

"""


class DataMeta(HasTraits):
    path = String()
    category = String()
    reader = Type()


class ImageStack(HasTraits):

    """
    ImageStack

    dtype : numpy.dtype

    """
    did = UUID(can_init=True)

    types = List([
        # np.int8,
        np.uint8,
        # np.int32,
        np.uint32,
        # np.int64,
        # np.uint64,
        np.float32,
        # np.float64
    ])

    meta = DataMeta()

    # TODO offset
    offset = Int(0)

    dtype = Property()

    # TODO sslice
    layer = Property()

    height = Property()

    width = Property()

    channel = Property()

    shape = Property()

    currentSliceIndex = Int()

    def __init__(self, fakeData=False):

        self.meta = DataMeta()
        self.id = uuid.uuid4()
        self.currentSliceIndex = 0

        if fakeData:
            data = dsample.vol()
            s, w, h = data.shape
            data.resize((s, w, h, 1))
            self.data = data

    def astype(self, t):
        ds = ImageStack()
        ds.data = self.data.astype(t)
        return ds

    def _get_dtype(self):
        return self.data.dtype

    def _set_dtype(self, type):
        self.data.astype(type)

    def _get_shape(self):
        return self.data.shape

    def _get_layer(self):
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

    def getSlice(self, s):
        assert s > -1 and s < self.layer
        s = self.data[s, :, :, :]
        if self.channel == 1:
            s = s.squeeze(axis=2)
        return s

    def getCurrentSlice(self):
        return self.getSlice(self.currentSliceIndex)

    def updateCurrentSlice(self, sliceData):
        self.updateSlice(self.currentSliceIndex, sliceData)

    def updateSlice(self, index, sliceData):
        """
        更新一个切片的数据
        """
        shape = sliceData.shape
        assert self.layer > index > -1
        copy = sliceData
        if len(shape) == 2:
            assert self.channel == 1
            assert self.height == shape[0]
            assert self.width == shape[1]
            copy = sliceData.reshape((shape[0], shape[1], 1))
        elif len(shape) == 3:
            assert self.channel == shape[2]

        # print(copy.dtype)
        # print(self.data.dtype)
        # imagect.showImage(copy.astype(self.data.dtype))

        self.data[index] = copy.astype(self.data.dtype)
        return True

    def asSlice(self):
        """
        以(height, width, channel)的格式导出数据
        """
        assert self.layer == 1
        return self.data.reshape(self.height, self.width, self.channel)

    def asGray(self):
        """
        以(height, width)的格式导出数据
        """
        assert self.layer == 1
        assert self.channel == 1
        return self.data.reshape(self.height, self.width)

    traits_view = View(
        Group(
            Item(name="did"),
            Item(name="dtype"),
            Item(name="offset"),
            Item(name="shape"),
            Item(name="layer"),
            Item(name="height"),
            Item(name="width"),
            Item(name="channel"),
            Item(name="meta", editor=InstanceEditor(), style='custom', ),
            label="Property",
            show_border=True
        ),
        buttons=[OKButton, CancelButton],
        # statusbar = [StatusItem(name="title")],
        dock="vertical",
        title="ImageStack Property"
    )

    @staticmethod
    def fromVol(data):
        assert len(data.shape) == 3
        s, w, h = data.shape
        d = data.reshape((s, w, h, 1))
        ds = ImageStack()
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
        ds = ImageStack()
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
        ds = ImageStack()
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
            "chessboard": dsample.chessboard
        }
        if name in create:
            return ImageStack.fromVol(create[name]())
        else:
            return ImageStack.fromVol(dsample.vol())
