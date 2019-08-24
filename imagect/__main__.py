from imagect.api.ctapp import IApp
from imagect.core.ctapp import CtApp
from imagect.api.mainwin import IMainWin
from imagect.core.mainwin import MainWin
import imagect.core.actmgr 
import imagect.api.actmgr 
from imagect.api.recent import IRecent
import imagect.core.recent
from imagect.api.actmgr import IActMgr, toQAction
from zope.component import getGlobalSiteManager

def __main__() :
    gsm = getGlobalSiteManager()

    app = CtApp([])
    gsm.registerUtility(app, IApp)

    win = MainWin()
    gsm.registerUtility(win, IMainWin)

    actmgr = imagect.api.actmgr.get()

    recent = imagect.core.recent.Recent()
    gsm.registerUtility(recent, IRecent)

    # print(actmgr.actions)

    win.show()

    menubar = win.menuBar()
    topacts = imagect.api.actmgr.get().topActions()
    for act in topacts:
        menubar.addMenu(toQAction(act, menubar).menu())

    app.exec()

if __name__ == "__main__" :

    __main__()