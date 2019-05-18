from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback


class LayerGui(QWidget):

    def __init__(self, layer):
        super().__init__()

        self.layer = layer

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout       = QVBoxLayout()
        self.label        = QLabel(self.layer.name, self)
        self.enable_chkbx = QCheckBox('visible')


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.enable_chkbx)

        self.enable_chkbx.toggled.connect(self.layer_enable_event)

    
    def update_gui(self):
        self.label.setAlignment(Qt.AlignCenter)
        self.enable_chkbx.setCheckState(Qt.Checked if self.layer.isVisible() else Qt.Unchecked)

    
    def layer_opacity_event(self, opacity):
        self.layer.setOpacity(opacity)
        self.layer.layer_changed()


    def layer_enable_event(self, chkbx_state):
        self.layer.setVisible(chkbx_state)
        self.layer.layer_changed()


    @callback
    def layer_destroy_event(self):
        self.layer_destroy_event.emit(self.name)
    