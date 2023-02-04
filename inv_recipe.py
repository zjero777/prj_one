from logging import warn
from random import randrange
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *
from inv import inv

class inv_recipe(inv):
    def __init__(self, app):
        super().__init__(app, (-3, -2), (2,5))
    
    def update(self):
        super().update()
      
        if self.keystate[pg.K_ESCAPE]:
            if self.first_pressed:
                self.first_pressed = False 
                self.is_open = False
                self.clear()
        else:
            self.first_pressed = True
            
        if self.is_open:
            self.hover_cell_num, _item = self.get_cell(self.mouse_pos)
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
            item_pos = (pos[0]+8, pos[1]+8)
            #img
            pic = pg.transform.scale(self.app.data.recipe_img[item['id']], (32, 32))
            self.surface.blit(pic, item_pos)
            if item==self.select_recipe:
                rect_selection = (pos[0], pos[1], 48, 48)
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
        cell_num, recipe = self.get_cell(mouse_pos)
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
        
        
            
            