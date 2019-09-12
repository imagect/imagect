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


    ds = This(transient=True)

    either = Either(Str, None)

    possible_stock_states = List([None, 0, 1, 2, 3, "Many"])

    stock = Enum(None, values="possible_stock_states")
    

    traits_view = View(
            VGroup(
                Item(name="width"),
                Item(name="height"),
                Item(name="offset"),
                Item(name="margin"),
                label="DataSet Property",
                show_border=True
            ), 
            VGroup(
                Item(name="ds"),
                Item(name="either"),
                Item(name="possible_stock_states"),
                Item(name="stock")
            ),        
            buttons = [OKButton, CancelButton],
            #statusbar = [StatusItem(name="title")],
            dock = "vertical",
            title = "Dataset Property"
    )

def showUi() :
    ds = RawDataSet()
    ds.configure_traits(kind="live")
    print(ds)


# add to menu
from imagect.api.actmgr import addActFun, renameAct
addActFun("help.example.traits", "Truits", index =1)(showUi)
renameAct("help.example", "Example")

if __name__ == "__main__":
    showUi()
