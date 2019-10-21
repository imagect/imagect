from traits.api import *
from traitsui.api import *
import PyQt5 
from PyQt5.QtCore import QObject, QEvent, Qt
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar
from pyqtgraph import ImageView, ViewBox
from pyqtgraph import ROI, CrosshairROI, LineROI, RectROI
from typing import List
import rx
from rx import operators as ops
from rx.subject import Subject
from enum import Enum
import numpy as np

from imagect.api.dataset import DataSet
import imagect.api.dataset

class CommandCode(Enum):

    Begin = 1
    Append = 2
    Move = 3
    Remove = 4 
    End = 5
    Noop = 6

class PickerEvent(object) :

    def __init__(self) :
        self.picker = None 
        self.code = CommandCode.Noop

class Button(Enum) :

    Left = 1
    Right= 2
    MID  = 3
    No   = 4

class CmdInfo(HasTraits) :

    code = Instance(CommandCode)

    button = Instance(Button)

    x = Float()

    y = Float()    


class PickerMachine(HasTraits):

    state = Int(0)

    def toCmd(self, me) :

        info = CmdInfo()
        info.code = CommandCode.Move
        if me.button() == Qt.LeftButton :
            info.button = Button.Left  
        elif me.button() == Qt.RightButton : 
            info.button = Button.Right
            info.code  = CommandCode.End
        else :
            info.button = Button.No

        pos = me.scenePos()
        info.x = pos.x()
        info.y = pos.y()

        return info

    def button(self, me) :

        if me.button() == Qt.LeftButton :
            return Button.Left  
        else : 
            return Button.Right


    def transition(self, me : QGraphicsSceneMouseEvent) -> List[CmdInfo] :    

        return [self.toCmd(me)]
        
class Pt2Machine(PickerMachine):

    def transition(self, me : QGraphicsSceneMouseEvent) -> List[CmdInfo]  :

        cmds = []

        # if me.button() == Qt.RightButton:
            # return cmds

        if self.state == 0 :
            if me.type() == QEvent.GraphicsSceneMousePress :
                cmds.append(CmdInfo(button=self.button(me), code=CommandCode.Begin, 
                        x=me.scenePos().x(), y=me.scenePos().y()))
                cmds.append(CmdInfo(button=self.button(me), code=CommandCode.Append, 
                        x=me.scenePos().x(), y=me.scenePos().y()))
                self.state = 1
        elif self.state == 1 :        
            if me.type() == QEvent.GraphicsSceneMouseMove :
                cmds.append(CmdInfo(button=self.button(me), code=CommandCode.Move, 
                        x=me.scenePos().x(), y=me.scenePos().y()))
            elif me.type() == QEvent.GraphicsSceneMouseRelease :
                cmds.append(CmdInfo(button=self.button(me), code=CommandCode.End, 
                        x=me.scenePos().x(), y=me.scenePos().y()))
                self.state = 0
        else :
            pass

        if len(cmds) > 0 :
            print(cmds)
        return cmds


class Picker(QObject):

    """
    filter scene event
    """

    def __init__(self) :
        QObject.__init__(self)
        self.machine = PickerMachine()
        self.mouse_cmd = Subject()
        self.mouse_ev = Subject()
        self.subpicker_ev = Subject()
        self.target = None

    def listenTo(self, scene):
        self.target  = scene
        scene.installEventFilter(self)
        
        self.cross = CrosshairROI()
        self.cross.setSize(10)
        scene.addItem(self.cross)

        def on_next(cmd) :
            self.cross.setPos((cmd.x, cmd.y))
            pass

        self.mouse_cmd.subscribe(on_next)

    def onMouseEvent(self, me : QEvent) :

        cmds = self.machine.transition(me)

        # print("mouse event")
        self.mouse_ev.on_next(me)

        # print("mouse cmd")
        for cmd in cmds :
            self.mouse_cmd.on_next(cmd)



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

class RectPicker(object) :

    def __init__(self):
        self.machine = Pt2Machine()

    def start(self, picker, scene, parent) :
        self.source = picker
        self.dis = picker.mouse_ev.pipe(
            ops.flat_map(self.machine.transition)
            ).subscribe(self)
        self.scene = scene
        self.parent = parent

    def stop(self) :
        
        if self.dis :
            pe = PickerEvent()
            pe.picker = self 
            pe.code = CommandCode.End
            self.source.subpicker_ev.on_next(pe)
            self.dis.dispose()
            self.dis = None             
            self.drawer = None

    def on_next(self, info) :

        if info.code == CommandCode.Begin :
            self.drawer = LineROI([0, 0], [0.1, 0], 1.0, 
                parent = self.parent, 
                translateSnap=True, 
                # rotatable=False, 
                removable=True
                )
            self.drawer.setZValue(100.0)
            self.scene.addItem(self.drawer)
            o = self.parent.mapFromScene(info.x, info.y)
            self.drawer.setPos(o)
            self.drawer.setSize((0.01,0))
        
        else :
            if info.code == CommandCode.Append or info.code == CommandCode.Move :
                pos = self.drawer.pos()
                o = self.parent.mapFromScene(info.x, info.y)
                dx = o.x() - pos.x()
                dy = o.y() - pos.y()
                self.drawer.setSize((dx,dy))

            elif info.code == CommandCode.End :
                self.on_completed()
    
    def on_completed(self):
        self.stop()

    def on_error(self):
        pass