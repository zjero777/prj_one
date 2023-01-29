from logging import warn
from random import randrange
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *
from inv import inv

class inv_recipe(inv):
    def __init__(self, app):
        super().__init__(app, app.player)
        self.is_openinv = False
        self.backpack_recipe = []
    
    def update(self):
        if not self.app.is_modal(self): return
        
        if self.is_openinv:
            pass
        
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            if self.first_pressed:
                self.first_pressed = False 
                self.is_openinv = False
                self.clear()
        else:
            self.first_pressed = True
            
        mouse_button = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        if self.is_openinv:
            self.backpack_cell_num, _item = self.get_cell(mouse_pos)
            if mouse_button[0]:
                if self.first_click:
                    self.first_click = False 
                    if self.backpack_cell_num>-1 and self.backpack_cell_num<len(self.backpack_recipe):
                        # select item
                        self.selected_backpack_cell = self.backpack_cell_num
                        self.is_openinv = False
                        self.clear()
            else:
                self.first_click = True

    
    def draw(self):
        if not self.is_openinv: return
        self.surface.fill(pg.Color(33,40,45))

        #  draw backpack cells
        for i in range(INV_CELL_COUNT):
            pos = (i%INV_CELL_CW*INV_CELL_W+i%INV_CELL_CW+INV_MARGIN, i//INV_CELL_CH*INV_CELL_H+i//INV_CELL_CH+INV_MARGIN)
            if self.backpack_cell_num==i:
                # hover
                self.surface.blit(self.bgimgactive, pos)
            else:
                # normal
                self.surface.blit(self.bgimg, pos)
        
        # draw backpack items
        i=-1
        for item in self.backpack_recipe:
            i+=1
            pos = (i%10*INV_CELL_W+i%INV_CELL_CW+INV_MARGIN, i//INV_CELL_CH*INV_CELL_H+i//INV_CELL_CH+INV_MARGIN)
            item_pos = (pos[0]+8, pos[1]+8)
            #img
            pic = pg.transform.scale(self.app.data.recipe_img[item['id']], (32, 32))
            self.surface.blit(pic, item_pos)
            #count
            # text = self.font.render(str(item['count']),True, pg.Color('white'))
            # count_text_pos = (pos[0]+INV_CELL_W-text.get_width()-3, pos[1]+INV_CELL_H-text.get_height()-3)
            # self.surface.blit(text, count_text_pos)
        
        self.app.screen.blit(self.surface, INV_POS)

    def load_recipe(self, allow_recipe_list):
        for recipe_id in allow_recipe_list:
            recipe = self.app.data.get_recipe_by_id(recipe_id)
            self.append(recipe)
        
    def append(self, recipe):
        self.backpack_recipe.append(recipe)
        
    def clear(self):
        self.backpack_recipe.clear()
        
            
            