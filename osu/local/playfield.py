from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.beatmap.beatmap import Beatmap
from osu.local.beatmap.beatmap_utility import BeatmapUtil
from misc.callback import callback

from gui.objects.layer.layers.std.hitobject_outline_layer import HitobjectOutlineLayer
from gui.objects.layer.layers.std.hitobject_aimpoint_layer import HitobjectAimpointLayer
from gui.objects.layer.layers.std.aimpoint_paths_layer import AimpointPathsLayer
from gui.objects.layer.layers.std.aimpoint_velocity_text_layer import AimpointVelocityTextLayer
from gui.objects.layer.layers.std.aimpoint_angle_text_layer import AimpointAngleTextLayer


'''
Visualizes a beatmap

Input: 
    beatmap - The beatmap to visualize
    time - The time value of the playfield. The time value which point in time to view the beatmap for.

Output: 
    Visual display of the beatmap's contents
'''
class Playfield(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)

        self.time = 0
        self.beatmap = None
        self.visible_hitobjects = []
        self.layers = {}

        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.set_time.connect(self.update_hitobject_visiblity)


    def load_beatmap(self, beatmap):
        self.beatmap = beatmap
        
        for hitobject in beatmap.hitobjects:
            beatmap.set_cs_val.connect(hitobject.set_radius)
        
        # To set the now connected hitobject radii
        beatmap.set_cs_val(beatmap.cs)
        

    def layer_changed(self):
        self.scene.update()


    def resizeEvent(self, event):
        for layer in self.layers.values():
            layer.area_resize_event(self.width(), self.height())

        self.scene.update()


    def update_hitobject_visiblity(self, time):
        print('time: ', time)

        self.visible_hitobjects = BeatmapUtil.get_hitobjects_visible_at_time(self.beatmap, time)
        for hitobject in self.visible_hitobjects:
            hitobject.time_changed(self.time)
            hitobject.set_opacity(BeatmapUtil.get_opacity_at(self.beatmap, hitobject, time))
            
        self.scene.update()


    @callback
    def set_time(self, time):        
        self.time = time
        self.set_time.emit(self.time)


    def get_layers(self):
        return self.layers.values()


    def get_layer(self, layer_name):
        return self.layers[layer_name]


    @callback
    def add_layer_event(self, layer):
        self.layers[layer.name] = layer
        self.scene.addItem(layer)
        self.scene.update()

        self.add_layer_event.emit(layer)


    def remove_layer(self, layer_name):
        self.scene.removeItem(self.layer[layer_name])
        del self.layer[layer_name]
        self.scene.update()


    def create_basic_map_layers(self):
        if self.beatmap.gamemode == Beatmap.GAMEMODE_OSU:
            self.add_layer_event(HitobjectOutlineLayer(self))
            self.add_layer_event(HitobjectAimpointLayer(self))
            self.add_layer_event(AimpointPathsLayer(self))
            self.add_layer_event(AimpointVelocityTextLayer(self))
            self.add_layer_event(AimpointAngleTextLayer(self))
            return

        if self.beatmap.gamemode == Beatmap.GAMEMODE_MANIA:
            # TODO
            return

        if self.beatmap.gamemode == Beatmap.GAMEMODE_TAIKO:
            # TODO
            return

        if self.beatmap.gamemode == Beatmap.GAMEMODE_CATCH:
            # TODO
            return