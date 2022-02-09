from numpy.lib.function_base import append, select
import pygame as pg
import pygame_gui as gui
from options import *

class info:
    def __init__(self, app):
        self.app = app
        # self.surface = pg.Surface(WIN_SIZE)
        pg.font.init()
        #self.win_info = gui.elements.UIWindow(pg.Rect((0, 0), (SC_WIDTH, SC_HIGHT)), self.app.manager)
        self.main_panel_info = gui.elements.UIPanel(relative_rect=pg.Rect((FIELD_WIDTH,0),(P_INFO, SC_HIGHT)), 
                                               starting_layer_height=0, 
                                               manager=self.app.manager, 
                                               margins={'left':0,'top':3,'right':0,'bottom':3}
                                               #container=self.win_info
                                               )


        self.map_panel_info = gui.elements.UIPanel(relative_rect=pg.Rect((0,0),(P_INFO, 320)), 
                                               starting_layer_height=1, 
                                               manager=self.app.manager, 
                                               margins={'left':0,'top':3,'right':0,'bottom':3},
                                               container=self.main_panel_info,
                                               element_id='map_info'
                                               )

        self.panel_info = gui.elements.UIPanel(relative_rect=pg.Rect((0,320),(P_INFO, 400)), 
                                               starting_layer_height=0, 
                                               manager=self.app.manager, 
                                               margins={'left':0,'top':3,'right':0,'bottom':3},
                                               container=self.main_panel_info,
                                               element_id='panel_info'
                                               )
        
        
        self.text_rect = pg.Rect((0, 64), (INFO_WIDTH, 150))
        self.text_info = gui.elements.UITextBox(
                                    f'',
                                    relative_rect=self.text_rect, manager=self.app.manager, container=self.panel_info, object_id='textinfo')
        #self.start_button = gui.elements.UIButton(relative_rect=self.text_rect,
        #                                                 text='Start',
        #                                                 manager=self.app.manager)

        self.pic_rect = pg.Rect((0+INFO_WIDTH//2-63//2, 0), (63, 63))
        self.pic_info = gui.elements.UIImage(self.pic_rect,  self.app.terrain.field_img[0], self.app.manager, container=self.panel_info)


        # debuf info
        self.debug_font = pg.font.SysFont('arial', 36)
        self.debug_textlist = []
        
        # self.panels = []
        # self.panels.append(self.building_panel_info)
        # self.panels.append(self.terrain_panel_info)


        
        
    def update(self):
        pass
    
    def draw(self):
        # self.surface.fill(pg.Color(255,0,0))
        for item in self.debug_textlist:
            self.text_surface = self.debug_font.render(item['text'], True, (255, 0, 0))
            self.app.screen.blit(self.text_surface, item['pos'])
        self.debug_textlist.clear()
    
    def set(self, text, img_index):
        
        self.text_info.html_text = f'<font face=fira_code size=4>{text}</font>'
        self.pic_info.set_image(self.app.terrain.field_img[img_index])

        self.text_info.rebuild()
        
        
    def debug(self, pos,text):
        debugtext = f'{text}'
        self.debug_textlist.append({'pos':pos,'text':debugtext})

            
            
            
            