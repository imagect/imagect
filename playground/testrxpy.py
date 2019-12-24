import qtpy
import qtpy.QtCore
from qtpy.QtCore import QThread
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QMainWindow, QLabel, QToolBar, QPushButton
import sys

import rx
from rx import Observable
from rx.scheduler import ThreadPoolScheduler
from rx import operators as ops
from rx.scheduler.mainloop import QtScheduler

app = QApplication(sys.argv)

win = QMainWindow()

win.show()

toolbar = win.addToolBar("file")

btn = QPushButton("ADD", toolbar)
toolbar.addWidget(btn)

gui_scheduler = QtScheduler(qtpy.QtCore)

thread_pool_scheduler = ThreadPoolScheduler()

def printThreadId():
    print("Thread {}".format(QThread.currentThreadId()))

def addLabel():
    label = QLabel("Label", toolbar)
    toolbar.addWidget(label)

def onClicked():
    printThreadId()
    xs = rx.from_([1,2,3,4,5])

    def add(x) :
        printThreadId()
        addLabel()
        return x
    
    xs.pipe(
        ops.observe_on(thread_pool_scheduler),
        ops.observe_on(gui_scheduler),
        ops.map(add),
        #ops.observe_on(thread_pool_scheduler),
        ops.map(lambda x: 2 * x)
    ).subscribe(print)


btn.clicked.connect(onClicked)

addLabel()

app.exec()
