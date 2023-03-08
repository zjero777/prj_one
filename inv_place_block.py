from logging import warn
from random import randrange
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *
from inv import *

class inv_place_block(inv):
    def __init__(self, app):
        super().__init__(app)
        # self.available_blocks = []
        self.update_available_blocks()
        
    def open(self):
        super().open()
    
    def update(self):
        super().update()
        if not self.is_open: return

        mouse_status_type = self.app.mouse.status['action']
        mouse_status_button = self.app.mouse.status['button']
        # mouse_status_area = self.app.mouse.status['area']

        
        if (mouse_status_type==MOUSE_TYPE_CLICK and mouse_status_button==MOUSE_RBUTTON) or (self.keystate[pg.K_e]) or (self.keystate[pg.K_ESCAPE]): # Rigth mouse button click
            self.close()
        
        
        if not self.is_hover: return
        
        # if self.keystate[pg.K_e] and self.app.inv_toolbar.selected_cell:
        #     if self.first_pressed:
        #         self.first_pressed = False
        #         self.is_open = not self.is_open
        #         if self.is_open:
        #             self.app.ui_tech_bp.hide()
        # else:
        #     self.first_pressed = True
            

        if mouse_status_type==MOUSE_TYPE_CLICK and mouse_status_button==MOUSE_LBUTTON: # Rigth mouse button click
        # if self.mouse_button[0]:
            # if self.first_click:
            #     self.first_click = False 
            if not self.hover_cell_num is None and self.hover_cell_num<len(self.cells):
                # select item
                self.select(self.hover_cell_num)
                # self.selected_cell = self.hover_cell_num
                self.app.mouse.setcursor_with_item(self.hover_item)
                place_block_tool_id = self.app.data.get_tool_by_name('place_block')
                self.app.inv_toolbar.set_image(place_block_tool_id, self.hover_item['img'])
                self.close()
                

            
                    
        # else:
        #     self.first_click = True

        # if not self.selected_cell_num is None:
        #     self.app.mouse.setcursor_with_item(self.item)
        # else:
        #     self.app.mouse.setcursor_noitem()    

    
    def draw(self):
        # draw selected item on terrain
        self.tile_pos = self.app.mouse.tile_pos   
        self.pos = self.app.terrain.pos
        
        if self.tile_pos:
            xyRect = pg.Rect((self.tile_pos[0]-self.pos[0]+HALF_WIDTH)*TILE,
                            (self.tile_pos[1]-self.pos[1]+HALF_HIGHT)*TILE, TILE, TILE)

            # Ghost cursor
            place = self.app.data.GetInfo(
                'name', self.app.terrain.field[self.tile_pos[0], self.tile_pos[1]])
            build_item, b_type = self.app.terrain.Get_info_block_placed(
                self.app.player.inv.item, place)
            
            
            is_operate = self.app.terrain.operate[self.tile_pos[0], self.tile_pos[1]]

            if b_type and is_operate:
                # allow place
                img = self.app.terrain.Get_img(build_item, b_type).copy()
                img.set_alpha(172)
                self.surface.blit(img, xyRect)
            else:
                if build_item: 
                    # disallow place
                    img = self.app.terrain.Get_img(build_item, 'block').copy()
                    img.set_alpha(172)
                    colorImage = pg.Surface(img.get_size()).convert_alpha()
                    colorImage.fill(pg.Color('red'))
                    img.blit(colorImage, (0, 0),
                                special_flags=pg.BLEND_RGBA_MULT)
                    self.surface.blit(
                        img, xyRect, special_flags=pg.BLEND_RGBA_MIN)
    
    
        
        
        # draw inv
        if not self.is_open: return
        super().draw()
        # self.draw_items()
        
        # blit on main screen
        self.app.screen.blit(self.surface, self.inv_pos)

        
    def incomplete_stack(self, item):
        idx=-1
        if self.cells == []: return(False, idx)
        for i in self.cells:
            idx += 1
            if i['id'] == int(item):
                return(True, idx)
        return(False, idx)
            
    def append(self, item, count=1):
        self.cells.append({'id':int(item), 'count':count})
        pass
        
    def stack(self, item, stack_number, count=1):
        self.cells[stack_number]['id'] = item
        self.cells[stack_number]['count'] += count
        
    def add(self, item, count=1):
        isIncomplete, stack_number = self.incomplete_stack(item)
        if isIncomplete:
            self.stack(item, stack_number, count)
        else:
            self.append(item, count)

    def delete_selected_backpack_cell(self):
        if self.item['count'] == 1: 
            del self.item
            self.selected_cell_num = None
            # self.item = {}
        elif self.item['count'] > 1:
            self.item['count'] -= 1
    
    def item_exist(self, item):
        use_item = 0
        if self.item: use_item = (self.item['id']==item['id'])*1
        finditem = next((x for x in self.cells if x['id'] == item['id']), {'id':0,'count':0})
        return(finditem['count']-use_item>item['count']-1)
        
    def exist(self, items):
        if items is None: return(True)
        for block in items:
            if not self.item_exist(block):
                return(False)
        return(True)

    def find_by_key(self, iterable, key, value):
        for index, dict_ in enumerate(iterable):
            if key in dict_ and dict_[key] == value:
                return (index, dict_)
        return -1, -1

    def add_item(self, block):
        if block['id']==0: 
            warn('try add block id=0')
            return
        index, item = self.find_by_key(self.cells, 'id', block['id'])
        if index>-1:
            self.cells[index] = {'id': block['id'], 'count': block['count']+item['count']}  
        else:
            self.cells.append(block)
            

    def delete_item(self, block):
        finditem = next((x for x in self.cells if x['id'] == block['id']), False)
        if not finditem: return
        if finditem['count']==block['count']: 
            item = self.item
            self.cells.remove(finditem)
            self.selected_cell_num = None
            idx=0
            for i in self.cells:
                if i==item:
                    self.selected_cell_num = idx
                    break
                idx+=1
                    
            
            
            
        elif finditem['count'] > block['count']:
            finditem['count'] = finditem['count'] - block['count']

    def delete(self, items):
        if items is None: return
        for block in items:
            self.delete_item(block)
            
    def insert(self, items):
        for block in items:
            if block['id']>0:
                self.add_item(block.copy())
            
    def view_info(self):
        mouse_pos = pg.mouse.get_pos()
        cell_num, item, hover = self.get_cell(mouse_pos)
        if item is None: return
        item = self.app.data.get_bdata('id', item['id'])
        name = item['name']
        self.app.info.append_text(f'Название: {name}')
        self.app.info.append_pic(item['img'])
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
    
    def delete_id(self, list, id):
        for item in list:
            if item['id'] == id: list.remove(item)
    
    def update_available_blocks(self):
        self.cells = []
        all_block_types = self.app.data.data['block_type']
        
        all_factory_types = self.app.data.data['factory_type']
        for f_item in all_factory_types:
            if f_item['open'] and 'use_recipes' in f_item.keys():
                recipe_id_types = f_item['use_recipes']['allowed_id']
                for recipe_id in recipe_id_types:
                    recipe = self.app.data.get_recipe_by_id(recipe_id)
                    blocks_id = recipe['out']
                    for block_item in blocks_id:
                        block = self.app.data.get_block_by_id(block_item['id'])
                        if block and not block in self.cells:
                            # if {'id':block_item['id']} not in self.cells:
                            
                            self.cells.append(block)
                            block['img'] = (pg.image.load(path.join(img_dir, block['pic'])).convert_alpha())                                                                            
        #                     self.delete_id(all_block_types, block['id'])
        # for block in all_block_types:
        #     if {'id':block['id']} not in self.cells:
        #         self.cells.append({'id':block['id']})
            
