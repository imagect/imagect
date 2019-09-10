
from traits.api import *
from traitsui.api import *
import PyQt5 
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar
from pyqtgraph import ImageView, ViewBox
from pyqtgraph import ROI, CrosshairROI
from typing import List
import rx
from rx import operators as ops
from rx.subject import Subject
from enum import Enum

class CommandCode(Enum):

    Begin = 1
    Append = 2
    Move = 3
    Remove = 4 
    End = 5

class Button(Enum) :

    Left = 1
    Right= 2
    MID  = 3

class CmdInfo(HasTraits) :

    code = Instance(CommandCode)

    button = Instance(Button)

    x = Float()

    y = Float()


class PickerMachine(HasTraits):

    state = Int()

    def toCmd(self, me) :

        info = CmdInfo()
        info.code = CommandCode.Move
        if me.button() == Button.Left :
            info.mouse = Button.Left  
        else : 
            info.mouse = Button.Right
        pos = me.scenePos()
        info.x = pos.x()
        info.y = pos.y()

        return info


    def transition(self, me : QGraphicsSceneMouseEvent) -> List[int] :    

        return [self.toCmd(me)]
        

class Picker(QObject):

    """
    filter scene event
    """

    def __init__(self) :
        QObject.__init__(self)
        self.machine = PickerMachine()
        self.mousecmd = Subject()
        self.target = None
        self.cross = CrosshairROI()
        self.cross.setSize(10)

    def listenTo(self, scene):
        self.target  = scene
        scene.installEventFilter(self)
        # self.cross.set
        scene.addItem(self.cross)

        def on_next(cmd) :
            self.cross.setPos((cmd.x, cmd.y))

        self.mousecmd.subscribe(on_next)

    def onMouseEvent(self, me : QEvent) :

        cmds = self.machine.transition(me)

        for cmd in cmds :
            self.mousecmd.on_next(cmd)

    def eventFilter(self, watched, event) :

        if self.target is watched and event.type() in [
            QEvent.GraphicsSceneHoverEnter,
            QEvent.GraphicsSceneHoverLeave,
            QEvent.GraphicsSceneHoverMove,
            QEvent.GraphicsSceneMouseDoubleClick,
            QEvent.GraphicsSceneMouseMove,
            QEvent.GraphicsSceneMousePress,
            QEvent.GraphicsSceneMouseRelease ] :
            self.onMouseEvent(event)

        return False

class MainWin(QMainWindow):

    picker = Picker()

    rois = Instance(list)

    def __init__(self):

        QMainWindow.__init__(self)

        self.tbar = self.addToolBar("Picker")

        self.linePicker = self.tbar.addAction("Line")

        self.rectPicker = self.tbar.addAction("Rect")

        self.lineSegPicker = self.tbar.addAction("Seg")

        self.acts = [self.linePicker, self.rectPicker, self.linePicker]

        for act in self.acts :
            act.setCheckable(True)

        self.vb = ViewBox(enableMouse=False)

        self.imv = ImageView(self, view = self.vb)
        self.picker.listenTo(self.imv.scene)

        from matplotlib.image import imread
        import os.path 
        self.data = imread(os.path.join(os.path.dirname(__file__), "ct.png"))
        self.imv.setImage(self.data)

        self.setCentralWidget(self.imv)


    def lineRoi(self) :
        
        """
        picker, add roi to self.imv.view
        self.imv.view.addItem(roi)
        """
        pass


if __name__ == "__main__" :

    app = QApplication([])

    win = MainWin()

    win.resize(1000, 800)

    win.show()

    app.exec()