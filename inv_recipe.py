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
        # self.select_recipe = None
    
    def update(self):
        if not self.app.is_modal(self): return
        
        # if self.is_openinv:
        #     self.app.terrain.view_invinfo()        
        
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
                    if not self.backpack_cell_num is None and self.backpack_cell_num<len(self.backpack_recipe):
                        # select item
                        selected_factory = self.app.factories.selected
                        selected_factory.recipe = self.backpack_recipe[self.backpack_cell_num]
                        selected_factory.command_step = 0
                        selected_factory.status = FSTAT_CHG_RECIPE                        
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
            if item==self.select_recipe:
                rect_selection = (pos[0], pos[1], 48, 48)
                pg.draw.rect(self.surface, pg.Color('yellow'), rect_selection, 1)

            #count
            # text = self.font.render(str(item['count']),True, pg.Color('white'))
            # count_text_pos = (pos[0]+INV_CELL_W-text.get_width()-3, pos[1]+INV_CELL_H-text.get_height()-3)
            # self.surface.blit(text, count_text_pos)
        
        self.app.screen.blit(self.surface, INV_POS)

    def get_cell(self, pos):
        pos2=((pos[0]-INV_POS[0]-INV_MARGIN)//INV_CELL_W, (pos[1]-INV_POS[1]-INV_MARGIN)//INV_CELL_H)
        cell=(pos[0]-INV_POS[0]-INV_MARGIN)//INV_CELL_W+(pos[1]-INV_POS[1]-INV_MARGIN)//INV_CELL_H*INV_CELL_CW
        if cell<0 or cell>INV_CELL_COUNT or pos2[0]<0 or pos2[0]>INV_CELL_CW-1:
            return(None, None)
        else:
            if cell>-1 and cell<len(self.backpack_recipe):
                block = self.backpack_recipe[cell]
            else:
                block = None
            return(cell,block)

    def load_recipe(self, allow_recipe_list, select_recipe):
        self.select_recipe = select_recipe
        for recipe_id in allow_recipe_list:
            recipe = self.app.data.get_recipe_by_id(recipe_id)
            self.append(recipe)
        
        
    def append(self, recipe):
        self.backpack_recipe.append(recipe)
        
    def clear(self):
        self.backpack_recipe.clear()
        
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
        
        
            
            