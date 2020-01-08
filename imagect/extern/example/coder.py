
"""
Implementation of a CodeEditor demo plugin for Traits UI demo program.
This demo shows each of the four styles of the CodeEditor
"""

# Imports:
from __future__ import absolute_import
from traits.api \
    import HasTraits, Code, ToolbarButton

from traitsui.api \
    import Item, Group, View, HGroup, VGroup

# The main demo class:


class CodeEditorDemo(HasTraits):
    """ Defines the CodeEditor demo class.
    """

    run = ToolbarButton()

    def _run_fired(self) :
        import imagect.api.util as iu 
        iu.console.execute(self.code_sample)


    toolbar = Group(
        Item("run", show_label=False)
    )

    # Define a trait to view:
    code_sample = Code(
        """%matplotlib
import imagect.api.util as iu
from matplotlib import pyplot as plt
import numpy as np
X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)
plt.plot(X, C)
plt.plot(X, S)
plt.show()
""")

    # Display specification:
    code_group = Group(
        Item('code_sample', style='custom', label='Custom', show_label=False),
    )

    # Demo view:
    view = View(
        VGroup(toolbar, code_group),
        title='CodeEditor',
        buttons=['OK'])

def showCoder() :
    # Create the demo:
    demo = CodeEditorDemo()
    demo.configure_traits()

# add to menu
from imagect.api.actmgr import addActFun, renameAct
addActFun("help.example.coder", "Coder", index =1, shortcut="F5")(showCoder)
renameAct("help.example", "Example")

if __name__ == "__main__" :
    showCoder()