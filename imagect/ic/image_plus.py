from rx.subject import Subject
from traits.api import UUID, Bool, Instance, Property, HasTraits
from .image_stack import ImageStack
from threading import RLock
import uuid


class ImagePlus(HasTraits):
    """
    wrapper for image stack
        event
        update
        read
        view
        roi //todo
    """

    iid = UUID(can_init=True)

    did = Property()

    locked = Bool()

    sub_stack_updated = Instance(Subject)

    sub_slice_updated = Instance(Subject)

    data = Instance(ImageStack)

    def __init__(self):
        self.iid = uuid.uuid4()
        self.locked = False
        self.sub_slice_updated = Subject()
        self.sub_stack_updated = Subject()
        self.views = []
        self.data_lock = RLock()

    def _get_did(self):
        return self.data.did

    def getStack(self):
        return self.data

    def getSlice(self, index):
        return self.data.getSlice(index)

    def getCurrentSlice(self):
        return self.data.getCurrentSlice()

    def getCurrentSliceIndex(self):
        return self.data.currentSliceIndex

    def updateStack(self, stack):
        with self.data_lock:
            self.data = stack
            self.iid = stack.did
            self.sub_stack_updated.on_next(self.data)
            self.sub_slice_updated.on_next((self.data.currentSliceIndex,
                                            self.data.getCurrentSlice()))

    def updateCurrentSlice(self, sslice):
        with self.data_lock:
            self.updateSlice(self.data.currentSliceIndex, sslice)

    def updateSlice(self, index, sslice):
        with self.data_lock:
            if self.data.updateSlice(index, sslice):
                self.sub_slice_updated.on_next((index, sslice))

    def remove(self, vid):
        with self.data_lock:
            index = 0
            while index < len(self.views):
                if self.views[index].vid == vid:
                    v = self.views[index]
                    if hasattr(v, "sliceUpdatedHandle"):
                        v.sliceUpdatedHandle.dispose()
                    else:
                        assert False
                    del (self.views[index])
                    print("remove viewer vid={}".format(vid))
                index += 1

    def insert(self, v):
        with self.data_lock:
            vs = list(filter(lambda o: o.vid == v.vid, self.views))
            v.iid = self.iid
            assert v.did == self.did
            if len(vs) == 0:
                self.views.append(v)

            if hasattr(v, "setImageSliceIndex"):
                def update(tdata):
                    index, sslice = tdata
                    v.setImageSliceIndex(index)
                v.sliceUpdatedHandle = self.sub_slice_updated.subscribe(update)
            else:
                assert False

    def getRoi(self):
        """
        todo
        :return: roi
        """
        pass
