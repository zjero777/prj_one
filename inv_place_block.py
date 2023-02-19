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
    
    def update(self):
        super().update()
        if not self.is_open: return
        if not self.is_hover: return
        
        # if self.keystate[pg.K_e] and self.app.inv_toolbar.selected_cell:
        #     if self.first_pressed:
        #         self.first_pressed = False
        #         self.is_open = not self.is_open
        #         if self.is_open:
        #             self.app.ui_tech_bp.hide()
        # else:
        #     self.first_pressed = True
            
        if self.mouse_button[0]:
            if self.first_click:
                self.first_click = False 
                if not self.hover_cell_num is None and self.hover_cell_num<len(self.cells):
                    # select item
                    self.select(self.hover_cell_num)
                    # self.selected_cell = self.hover_cell_num
                    self.app.mouse.setcursor_with_item(self.hover_item)
        else:
            self.first_click = True

        if not self.selected_cell_num is None:
            self.app.mouse.setcursor_with_item(self.item)
        else:
            self.app.mouse.setcursor_noitem()    

    
    def draw(self):
        # draw selected item on terrain
        self.tile_pos = self.app.mouse.tile_pos   
        self.pos = self.app.terrain.pos
        
        if self.tile_pos:
            xyRect = pg.Rect((self.tile_pos[0]-self.pos[0]+HALF_WIDTH)*TILE,
                            (self.tile_pos[1]-self.pos[1]+HALF_HIGHT)*TILE, TILE, TILE)

            if not self.app.player.inv.is_open and self.app.player.inv.item:
                # Ghost cursor
                place = self.app.terrain.GetInfo(
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

        # draw backpack items
        i=-1
        for item in self.cells:
            i+=1

            pos = self.get_pos(i)

            # pos = (i%10*self.inv_cell_h+i%self.inv_cell_cw+self.inv_margin, i//self.inv_cell_ch*self.inv_cell_h+i//self.inv_cell_ch+self.inv_margin)
            item_pos = (pos[0]+8, pos[1]+8)
            #img
            pic = pg.transform.scale(self.app.terrain.block_img[item['id']], (32, 32))
            self.surface.blit(pic, item_pos)
            #count
            text = self.font.render(str(item['count']),True, pg.Color('white'))
            count_text_pos = (pos[0]+self.inv_cell_h-text.get_width()-3, pos[1]+self.inv_cell_h-text.get_height()-3)
            self.surface.blit(text, count_text_pos)
        
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
            
            