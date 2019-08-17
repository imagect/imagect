from imagect.api.ctapp import IApp
from imagect.core.ctapp import CtApp
from imagect.api.mainwin import IMainWin
from imagect.core.mainwin import MainWin, ExitAction, TestMsgAction
import imagect.core.actmgr 
import imagect.api.actmgr 
from imagect.api.actmgr import IActMgr, toQActionWithSubMenu
from zope.component import getGlobalSiteManager

def __main__() :
    gsm = getGlobalSiteManager()

    app = CtApp([])
    gsm.registerUtility(app, IApp)

    win = MainWin()
    gsm.registerUtility(win, IMainWin)

    actmgr = imagect.api.actmgr.get()

    # print(actmgr.actions)

    win.show()

    menubar = win.menuBar()
    topacts = imagect.api.actmgr.get().topActions()
    for act in topacts:
        menubar.addMenu(toQActionWithSubMenu(act, actmgr, menubar).menu())

    # addAction(actmgr.file, ExitAction)
    # addAction(actmgr.file, TestMsgAction)
    app.exec()

if __name__ == "__main__" :

    __main__()