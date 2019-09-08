from traits.api import *
from traitsui.api import *
from traitsui.menu import OKButton, CancelButton

class RawDataSet(HasTraits):

    """
    DataSet
    """

    width = Int()
    
    height = Int()

    offset = Int()

    margin = Int()

    traits_view = View(
            VGroup(
                Item(name="width"),
                Item(name="height"),
                Item(name="offset"),
                Item(name="margin"),
                label="DataSet Property",
                show_border=True
            ),            
            buttons = [OKButton, CancelButton],
            #statusbar = [StatusItem(name="title")],
            dock = "vertical",
            title = "Dataset Property"
    )

def showUi() :
    ds = RawDataSet()
    ds.configure_traits(kind="live")


# add to menu
from imagect.api.actmgr import addActFun, renameAct
addActFun("help.example.traits", "Truits", index =1)(showUi)
renameAct("help.example", "Example")

if __name__ == "__main__":
    showUi()
