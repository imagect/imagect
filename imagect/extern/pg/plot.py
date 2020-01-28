from imagect.plugin.filter_plugin import PlugInFlag, SliceFilterPlugin
from imagect.plugin.filter_plugin_runner import register_filter
import imagect

@register_filter
class PgPlotPlugin(SliceFilterPlugin):
    id = "help.demo.PgPlot"
    title = "PgPlot"
    index = 0
    icon = imagect.icon("console.png")
    shortcut = "Ctrl+K, Ctrl+L"

    def __init__(self):
        super().__init__()

    def setup(self, arg, imp):

        if not imp:
            return PlugInFlag.NOTHING, None

        import pyqtgraph as pg
        pg.image(imp.data.data)
        pg.stack()

        return PlugInFlag.NOTHING, None

