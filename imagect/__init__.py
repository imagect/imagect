
import os
import os.path

from PyQt5.QtGui import QIcon

imagect_dir = os.path.dirname(__file__)
resource_dir = os.path.abspath(os.path.join(imagect_dir, "resource"))
icon_dir = os.path.abspath(os.path.join(imagect_dir, "resource/icon"))

def icon(filename):
    return QIcon(os.path.join(icon_dir, filename))



from . import pgtools
showImage = pgtools.showImage