
from imagect.api.viewmgr import Viewer
from imagect.api.dataset import DataSet
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.Qt as Qt
import pyqtgraph as pg

import rx 
# from rx import operators as ops 
from rx.subject import Subject

import imagect.core.view.SliceView as sview 

class VolViewer(Viewer) :
    def __init__(self) :
        
        super().__init__()
        super().setMouseTracking(False)
        self.resize(1000, 800)

        self.view = sview.SliceView()
        self.setCentralWidget(self.view)

        self.toolBarPickers = self.addToolBar("Picker")
        for a in self.view.pickerActs :
            self.toolBarPickers.addAction(a)

        # update image data use slider
        self.sliceDataSubject = Subject()
        self.sliceDataSubject.subscribe(self.onNextSliceData)

        self.range = QtGui.QLabel(parent=self)
        self.range.setText("1/1")
        self.statusBar().addPermanentWidget(self.range)
        self.slider = QtGui.QSlider(orientation=QtCore.Qt.Horizontal, parent=self)
        self.statusBar().addPermanentWidget(self.slider, stretch=1)
        def updateImageItemFromSlider(v) :
            assert self.vol_data 
            assert v < self.vol_data.stack
            # print("slider update to slice {}".format(v))
            self.sliceDataSubject.on_next(self.vol_data.getStack(v))
            self.range.setText("{}/{}".format(v, self.vol_data.stack))
            self.vol_data.currentStackIndex = v
        self.slider.valueChanged.connect(updateImageItemFromSlider)

        # update image when dataset changed
        self.stackUpdatedHandle = None

        
    def setImageData(self, data : DataSet) :      

        if self.stackUpdatedHandle :
            self.stackUpdatedHandle.dispose()
        self.stackUpdatedHandle = data.stackUpdated.subscribe(self.setImageSliceIndex)

        self.did = data.did
        self.vol_data = data 

        # setup slider
        stack = data.stack 
        self.slider.setMinimum(0)
        self.slider.setMaximum(stack)
        if stack > 1 :
            self.statusBar().show()
        else :
            self.statusBar().hide()
        self.slider.setValue(data.currentStackIndex)
        self.range.setText("{}/{}".format(data.currentStackIndex, data.stack))

        # update image item
        self.sliceDataSubject.on_next(data.getCurrentStack())

    def setImageSliceData(self, data) :
        self.onNextSliceData(data)

    def setImageSliceIndex(self, index) :
        assert self.vol_data
        self.slider.setValue(index)
        if index == self.slider.value():
            self.sliceDataSubject.on_next(self.vol_data.getStack(index))
    
    def onNextSliceData(self, slice_data) :
        self.slice_data = slice_data 
        self.view.setImage(self.slice_data) 

if __name__ == "__main__" :
    from PyQt5.QtWidgets import QApplication
    import imagect.api.dataset as ds
    import numpy as np
    app = QApplication([])

    dm = ds.get()
    # sample = ds.DataSet.fromSample("chessboard").astype(np.float32)
    sample = ds.DataSet.fromSample("vol").astype(np.float32)
    v = VolViewer()
    v.setImageData(sample)
    v.show()

    app.exec()
