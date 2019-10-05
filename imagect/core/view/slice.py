
from imagect.api.viewmgr import View
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

class SliceView(View) :

    def __init__(self):
        super().__init__()
        super().setMouseTracking(False)
        # self.setWindowIcon(QtGui.QIcon("icons/image.png"))

        # graphicsview
        self.view = pg.GraphicsLayoutWidget()
        self.view.setAspectLocked(True)
        self.view.setParent(self)
        self.setCentralWidget(self.view)

        self.plot = self.view.addPlot()
        self.img = pg.ImageItem()
        self.plot.addItem(self.img)

    def setImageData(self, data):
        self.data = data
        self.img.setImage(self.data)