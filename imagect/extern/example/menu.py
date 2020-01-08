from imagect.api.actmgr import IAction, register_action, addActFun, renameAct
import imagect.api.app as app
import imagect

"""
两种方法等价
"""

"""
method 1
"""


@register_action
class ExitMenuItem(IAction):

    def __init__(self):
        super().__init__()
        self.id = "help.demo.exit"
        self.pid = "help.demo"
        self.title = "Exit1"
        self.index = 2
        self.icon = imagect.icon("console.png")
        self.callable = self.cb

    def cb(self):
        app.getQtApp().exit()


"""
method 2
"""


@addActFun("help.demo.exit2", text="Exit2", index=1, icon=imagect.icon("console.png"))
def appexit():
    app.getQtApp().exit()


"""
前面的代码增加了一个二级菜单，该二级菜单需要重命名
"""
renameAct("help.demo", "Demo")
