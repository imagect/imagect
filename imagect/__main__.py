from imagect.api.ctapp import IApp
from imagect.core.ctapp import CtApp
from imagect.api.mainwin import IMainWin
from imagect.core.mainwin import MainWin, ExitAction, TestMsgAction
from imagect.core.actmgr import ActMgr
from imagect.api.actmgr import IActMgr, addAction
from zope.component import getGlobalSiteManager

def __main__() :
    gsm = getGlobalSiteManager()

    app = CtApp([])
    gsm.registerUtility(app, IApp)

    actmgr = ActMgr()
    gsm.registerUtility(actmgr, IActMgr)

    win = MainWin()
    gsm.registerUtility(win, IMainWin)


    win.show()

    menubar = win.menuBar()
    topacts = actmgr.topActions()
    for act in topacts:
        menubar.addAction(act)

    addAction(actmgr.file, ExitAction)
    addAction(actmgr.file, TestMsgAction)
    app.exec()

if __name__ == "__main__" :

    __main__()