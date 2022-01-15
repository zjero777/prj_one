import pygame as pg
import pygame_gui as gui
from options import *

class inv:
    def __init__(self, app):
        self.app = app
        # self.surface = pg.Surface((INV_WIDTH, INV_HIGHT))
        # INV_RECT = (0,SC_HIGHT-P_BOTTOM,SC_WIDTH-P_INFO-1,SC_HIGHT)

        self.panel_info = gui.elements.UIPanel(relative_rect=pg.Rect((-2,SC_HIGHT-P_BOTTOM-2),(INV_WIDTH+4, INV_HIGHT+4)), 
                                               starting_layer_height=0, 
                                               manager=self.app.manager, 
                                               margins={'left':3,'top':10,'right':3,'bottom':10}
                                               )
        # self.text_rect = pg.Rect((0, 0), (300, 300))
        
    def update(self):
        pass
    
    def draw(self):
        pass
        # self.surface.fill(pg.Color(255,0,0))
        # self.app.screen.blit(self.surface, INV_RECT)
    
    