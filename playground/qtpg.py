

import os.path
import sys
import qtpy

imagect_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(imagect_dir, "../deps/pyqtgraph"))
sys.path.append(os.path.join(imagect_dir, "../imagect/qtools"))

# from ..deps.pyqtgraph import pyqtgraph as pg
# from ..imagect.qttools import app
import numpy as np
import app
import pyqtgraph as pg

def vol() :
    x1 = np.linspace(-30, 10, 64)[:, np.newaxis, np.newaxis]
    x2 = np.linspace(-20, 20, 64)[:, np.newaxis, np.newaxis]
    y = np.linspace(-30, 10, 128)[np.newaxis, :, np.newaxis]
    z = np.linspace(-20, 20, 256)[np.newaxis, np.newaxis, :]
    d1 = np.sqrt(x1**2 + y**2 + z**2)
    d2 = 2*np.sqrt(x1[::-1]**2 + y**2 + z**2)
    d3 = 4*np.sqrt(x2**2 + y[:,::-1]**2 + z**2)
    data = (np.sin(d1) / d1**2) + (np.sin(d2) / d2**2) + (np.sin(d3) / d3**2)
    z, y, x = data.shape
    data = data*100
    print(data.shape)
    return data


if __name__ == "__main__" :
    a = app.mkQApp()

    pg.setConfigOption("imageAxisOrder", "row-major")

    data = vol()
    imv = pg.ImageView()
    imv.show()



    imv.setImage(data, levels=[-1.0, 1.0])

    ## Set a custom color map
    colors = [
        (0, 0, 0),
        (45, 5, 61),
        (84, 42, 55),
        (150, 87, 60),
        (208, 171, 141),
        (255, 255, 255)
    ]
    cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
    imv.setColorMap(cmap)
    # pg.image(data)

    a.exec()