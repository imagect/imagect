# imagect

see [document](./doc/source/contents.md), or [readthedocs](https://imagect.readthedocs.io/en/latest/)


pip uninstall pyqtgraph

PYTHONPATH : ${workspaceFolder}:${workspaceFolder}/3rd/pyqtgraph:${PYTHONPATH}

# 2020.1.4

[]软件名：ImageProspector

[]去掉zope库依赖。是不是只用到了getUtility函数?

[]自定义Trait类型，实现数据范围的限制

[]通过“配置信息”自动生成界面，而不是手动写界面代码

# todo

[] 第三方模块加载，第三方模块放在extern中，每个目录为一组独立的插件，动态加载

[] 增加对ROI数据的支持

[] 使用awesome font做为软件的图标 参考 https://github.com/gamecreature/QtAwesome

[] 设置环境变量，指定测试文件位置，然后用快捷键读入数据

[] 设置环境变量,指定是否后台进程运行算法

[] 三维数据显示翻页

[] python PEP 编码规范

[] 增加图标，画在工具栏上

[] 增加显示三维示例数据的选项

[] 优化打开三维数据的界面