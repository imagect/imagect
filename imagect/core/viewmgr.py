import imagect.api.viewmgr
from imagect.api.dataset import DataSet
from imagect.api.viewmgr import IImagePlusMgr, Viewer, ImagePlus
from zope import interface
from . import view
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from traits.api import HasTraits, List, Instance, UUID, Property
from traitsui.api import View, Item, OKButton, CancelButton, InstanceEditor
import numpy as np

pg.setConfigOptions(imageAxisOrder="row-major")


@interface.implementer(IImagePlusMgr)
class ImagePlusMgr(HasTraits):
    current_iid = Property()
    current_vid = Property()
    current_view = Instance(Viewer)

    traits_view = View(
        Item(name="sess"),
        buttons=[OKButton, CancelButton],
        # statusbar = [StatusItem(name="title")],
        dock="vertical",
        title="ImagePlus"
    )

    class EventEator(QtCore.QObject):
        def eventFilter(self, obj, evnt):
            if isinstance(evnt, (QtGui.QFocusEvent, QtGui.QCloseEvent)):
                t = self.target(obj)
                if t is not None:
                    if isinstance(evnt, QtGui.QCloseEvent):
                        imagect.api.viewmgr.get().closeView(t.iid, t.vid)

                    if isinstance(evnt, QtGui.QFocusEvent):
                        if evnt.gotFocus():
                            imagect.api.viewmgr.get().resetCurrentView(t)

            return super().eventFilter(obj, evnt)

        def target(self, obj):
            if not isinstance(obj, QtGui.QWidget):
                return None

            pw = obj
            while pw is not None:
                if isinstance(pw, Viewer):
                    return pw
                pw = pw.parentWidget()
            return None

    def __init__(self):
        super().__init__()
        self.sess = []
        self.eator = ImagePlusMgr.EventEator()
        QtGui.QGuiApplication.instance().installEventFilter(self.eator)

    def createImagePlus(self, ds):

        s = ImagePlus()
        s.updateStack(ds)

        # todo : create other view according to ds.meta
        if ds.layer == 1:
            v = view.VolViewer()
            v.setImageData(ds)
            s.insert(v)
            return (s, v)
        elif ds.layer > 1:
            v = view.VolViewer()
            v.setImageData(ds)
            s.insert(v)
            return (s, v)

    def insertVolImagePlus(self, ds):
        s, v = self.createImagePlus(ds)
        v.show()
        self.insert(s)

    def _get_current_iid(self):
        return self.current_view.iid if self.current_view else None

    def _get_current_vid(self):
        return self.current_view.vid if self.current_view else None

    def setCurrent(self, iid, vid):
        s = self.getImagePlus(iid)
        v = self.getView(iid, vid)
        self.resetCurrentView(v)

    def getCurrent(self):
        """
        return (iid, vid)
        """
        return (self.current_iid, self.current_vid)

    def currentView(self):
        return self.current_view

    def currentImagePlus(self):
        return self.getImagePlus(self.current_iid)

    def resetCurrentView(self, v):
        """
        用户界面操作，点击后重置当前窗口，根据当前窗口更新界面显示信息
        """
        self.current_view = v
        if v:
            print("current view ={}".format(v.vid))

    def closeView(self, iid, vid):
        s = self.getImagePlus(iid)
        if not s:
            return

        if s:
            s.remove(vid)
        if len(s.views) == 0:
            index = 0
            while index < len(self.sess):
                if self.sess[index].iid == iid:
                    del (self.sess[index])
                    print("remove image plus iid = {}".format(iid))
                index += 1

    def insert(self, s):
        res = self.getImagePlus(s.iid)
        if res:
            return False
        else:
            self.sess.append(s)
            if len(s.views) > 0:
                v = s.views[0]
                self.current_view = v
            return True

    def getImagePlus(self, iid) -> ImagePlus:
        res = list(filter(lambda s: s.iid == iid, self.sess))
        return res[0] if len(res) == 1 else None

    def getView(self, iid, vid) -> Viewer:
        ss = list(filter(lambda s: s.iid == iid, self.sess))
        if len(ss) == 0:
            return None
        vv = list(filter(lambda v: v.vid == vid, ss[0].views))
        return vv[0] if len(vv) == 1 else None

