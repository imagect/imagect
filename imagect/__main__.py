from imagect.api.app import IApp
from imagect.core.app import App
from imagect.api.mainwin import IMainWin
from imagect.core.mainwin import MainWin
from imagect.api.console import IConsole
import imagect.core.console
import imagect.api.actmgr 
from imagect.api.recent import IRecent
import imagect.core.recent
from imagect.api.actmgr import IActMgr, toQAction
import imagect.core.opener.image
import imagect.core.opener.opener
from zope.component import getGlobalSiteManager

import imagect.example

def __main__() :
    gsm = getGlobalSiteManager()

    application = App([])
    gsm.registerUtility(application, IApp)

    win = MainWin()
    gsm.registerUtility(win, IMainWin)

    actmgr = imagect.api.actmgr.get()

    recent = imagect.core.recent.Recent()
    gsm.registerUtility(recent, IRecent)

    console = imagect.core.console.Console()
    gsm.registerUtility(console, IConsole)

    win.show()

    menubar = win.menuBar()
    topacts = imagect.api.actmgr.get().topActions()
    for act in topacts:
        menubar.addMenu(toQAction(act, menubar).menu())

    console.execute("import imagect.api.util as iu")

    application.exec()

if __name__ == "__main__" :

    __main__()