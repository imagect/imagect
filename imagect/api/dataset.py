
from traits.api import *
from traitsui.api import *
from traitsui.menu import OKButton, CancelButton
import numpy as np

#TODO dataset input
#TODO dataset management


def hydrogen() :
    ## Hydrogen electron probability density
    def psi(i, j, k, offset=(50,50,100)):
        x = i-offset[0]
        y = j-offset[1]
        z = k-offset[2]
        th = np.arctan2(z, (x**2+y**2)**0.5)
        phi = np.arctan2(y, x)
        r = (x**2 + y**2 + z **2)**0.5
        a0 = 2
        ps = (1./81.) * 1./(6.*np.pi)**0.5 * (1./a0)**(3/2) * (r/a0)**2 * np.exp(-r/(3*a0)) * (3 * np.cos(th)**2 - 1)
        return ps


    data = np.fromfunction(psi, (100,100,200))
    positive = np.log(np.clip(data, 0, data.max())**2)
    negative = np.log(np.clip(-data, 0, -data.min())**2)
    d2 = np.empty(data.shape + (4,), dtype=np.ubyte)
    d2[..., 0] = positive * (255./positive.max())
    d2[..., 1] = negative * (255./negative.max())
    d2[..., 2] = d2[...,1]
    d2[..., 3] = d2[..., 0]*0.3 + d2[..., 1]*0.3
    d2[..., 3] = (d2[..., 3].astype(float) / 255.) **2 * 255
    d2[:, 0, 0] = [255,0,0,100]
    d2[0, :, 0] = [0,255,0,100]
    d2[0, 0, :] = [0,0,255,100]
    d2.resize((100, 100, 200, 1))
    return d2

def vol() :
    x1 = np.linspace(-30, 10, 128)[:, np.newaxis, np.newaxis]
    x2 = np.linspace(-20, 20, 128)[:, np.newaxis, np.newaxis]
    y = np.linspace(-30, 10, 128)[np.newaxis, :, np.newaxis]
    z = np.linspace(-20, 20, 128)[np.newaxis, np.newaxis, :]
    d1 = np.sqrt(x1**2 + y**2 + z**2)
    d2 = 2*np.sqrt(x1[::-1]**2 + y**2 + z**2)
    d3 = 4*np.sqrt(x2**2 + y[:,::-1]**2 + z**2)
    data = (np.sin(d1) / d1**2) + (np.sin(d2) / d2**2) + (np.sin(d3) / d3**2)    
    z, y, x = data.shape
    data.resize((z,y,x,1))
    return data

class RawDataSet(HasTraits):

    """
    DataSet
    """
    id = UUID()

    dtype = Property()

    stack = Property()

    height = Property()

    width = Property()

    channel = Property()

    shape = Property()
    
    data = Instance(np.ndarray, transient=True)

    def __init__(self, fakedata=False) :

        if fakedata :
            self.data = vol()    

    def _get_dtype(self):
        return self.data.dtype   

    def _get_shape(self):
        return self.data.shape 

    def _get_stack(self) :
        shape = self.data.shape
        assert len(shape) == 4
        return shape[0]

    def _get_height(self) :
        shape = self.data.shape
        assert len(shape) == 4
        return shape[1]

    def _get_width(self) :
        shape = self.data.shape
        assert len(shape) == 4
        return shape[2]

    def _get_channel(self) :
        shape = self.data.shape
        assert len(shape) == 4
        assert shape[3]==1 or shape[3]==3 or shape[3]==4
        return shape[3]  

    def getStack(self, s) :
        assert s > -1 and s < self.stack
        s = self.data[s, :, :, :]
        if self.channel == 1 :
            s=s.squeeze(axis=2)
        return s

    traits_view = View(
            VGroup(
                Item(name="id"),
                Item(name="dtype"),
                Item(name="shape"),
                Item(name="stack"),
                Item(name="height"),
                Item(name="width"),
                Item(name="channel"),
                label="DataSet Property",
                show_border=True
            ),            
            buttons = [OKButton, CancelButton],
            #statusbar = [StatusItem(name="title")],
            dock = "vertical",
            title = "Dataset Property"
    )

if __name__ == "__main__":
    ds = RawDataSet(fakedata=True)
    ds.configure_traits(kind="live")