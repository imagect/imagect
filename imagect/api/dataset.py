
from traits.api import *
from traitsui.api import *
from traitsui.menu import OKButton, CancelButton


class ImageType : 
    "data type"


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

if __name__ == "__main__":
    ds = RawDataSet()
    ds.configure_traits(kind="live")