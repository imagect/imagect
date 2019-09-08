
import rx
from rx import operators as ops
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class Window(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Rx for Python rocks")
        self.resize(600, 600)
        self.setMouseTracking(True)

        # This Subject is used to transmit mouse moves to labels
        self.mousemove = Subject()

        text = 'TIME FLIES LIKE AN ARROW'

        def on_next(info):
            label, (x, y), i = info
            label.move(x + i*12 + 15, y)
            label.show()

        def handle_label(label, i):
            delayer = ops.delay(i * 0.100)
            mapper = ops.map(lambda xy: (label, xy, i))

            return self.mousemove.pipe(
                delayer,
                mapper,
            )

        labeler = ops.flat_map_indexed(handle_label)
        mapper = ops.map(lambda c: QLabel(c, self))

        from imagect.api.app import get
        rx.from_(text).pipe(
            mapper,
            labeler,
        ).subscribe(on_next, on_error=print, scheduler=get().rx_scheduler())

    def mouseMoveEvent(self, event):
        self.mousemove.on_next((event.x(), event.y()))

# add to menu
from imagect.api.actmgr import addActFun, renameAct
@addActFun("help.example.rxqt", "Rx", index =1, shortcut="F6") 
def showui():
    w = Window()
    w.show()

renameAct("help.example", "Example")
