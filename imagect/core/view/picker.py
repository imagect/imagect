from traits.api import *
from traitsui.api import *

import PyQt5 
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import QObject, QEvent, Qt, QPointF
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar

import pyqtgraph as pg
from pyqtgraph import ImageView, ViewBox
from pyqtgraph import ROI, CrosshairROI

from typing import List

import rx
from rx import operators as ops
from rx.subject import Subject

from enum import Enum
import numpy as np

from imagect.api.dataset import DataSet
import imagect.api.dataset

import imagect

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

        # if len(cmds) > 0 :
            # print(cmds)
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
        
        # self.cross = CrosshairROI()
        # self.cross.setSize(10)
        # scene.addItem(self.cross)

        def on_next(cmd) :
            # self.cross.setPos((cmd.x, cmd.y))
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

_pickerKlass = {}

def register(cls) :
    global _pickerKlass
    _pickerKlass[cls.__name__] = cls
    return cls


def pickers():
    return _pickerKlass.values()

class RectROI(pg.ROI):
    r"""
    Rectangular ROI subclass with a single scale handle at the top-right corner.

    ============== =============================================================
    **Arguments**
    pos            (length-2 sequence) The position of the ROI origin.
                   See ROI().
    size           (length-2 sequence) The size of the ROI. See ROI().
    centered       (bool) If True, scale handles affect the ROI relative to its
                   center, rather than its origin.
    sideScalers    (bool) If True, extra scale handles are added at the top and 
                   right edges.
    \**args        All extra keyword arguments are passed to ROI()
    ============== =============================================================
    
    """
    def __init__(self, pos, size, **args):
        pg.ROI.__init__(self, pos, size, **args)            
        #self.addScaleHandle([1, 1], center)

@register
class RectPicker(object) :

    icon = imagect.icon("picker_rect.png")

    def __init__(self):
        self.machine = Pt2Machine()

    def start(self, gPicker, target) :
        self.source = gPicker
        self.dis = gPicker.mouse_ev.pipe(
            ops.flat_map(self.machine.transition)
            ).subscribe(self)
            
        self.parentItem = target

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

        o = self.parentItem.mapFromScene(info.x, info.y)

        if info.code == CommandCode.Begin :
            self.pts_start = o
            self.drawer = RectROI(self.pts_start, [0, 0], 
                parent = self.parentItem, 
                translateSnap=True, 
                # rotatable=False, 
                movable = False,
                removable=True,
                # sideScalers=True,
                # centered=False,
                pen = pg.mkPen(200,200,200,width=20)
                )
            self.drawer.setZValue(100.0)
            self.drawer.setPos(self.pts_start)
       
        else :
            if info.code == CommandCode.Append or info.code == CommandCode.Move :
                
                minx = min(o.x(), self.pts_start.x())
                miny = min(o.y(), self.pts_start.y())
                maxx = max(o.x(), self.pts_start.x())
                maxy = max(o.y(), self.pts_start.y())

                rect_start = QPointF(minx, miny)
                self.drawer.setPos(rect_start)
                self.drawer.setSize((maxx-minx,maxy-miny))

            elif info.code == CommandCode.End :
                self.on_completed()



    def on_completed(self):
        self.drawer.translatable = True
        center = [0, 0]
        self.drawer.addScaleHandle([1, 0.5], [center[0], 0.5])
        self.drawer.addScaleHandle([0.5, 1], [0.5, center[1]])

        self.stop()

    def on_error(self):
        pass



@register
class LinePicker(object) :

    icon = imagect.icon("picker_line.png")

    def __init__(self):
        self.machine = Pt2Machine()

    def start(self, gPicker, target) :
        self.source = gPicker
        self.dis = gPicker.mouse_ev.pipe(
            ops.flat_map(self.machine.transition)
            ).subscribe(self)
            
        self.parentItem = target

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
        o = self.parentItem.mapFromScene(info.x, info.y)
        if info.code == CommandCode.Begin :
            self.pts_start = o
            self.drawer = RectROI(self.pts_start, [0, 0], 
                parent = self.parentItem, 
                translateSnap=True, 
                movable = False,
                removable=True,
                
                pen = pg.mkPen(200,200,200,width=20)
                )
            self.drawer.setZValue(100.0)
            self.drawer.setPos(self.pts_start)
       
        else :
            if info.code == CommandCode.Append or info.code == CommandCode.Move :
                
                minx = min(o.x(), self.pts_start.x())
                miny = min(o.y(), self.pts_start.y())
                maxx = max(o.x(), self.pts_start.x())
                maxy = max(o.y(), self.pts_start.y())

                rect_start = QPointF(minx, miny)
                self.drawer.setPos(rect_start)
                self.drawer.setSize((maxx-minx,maxy-miny))

            elif info.code == CommandCode.End :
                self.on_completed()

    def on_completed(self):
        self.drawer.translatable = True
        center = [0, 0]
        self.drawer.addScaleHandle([1, 0.5], [center[0], 0.5])
        self.drawer.addScaleHandle([0.5, 1], [0.5, center[1]])

        self.stop()

    def on_error(self):
        pass


