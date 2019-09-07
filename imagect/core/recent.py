from zope import interface
from typing import List
import pickle
import os
import os.path
import datetime 
import pytz
from collections import namedtuple
import first

from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QObject

import imagect.api.actmgr
import imagect.api.app as app
from imagect.api.actmgr import addActFetch, addActFun, renameAct
from imagect.api.recent import IRecent
import imagect.api.recent as recent

Rec = namedtuple("Rec", ["time", "path"])

@interface.implementer(IRecent)
class Recent(object) :
    """
    recent file manager
    """
    _filename = "recent.pyz"
    _max = 10
    # Key = lambda r : r.path

    def __init__(self):
        super().__init__()
        self._files = []
        self.load()

    def load(self) :
        """
        load file list from file
        """        
        datadir = app.get().appDataDir()
        filepath = os.path.join(datadir, Recent._filename)
        if os.path.exists(filepath) :
            with open(filepath, mode="rb") as infile:
                self._files = pickle.load(infile)

    def save(self) :
        """
        save
        """
        datadir = app.get().appDataDir()
        os.makedirs(datadir, exist_ok=True)
        filepath = os.path.join(datadir, Recent._filename)
        with open(filepath, mode="wb") as outfile:
            pickle.dump(self._files, outfile, pickle.HIGHEST_PROTOCOL)

    def push(self, path : str) :
        """
        add to top a the list

        if exist in the list, remove and then push to top
        """
        path = os.path.abspath(path)
        newone = Rec(time=datetime.datetime.now(tz=pytz.utc), path = path)
        index = -1
        found = -1
        for r in self._files :
            index += 1
            if r.path == path :
                first.first(self._files, key=lambda r: r == path)
                found = index
                break

        if found >= 0:
            self._files.pop(found)

        self._files.insert(0, newone)

        if len(self._files) > Recent._max:
            self._files = self._files[:-2]

        self.save()


    def clear(self):
        """
        clear the list
        """
        self._files.clear()
        self.save()

    def getFiles(self) -> List[str] :
        """
        return a list a files
        """
        return [ r.path for r in self._files]


@addActFetch("file.recent", "Recent File", index=2)
def recentMenu(qact : QObject):
    files = recent.get().getFiles()
    return [QAction(f, qact) for f in files]

g = 0
@addActFun("help.recent.add", "Add Recent File", index =1, shortcut="F2")
def testRecent():
    global g
    filename = "file-{}".format(g)
    g += 1
    recent.get().push(filename)

@addActFun("help.recent.clear", "Clear Recent File", index =1)
def testRecent(index=0):
    recent.get().clear()

renameAct("help.recent", "Recent", index =12)