from logging import warn
from random import randrange
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *

class inv:
    def __init__(self, app):
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
        
        keystate = pg.key.get_pressed()
        if keystate[pg.K_1]:
            if self.first_pressed:
                self.first_pressed = False 
                self.is_open = True
        else:
            self.first_pressed = True
            
        mouse_button = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        if self.is_open:
            self.hover_cell_num, _item = self.get_cell(mouse_pos)
            if mouse_button[0]:
                if self.first_click:
                    self.first_click = False 
                    if not self.hover_cell_num is None and self.hover_cell_num<len(self.cells):
                        # select item
                        self.selected_cell = self.hover_cell_num
            else:
                self.first_click = True

    
    def draw(self):
        if not self.is_open: return
        
        self.surface.fill(pg.Color(33,40,45))

        #  draw cells cells
        for i in range(INV_CELL_COUNT):
            pos = (i%INV_CELL_CW*INV_CELL_W+i%INV_CELL_CW+INV_MARGIN, i//INV_CELL_CH*INV_CELL_H+i//INV_CELL_CH+INV_MARGIN)
            if self.hover_cell_num==i:
                # hover
                self.surface.blit(self.bgimgactive, pos)
            else:
                # normal
                self.surface.blit(self.bgimg, pos)
        
        # draw cells items
        i=-1
        for item in self.cells:
            i+=1
            pos = (i%10*INV_CELL_W+i%INV_CELL_CW+INV_MARGIN, i//INV_CELL_CH*INV_CELL_H+i//INV_CELL_CH+INV_MARGIN)
            item_pos = (pos[0]+8, pos[1]+8)
            #img
            pic = pg.transform.scale(self.app.terrain.block_img[item['id']], (32, 32))
            self.surface.blit(pic, item_pos)
        
        self.app.screen.blit(self.surface, INV_POS)

        

            
            
            