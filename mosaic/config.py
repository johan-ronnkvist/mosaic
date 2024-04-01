from mosaic import widgets
from mosaic.core.builder import Builder, LazyInit


def populate_builder(builder: Builder):
    builder.register(widgets.MainMenu, instance=LazyInit)
    builder.register(widgets.StatusBar, instance=LazyInit)
    builder.register(widgets.MainWindow)
