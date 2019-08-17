# qt

## signal and slots

```python
    def setupMenus(self) :
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")

        show = fileMenu.addAction("Show")

        def showMsg() :
            ctapp.get().showMsg("title", "hello")
        show.triggered.connect(showMsg)
```

## rxqt