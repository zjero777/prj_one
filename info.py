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
        self.panel_info = gui.elements.UIPanel(relative_rect=pg.Rect((FIELD_WIDTH-2,-2),(SC_WIDTH, SC_HIGHT+4)), 
                                               starting_layer_height=0, 
                                               manager=self.app.manager, 
                                               margins={'left':3,'top':10,'right':3,'bottom':10}
                                               #container=self.win_info
                                               )
        self.text_rect = pg.Rect((0, 65), (INFO_WIDTH, 120))
        self.text_info = gui.elements.UITextBox(
                                    '',
                                    relative_rect=self.text_rect, manager=self.app.manager, container=self.panel_info)
        #self.start_button = gui.elements.UIButton(relative_rect=self.text_rect,
        #                                                 text='Start',
        #                                                 manager=self.app.manager)
        
        self.field_img = []
        self.field_img = append(self.field_img, pg.image.load(path.join(img_dir, "s1.png")).convert())
        self.field_img = append(self.field_img, pg.image.load(path.join(img_dir, "e1.png")).convert())
        self.field_img = append(self.field_img, pg.image.load(path.join(img_dir, "hs.png")).convert())
        self.field_rect = self.field_img[1].get_rect()        
        
        self.pic_rect = pg.Rect((5, 0), (63, 63))
        self.pic_info = gui.elements.UIImage(self.pic_rect,  self.field_img[0], self.app.manager, container=self.panel_info)


        # debuf info
        self.debug_font = pg.font.SysFont('arial', 36)
        self.debug_textlist = []

        
        
    def update(self):
        pass
    
    def draw(self):
        # self.surface.fill(pg.Color(255,0,0))
        for item in self.debug_textlist:
            self.text_surface = self.debug_font.render(item['text'], True, (255, 0, 0))
            self.app.screen.blit(self.text_surface, item['pos'])
        self.debug_textlist.clear()
    
    def set(self, text, img_index):
        self.text_info.html_text = f'<font face=fira_code size=4 color=#FFFFFF><b>Info:</b><br><br>{text}</font><br><img src="img/s1.png"></img>'
        self.pic_info.set_image(self.field_img[img_index])
        self.text_info.rebuild()
        
    def debug(self, pos,text):
        debugtext = f'{text}'
        self.debug_textlist.append({'pos':pos,'text':debugtext})

            
            
            
            