from logging import warn
from random import randrange
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *

class inv:
# # inventory
# INV_MARGIN = 15
# INV_CELL_W = 48
# INV_CELL_H = 48
# INV_CELL_SIZE = (INV_CELL_W, INV_CELL_H)
# INV_CELL_COUNT = 100
# INV_CELL_CW = 10
# INV_CELL_CH = INV_CELL_COUNT // INV_CELL_CW
# INV_WIDTH = INV_CELL_W*INV_CELL_CW+(INV_CELL_CW-1)+INV_MARGIN*2
# INV_HIGHT = INV_CELL_H*INV_CELL_CH+(INV_CELL_CH-1)+INV_MARGIN*2
# INV_SIZE = (INV_WIDTH, INV_HIGHT)
# INV_POS = (FIELD_WIDTH // 2 - INV_WIDTH // 2+INV_MARGIN, FIELD_HIGHT // 2 - INV_HIGHT // 2+INV_MARGIN)
# INV_RECT = (INV_POS[0], INV_POS[1], INV_WIDTH, INV_HIGHT)    
    
    
    def __init__(self, app, margin=15):
        self.app = app

        self.selected_cell = None
        self.cells = []
        self.hover_cell_num = None
        self.is_open = False
        

        self.surface = pg.Surface(INV_SIZE)
        self.bgimg = pg.image.load(path.join(img_dir, 'invbg.png')).convert()
        self.bgimgactive = pg.image.load(path.join(img_dir, 'invbgactive.png')).convert()
        self.bgrect = self.bgimg.get_rect()        
        self.font = pg.font.Font(None, 15)
        
        self.first_pressed = True
        self.first_click = True
    
    @property    
    def item(self):
        if self.selected_cell is None: return(None)
        return(self.cells[self.selected_cell])
  
        
        
    def get_cell(self, pos):
        pos2=((pos[0]-INV_POS[0]-INV_MARGIN)//INV_CELL_W, (pos[1]-INV_POS[1]-INV_MARGIN)//INV_CELL_H)
        cell=(pos[0]-INV_POS[0]-INV_MARGIN)//INV_CELL_W+(pos[1]-INV_POS[1]-INV_MARGIN)//INV_CELL_H*INV_CELL_CW
        # self.app.info.debug((0,80), f'{pos2}')
        # i = (i%10*INV_CELL_W+i%10+INV_MARGIN, i//10*INV_CELL_H+i//10+INV_MARGIN)
        if cell<0 or cell>INV_CELL_COUNT or pos2[0]<0 or pos2[0]>INV_CELL_CW-1:
            return(None, None)
        else:
            if cell>-1 and cell<len(self.cells):
                block = self.cells[cell]
            else:
                block = None
            return(cell,block)
        
    def update(self):
        if not self.app.is_modal(self): return
        self.keystate = pg.key.get_pressed()
        self.mouse_button = pg.mouse.get_pressed()
        self.mouse_pos = pg.mouse.get_pos()

    
    def draw(self):
        if not self.is_open: return
        
        self.surface.fill(pg.Color(33,40,45))

        #  draw bg cells 
        for i in range(INV_CELL_COUNT):
            pos = (i%INV_CELL_CW*INV_CELL_W+i%INV_CELL_CW+INV_MARGIN, i//INV_CELL_CH*INV_CELL_H+i//INV_CELL_CH+INV_MARGIN)
            if self.hover_cell_num==i:
                # hover
                self.surface.blit(self.bgimgactive, pos)
            else:
                # normal
                self.surface.blit(self.bgimg, pos)
        

        


        

            
            
            