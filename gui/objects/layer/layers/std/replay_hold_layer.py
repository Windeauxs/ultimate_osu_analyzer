from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import numpy as np

from misc.math_utils import *
from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.std.std import Std, StdSettings
from analysis.osu.std.replay_data import StdReplayData


class StdReplayHoldLayer(Layer, Temporal):

    def __init__(self, replay, time_driver):
        self.replay_data = StdReplayData.get_replay_data(replay.play_data)

        Layer.__init__(self, 'Replay hold - ' + str(replay.player_name))
        Temporal.__init__(self)

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())

        StdSettings.set_k1_color.connect(self.layer_changed)
        StdSettings.set_k2_color.connect(self.layer_changed)
        StdSettings.set_m1_color.connect(self.layer_changed)
        StdSettings.set_m2_color.connect(self.layer_changed)
        StdSettings.set_view_time_back.connect(self.layer_changed)
        StdSettings.set_view_time_ahead.connect(self.layer_changed)


    def paint(self, painter, option, widget):
        if not self.time: return

        ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT

        start_idx = StdReplayData.get_idx_time(self.replay_data, self.time - StdSettings.view_time_back)
        end_idx   = StdReplayData.get_idx_time(self.replay_data, self.time + StdSettings.view_time_ahead)

        for prev_event, curr_event in zip(self.replay_data[start_idx:end_idx - 1], self.replay_data[start_idx + 1:end_idx]):
            prev_pos_x, curr_pos_x = prev_event[StdReplayData.XPOS]*ratio_x, curr_event[StdReplayData.XPOS]*ratio_x
            prev_pos_y, curr_pos_y = prev_event[StdReplayData.YPOS]*ratio_y, curr_event[StdReplayData.YPOS]*ratio_y

            if   prev_event[StdReplayData.K1]: painter.setPen(StdSettings.k1_color)
            elif prev_event[StdReplayData.K2]: painter.setPen(StdSettings.k2_color)
            elif prev_event[StdReplayData.M1]: painter.setPen(StdSettings.m1_color)
            elif prev_event[StdReplayData.M2]: painter.setPen(StdSettings.m2_color)
            else:                              painter.setPen(QColor(0, 0, 0, 0))

            painter.drawLine(prev_pos_x, prev_pos_y, curr_pos_x, curr_pos_y)