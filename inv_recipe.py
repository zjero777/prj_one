from random import randrange

import pygame as pg
import pygame_gui as gui

from inv import inv
from mouse import *
from options import *


class inv_recipe(inv):
    def __init__(self, app):
        super().__init__(app, (-3, -2), (2,5), inv_cell_h=64,  bg_color=pg.Color('#1f1f1f'), bg_hover_color=pg.Color('#2f2f2f'), inv_margin=5)
    
    def update(self):
        super().update()
        if not self.is_open: return
      
        mouse_status_type = self.app.mouse.status['type']
        mouse_status_button = self.app.mouse.status['button']
      
        if self.keystate[pg.K_ESCAPE] or (mouse_status_type == MOUSE_TYPE_CLICK and mouse_status_button==MOUSE_RBUTTON):
            if self.first_pressed:
                self.first_pressed = False 
                self.is_open = False
                self.clear()
        else:
            self.first_pressed = True
            
        
        self.hover_cell_num, _item, self.is_hover = self.get_cell(self.mouse_pos)
        if self.mouse_button[0]:
            if self.first_click:
                self.first_click = False 
                if not self.hover_cell_num is None and self.hover_cell_num<len(self.cells):
                    # select item
                    selected_factory = self.app.factories.selected
                    selected_factory.recipe = self.cells[self.hover_cell_num]
                    selected_factory.command_step = 0
                    selected_factory.status = FSTAT_CHG_RECIPE                        
                    self.is_open = False
                    self.clear()
        else:
            self.first_click = True

    
    def draw(self):
        if not self.is_open: return
        super().draw()
        
        # draw backpack items
        i=-1
        for item in self.cells:
            i+=1
            pos = self.get_pos(i)
            # pos = (i%10*self.inv_cell_h+i%self.inv_cell_cw+self.inv_margin, i//self.inv_cell_ch*self.inv_cell_h+i//self.inv_cell_ch+self.inv_margin)
            icon_size = (self.inv_cell_size[0]*0.9, self.inv_cell_size[1]*0.9)
            item_pos = (pos[0]+(self.inv_cell_w // 2 - icon_size[0] // 2), pos[1]+(self.inv_cell_h // 2 - icon_size[1] // 2))
            #img
            pic = pg.transform.scale(self.app.data.recipe_img[item['id']], icon_size)
            self.surface.blit(pic, item_pos)
            if item==self.select_recipe:
                rect_selection = (pos, self.inv_cell_size)
                pg.draw.rect(self.surface, pg.Color('yellow'), rect_selection, 1)
        
        self.app.screen.blit(self.surface, self.inv_pos)

    def load_recipe(self, allow_recipe_list, select_recipe):
        self.select_recipe = select_recipe
        for recipe_id in allow_recipe_list:
            recipe = self.app.data.get_recipe_by_id(recipe_id)
            self.append(recipe)
        
        
    def append(self, recipe):
        self.cells.append(recipe)
        
    def clear(self):
        self.cells.clear()
        
    def view_recipe_info(self):
        mouse_pos = pg.mouse.get_pos()
        cell_num, recipe, is_hover = self.get_cell(mouse_pos)
        if cell_num is None: return
        if recipe is None: return
        name = recipe['name']
        self.app.info.append_text(f'Рецепт: {name}')
        self.app.info.append_pic(self.app.data.recipe_img[recipe['id']])
        if 'in' in dict.keys(recipe):
            self.app.info.append_text('Вход:')
            self.app.info.append_list_items(recipe['in'])
        if 'out' in dict.keys(recipe):
            self.app.info.append_text('Выход:')
            self.app.info.append_list_items(recipe['out'])
        process = recipe['time']
        self.app.info.append_text(
            f'Производство: {process:0.1f} сек')
        
        
            
            