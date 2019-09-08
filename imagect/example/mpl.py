from traits.api import *
from traitsui.api import *
from traitsui.menu import OKButton, CancelButton

def exampleMPL() :
    import PyQt5 
    import PyQt5.QtWidgets as QtWidgets
    import matplotlib
    from matplotlib.figure import Figure   
    matplotlib.use("Qt5Agg")
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
    from traitsui.qt4.editor import Editor
    from traitsui.basic_editor_factory import BasicEditorFactory

    class _MPLFigureEditor(Editor) :

        scrollable = True 

        def init(self, parent) :
            """
            parent = Layout
            self.value = Figure()
            """
            
            Editor.__init__(self, parent)
            self.control = self._create_canvas(parent)
            self.set_tooltip()

        def update_editor(self) :
            pass

        def _create_canvas(self, parent) :
            mpl_control = FigureCanvas(self.value)
            # mpl_control = QtWidgets.QLabel("name")
            # parent.addWidget(mpl_control)
            return mpl_control

    class MPLFigureEditor(BasicEditorFactory):
        """
        相当于traits.ui中的EditorFactory，它返回真正创建控件的类
        """    
        klass = _MPLFigureEditor


    from numpy import sin, cos, linspace, pi

    class Test(HasTraits):
        figure = Instance(Figure, ())

        width = Int()

        height = Int()

        view = View(
            # Item(name="width", show_label=False),
            # Item(name="height", show_label=False),
            Item(name="figure", editor=MPLFigureEditor(), show_label=False),
            buttons = [OKButton, CancelButton]
            )

        def __init__(self):
            super(Test, self).__init__()
            axes = self.figure.add_subplot(111)
            t = linspace(0, 2*pi, 200)
            axes.plot(sin(t))

    # ds = DataSet()
    # ds.configure_traits(kind="live")
    Test().configure_traits()

# add to menu
from imagect.api.actmgr import addActFun, renameAct
addActFun("help.example.matplotlib", "Matplotlib", index =1)(exampleMPL)
renameAct("help.example", "Example")

if __name__ == "__main__" :
    exampleMPL()