# qt

## signal and slots

```python
    def setupMenus(self) :
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")

        show = fileMenu.addAction("Show")

        def showMsg() :
            app.get().showMsg("title", "hello")
        show.triggered.connect(showMsg)
```

## rxqt

## icon

图标放于 imagect/resource目录中

icon = imagect.icon("console.png")