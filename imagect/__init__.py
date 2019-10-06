
import os
import os.path

from PyQt5.QtGui import QIcon

imagect_dir = os.path.dirname(__file__)
resource_dir = os.path.abspath(os.path.join(imagect_dir, "resource"))

def icon(filename):
    return QIcon(os.path.join(resource_dir, filename))