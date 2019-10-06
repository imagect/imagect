
# traits & traitsui

* 模态对话框
参见例子 imagect.core.opener.vol
``` python
pro = RawVolMeta()
pro.configure_traits(kind="modal")
```

* 输入文件路径
界面上要指定dialog_style="open", 与输出文件区别
``` python
path = File("E:/CloudData/lizong_640_640_800_uint16_0Head.raw.raw")

    trait_view = View(
        Item(name="path", editor=FileEditor(dialog_style = "open")),
        Item(name="stack"),
        Item(name="height"),
        Item(name="width"),
        Item(name="dtype"),
        buttons=[OKButton, CancelButton],
        dock="vertical",
        title="Raw Data Property"
    )
```