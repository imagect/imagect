from zope.interface import implementer
from zope.component import getGlobalSiteManager
from collections import defaultdict
from traits.api import *
from traitsui.api import *
from traitsui.menu import OKButton, CancelButton
import numpy as np
import imagect.api.datasample as dsample
from zope.interface import Interface
from zope.component import getUtility
import uuid
from rx.subject import Subject
from imagect.ic import ImageStack, DataMeta

# TODO dataset input
# TODO dataset management
# TODO add datameta for dataset, describe source and reader

sampleId = "784c59df-acb8-4d4e-b2e5-fa926264c79e"


DataMeta = DataMeta

DataSet = ImageStack


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


def sample():
    mgr = get()
    data = mgr.get(sampleId)
    if data is None:
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
    # ds.meta = DataMeta()
    ds.configure_traits()
