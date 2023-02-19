from random import randrange

import pygame as pg
import pygame_gui as gui

from inv import inv
from mouse import *
from options import *


class inv_toolbar(inv):
    def __init__(self, app):
        super().__init__(app, (-2, -3), (6,2), bg_color=pg.Color('#1f1f1f'), inv_margin=5)
        self.is_open = True
        self.click = False
        self.append()
        self.select_building = None
    
    def update(self):
        super().update()
        # if not self.is_open: return
        if not self.is_hover: return
        if self.app.inv_recipe.is_open: return
      
        mouse_status_type = self.app.mouse.status['tile_action']
        mouse_status_button = self.app.mouse.status['button']
      
        if self.mouse_button[0]:
            if self.first_click:
                self.click = False
                self.first_click = False 
                self.is_hover_cell = not self.hover_cell_num is None and self.hover_cell_num<len(self.cells)
                if self.is_hover_cell:
                    if self.hover_item['type'] == 'toggle' :
                        # select item
                        self.select(self.hover_cell_num)
                        # self.selected_cell = self.hover_item
            else: 
                if not self.mouse_button[0]:
                    self.click = True
                
        else:
            self.first_click = True

    
    def draw(self):
        if not self.is_open: return
        super().draw()
        self.draw_items(self.app.data.toolbar_img)        
       
    #    # draw items
    #     i=-1
    #     for item in self.cells:
    #         i+=1
    #         pos = self.get_pos(i)
    #         icon_size = (self.inv_cell_size[0]*0.9, self.inv_cell_size[1]*0.9)
    #         item_pos = (pos[0]+(self.inv_cell_w // 2 - icon_size[0] // 2), pos[1]+(self.inv_cell_h // 2 - icon_size[1] // 2))
    #         #img
    #         pic = pg.transform.scale(self.app.data.toolbar_img[item['id']], icon_size)
    #         self.surface.blit(pic, item_pos)
    #         if item==self.selected_cell:
    #             rect_selection = (pos, self.inv_cell_size)
    #             pg.draw.rect(self.surface, pg.Color('yellow'), rect_selection, 1)
        
        self.app.screen.blit(self.surface, self.inv_pos)
        
    def view_info(self):
        mouse_pos = pg.mouse.get_pos()
        cell_num, recipe, hover = self.get_cell(mouse_pos)
        if cell_num is None: return
        # name = recipe['name']
        # self.app.info.append_text(f'Рецепт: {name}')
        # self.app.info.append_pic(self.app.data.recipe_img[recipe['id']])
        # if 'in' in dict.keys(recipe):
        #     self.app.info.append_text('Вход:')
        #     self.app.info.append_list_items(recipe['in'])
        # if 'out' in dict.keys(recipe):
        #     self.app.info.append_text('Выход:')
        #     self.app.info.append_list_items(recipe['out'])
        # process = recipe['time']
        # self.app.info.append_text(
        #     f'Производство: {process:0.1f} сек')
        
    def append(self):
        for item in self.app.data.data['toolbar']:
            self.cells.append(item)
            
            