
from imagect.api.viewmgr import Viewer
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

pg.setConfigOptions(imageAxisOrder="row-major")

class ImageView(pg.GraphicsView) :

    def __init__(self, parent=None, useOpenGL=None, background='default'):
        super().__init__(parent=parent, useOpenGL=useOpenGL, background=background)

        self.vb = pg.ViewBox()
        self.vb.setAspectLocked()
        self.setCentralItem(self.vb)
        self.img = pg.ImageItem()
        self.vb.addItem(self.img)
    
    def setImage(self, data) :
        if len(data.shape) == 2:
            h,w = data.shape
            self.resize(w,h)
        if len(data.shape) == 3:
            h,w,c = data.shape
            self.resize(w,h)
        self.img.setImage(data)
        self.vb.autoRange()
        

class ImageView2(pg.ImageView) :
    def __init__(self, parent=None, name='ImageView', imageItem=None, *args):
        
        _vb = pg.ViewBox(enableMouse=False)
        super().__init__(parent=parent, name=name, view=_vb, imageItem=imageItem, *args)
        
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.ui.graphicsView.enableMouse(False)
        self.ui.histogram.hide()

        self.imageItem.setBorder(10)

    def showHist(self) :
        self.ui.histogram.show()

class ImageView3(pg.PlotWidget) :
    def __init__(self, parent=None, background='default', **kargs):
        super().__init__(parent=parent, background=background, **kargs)
        def fakeMouseDragEvent(self, ev=None, axis=None) :
            pass
        self.plotItem.vb.mouseDragEvent = fakeMouseDragEvent
        self.plotItem.invertY()
        self.plotItem.showAxis("top")
        # self.plotItem.hideAxis("left")
        self.plotItem.hideAxis("bottom")
        self.img = pg.ImageItem() #parent=self.plotItem)        
        self.img.setBorder(10)
        self.addItem(self.img)

    
    def setImage(self, data) :        
        self.img.setImage(data)

import imagect.core.view.picker as PK
class SliceView(Viewer) :

    def __init__(self):
        super().__init__()
        super().setMouseTracking(False)
        self.resize(1000, 800)
        # self.setWindowIcon(QtGui.QIcon("icons/image.png"))

        self.view = ImageView3(self)
        self.setCentralWidget(self.view)

        self.tbar = self.addToolBar("Picker")
        self.lineAct = self.tbar.addAction("Rect")
        self.lineAct.toggled.connect(self.lineRoi)

        self.acts = [self.lineAct]
        for act in self.acts :
            act.setCheckable(True)

        self.picker = PK.Picker()
        self.picker.listenTo(self.view.plotItem.scene())
        self.picker.subpicker_ev.subscribe(self.on_picker_ev)

        self.linePicker = PK.RectPicker()
        self.currentPicker = None

        self.rois = []

    def on_picker_ev(self, cmd) :
        if cmd.code == PK.CommandCode.End :
            if self.currentPicker :
                self.rois.append(self.currentPicker.drawer)  
                # print(self.currentPicker.drawer.pos())
                pos = self.currentPicker.drawer.pos()
                size = self.currentPicker.drawer.size()
                p2= pos + size
                # for p in pos :
                print(self.view.img.mapFromScene(pos[0], pos[1]))
                print(self.view.img.mapFromScene(p2[0], p2[1]))
                
                self.rois.append(self.currentPicker.drawer)

                self.currentPicker = None

                for act in self.acts :
                    act.setChecked(False)


    def lineRoi(self, checked) :        
        """
        picker, add roi to self.imv.view
        self.imv.view.addItem(roi)
        """
        if self.currentPicker :
            self.currentPicker.stop()
            self.currentPicker = None
        
        if checked :
            self.currentPicker = self.linePicker
            self.currentPicker.start(self.picker, self.view.plotItem.scene())


    def setImageData(self, data):
        self.slice_data = data
        self.view.setImage(data)

if __name__ == "__main__" :
    from PyQt5.QtWidgets import QApplication
    import imagect.api.dataset as ds
    import numpy as np
    app = QApplication([])

    dm = ds.get()
    # sample = ds.DataSet.fromSample("chessboard").astype(np.float32)
    sample = ds.DataSet.fromSample("vol").astype(np.float32)
    v = SliceView()
    v.did = sample.did
    v.sid = sample.did 
    v.setImageData(sample.getStack(int(sample.stack/2)))
    v.show()

    app.exec()
    


