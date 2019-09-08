# Action Manager

## Intr

method to add a new menu item

### method 1

```python
import imagect.api.actmgr
from imagect.api.actmgr import addAct, addActFun, renameAct

@addActFun("file.exampe.msg", text="&Message", index=1, shortcut="F5")
def apptest():
    win = get()
    win.showMessage("Test Message")
```

### method 2

```python
from imagect.api.actmgr import addActFetch, renameAct
@addActFetch("file.recent", "Recent File", index=2)
def recentMenu(qact : QAction):
    return [ QAction("Recent 1", qact), QAction("Recent 2", qact)]
```

### method 3

```python
import imagect.api.actmgr
from imagect.api.actmgr import addActWdg, renameAct

@addActWdg("file.exampe.wdg", text="Show Widget", index = 3)
class ActWdg(QSpinBox) :
    def __init__(self, parent):
        super().__init__(parent) 
```

## API

```eval_rst
.. automodule:: imagect.api.actmgr
   :members:
   :undoc-members:
   :show-inheritance:
```

