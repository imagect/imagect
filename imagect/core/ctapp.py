
from imagect.api.ctapp import IApp
from zope import interface 
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5 import QtCore
from asyncqt import QEventLoop, QThreadExecutor
import asyncio
from rx.scheduler.mainloop import QtScheduler

@interface.implementer(IApp)
class CtApp(QApplication):

    """
    application
    """

    def __init__(self, argv):
        super().__init__(argv)

        self.loop = QEventLoop(self)
        asyncio.set_event_loop(self.loop)

        self.scheduler = QtScheduler(QtCore)
        
    def asyncio_loop(self):
        return self.loop

    def rx_scheduler(self):
        return self.scheduler

    def showMsg(self, title : str, msg : str):
        """
        show message box
        """
        QMessageBox.information(None, title, msg)
        pass


if __name__ == "__main__" :

    from PyQt5.QtWidgets import QProgressBar, QWidget, QLabel
    import rx
    from rx import operators as ops
    from rx.subject import Subject
    import time
    import sys

    class Window(QWidget):

        def __init__(self):
            QWidget.__init__(self)
            self.setWindowTitle("Rx for Python rocks")
            self.resize(600, 600)
            self.setMouseTracking(True)
    
            # This Subject is used to transmit mouse moves to labels
            self.mousemove = Subject()
    
        def mouseMoveEvent(self, event):
            self.mousemove.on_next((event.x(), event.y()))

    def showProgress(loop):

        progress = QProgressBar()
        progress.setRange(0, 99)
        progress.show()
    
        close = loop.create_future()
    
        async def master():
            await first_50()
            with QThreadExecutor(1) as exec:
                await loop.run_in_executor(exec, last_50)
            # TODO announce completion?
            await close
    
        async def first_50():
            for i in range(50):
                progress.setValue(i)
                await asyncio.sleep(.1)
    
    
        def last_50():
            for i in range(50, 100):
                loop.call_soon_threadsafe(progress.setValue, i)
                time.sleep(.1)
    
        # asyncio.run_coroutine_threadsafe(master(), loop)
        task = loop.create_task(master())
    
        def cancel() :
            close.set_result(0)

    app = CtApp([])

    window = Window()
    window.show()

    showProgress(app.asyncio_loop())

    text = 'TIME FLIES LIKE AN ARROW'

    def on_next(info):
        label, (x, y), i = info
        label.move(x + i*12 + 15, y)
        label.show()

    def handle_label(label, i):
        delayer = ops.delay(i * 0.100)
        mapper = ops.map(lambda xy: (label, xy, i))

        return window.mousemove.pipe(
            delayer,
            mapper,
        )

    labeler = ops.flat_map_indexed(handle_label)
    mapper = ops.map(lambda c: QLabel(c, window))

    rx.from_(text).pipe(
        mapper,
        labeler,
    ).subscribe(on_next, on_error=print, scheduler=app.rx_scheduler())

    sys.exit(app.exec_())