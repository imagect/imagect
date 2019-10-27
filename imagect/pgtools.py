
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg


def showImage(data) :
    imv = pg.ImageView()
    imv.setImage(data)
    imv.show()

    def handler():
        imv.show()
    imv.handler = handler
