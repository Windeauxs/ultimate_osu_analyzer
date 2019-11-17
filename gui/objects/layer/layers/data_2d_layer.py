from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.std.std import Std


class Data2DLayer(Layer, Temporal):

    def __init__(self, name, data, draw_func, time_driver):
        Layer.__init__(self, name)
        Temporal.__init__(self)

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())

        self.data      = data
        self.draw_func = draw_func


    def paint(self, painter, option, widget):
        if not self.time: return
        painter.setPen(QColor(0, 0, 0, 255))
        
        ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT
        
        try: self.draw_func(painter, ratio_x, ratio_y, self.time, self.data)
        except Exception as e: print(e)