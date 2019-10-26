
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import imagect.core.view.picker as PK

class SliceView(pg.PlotWidget) :
    def __init__(self, parent=None, background='default', **kargs):
        super().__init__(parent=parent, background=background, **kargs)
        def fakeMouseDragEvent(self, ev=None, axis=None) :
            pass
        self.plotItem.vb.mouseDragEvent = fakeMouseDragEvent
        self.plotItem.invertY()
        # self.plotItem.showAxis("top")
        self.plotItem.hideAxis("left")
        self.plotItem.hideAxis("bottom")
        self.img = pg.ImageItem() #parent=self.plotItem)        
        self.img.setBorder(10)
        self.addItem(self.img)

        # global picker
        self.picker = PK.Picker()
        self.picker.listenTo(self.plotItem.scene())
        self.picker.subpicker_ev.subscribe(self.onNextEv)

        self.currentPicker = None
        self.pickers = []
        self.pickerActs = []

        self.rois = []

        def addPicker(cls) :
            picker = cls()
            act = QtGui.QAction(self)
            act.setIcon(QtGui.QIcon(cls.icon))
            act.setCheckable(True)

            def click(checked):
                if self.currentPicker :
                    self.currentPicker.stop()
                if checked :
                    self.currentPicker = picker 
                    self.currentPicker.start(self.picker, self.img)

            act.toggled.connect(click)
            return (picker, act)

        for cls in PK.pickers() :
            p, a = addPicker(cls) 
            self.pickers.append(p)
            self.pickerActs.append(a)
        


    def onNextEv(self, cmd):
        if cmd.code == PK.CommandCode.End :
            if self.currentPicker :
                pos = self.currentPicker.drawer.pos()
                size = self.currentPicker.drawer.size()
                p2= pos + size                
                print((pos[0], pos[1]))
                print((p2[0], p2[1]))                
                self.rois.append(self.currentPicker.drawer)
                self.currentPicker = None
                for act in self.pickerActs :
                    act.setChecked(False)
        
    
    def setImage(self, data) :
        self.img.setImage(data)