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
        
        self.load_from_data()
        self.select_building = None
    
    def update(self):
        super().update()
        # if self.app.inv_place_block.item is None:
        #     self.change_icon('place_block', )

        if not self.is_hover: return
        if self.app.inv_recipe.is_open: return
        if self.app.inv_place_block.is_open: return        
        
      
        mouse_status_type = self.app.mouse.status['action']
        mouse_status_button = self.app.mouse.status['button']
      
        if mouse_status_type==MOUSE_TYPE_CLICK and mouse_status_button==MOUSE_LBUTTON: # Rigth mouse button click      
            if self.hover_item:
                if self.hover_item['type'] == 'toggle' :
                    if self.hover_item['name'] == 'place_block':
                        if (not (self.app.inv_place_block.item is None) and (self.selected_cell_num == TOOL_PLACE)) or self.app.inv_place_block.item is None:
                            # select item
                            self.select(self.hover_cell_num)
                            if self.app.inv_place_block.item:
                                self.app.mouse.setcursor_with_item(self.app.inv_place_block.item)
                            
                            self.app.inv_place_block.open()
                        else:
                            self.select(self.hover_cell_num)
                            if self.app.inv_place_block.item:
                                self.app.mouse.setcursor_with_item(self.app.inv_place_block.item)
                            
                    else:
                        self.select(self.hover_cell_num)
                        self.app.mouse.setcursor_noitem()
                        
                

                            


    
    def draw(self):
        if not self.is_open: return
        super().draw()
        # self.draw_items()        
       
       # draw items
        # i=-1
        # for item in self.cells:
        #     i+=1
        #     pos = self.get_pos(i)
        #     icon_size = (self.inv_cell_size[0]*0.9, self.inv_cell_size[1]*0.9)
        #     item_pos = (pos[0]+(self.inv_cell_w // 2 - icon_size[0] // 2), pos[1]+(self.inv_cell_h // 2 - icon_size[1] // 2))
        #     #img
        #     pic = pg.transform.scale(item['img'], icon_size)
        #     self.surface.blit(pic, item_pos)
        #     if item==self.item:
        #         rect_selection = (pos, self.inv_cell_size)
        #         pg.draw.rect(self.surface, pg.Color('yellow'), rect_selection, 1)
        
        self.app.screen.blit(self.surface, self.inv_pos)
        
    def view_info(self):
        mouse_pos = pg.mouse.get_pos()
        cell_num, item, hover = self.get_cell(mouse_pos)
        if item is None: return
        if self.app.inv_place_block.is_open: return
        name = item['description']
        self.app.info.append_text(f'{name}')
        # self.app.info.append_pic(self.app.data.block_img[item['id']])
        # if 'in' in dict.keys(recipe):
        #     self.app.info.append_text('Вход:')
        #     self.app.info.append_list_items(recipe['in'])
        # if 'out' in dict.keys(recipe):
        #     self.app.info.append_text('Выход:')
        #     self.app.info.append_list_items(recipe['out'])
        # process = recipe['time']
        # self.app.info.append_text(
        #     f'Производство: {process:0.1f} сек')
        
    def load_from_data(self):
        self.img = [None for i in self.app.data.data['toolbar']]
        for item in self.app.data.data['toolbar']:
            self.cells.append(item)
            item['img'] = (pg.image.load(path.join(img_dir, item['icon'])).convert_alpha())

            
        self.default = self.cells.copy()
        
        
            
            