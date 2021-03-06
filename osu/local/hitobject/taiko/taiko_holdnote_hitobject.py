from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.taiko.taiko import Taiko

from misc.frozen_cls import FrozenCls


@FrozenCls
class TaikoHoldNoteHitobject(QGraphicsItem, Hitobject):

    def __init__(self, data):
        QGraphicsItem.__init__(self)
        Hitobject.__init__(self, data)


    def paint(self, painter, option, widget):
        # TODO
        pass


    def resizeEvent(self, event):
        print('owh')


    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)