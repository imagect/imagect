
from imagect.api.viewmgr import Viewer
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

import rx 
from rx import operators as ops 
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

        
    def setImageData(self, data) :
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
    v = VolViewer()
    v.did = sample.did
    v.sid = sample.did 
    v.setImageData(sample.getStack(int(sample.stack/2)))
    v.show()

    app.exec()
