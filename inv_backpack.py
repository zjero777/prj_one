from logging import warn
from random import randrange
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *
from inv import *

class inv_backpack(inv):
    def __init__(self, app, player):
        super().__init__(app)
        self.player = player
        self.cells = [{'id':1,'count':20},{'id':16,'count':10},{'id':2, 'count':10},{'id':25,'count':10},{'id':4,'count':50},{'id':3,'count':50}]
        self.text_rect = pg.Rect((0, 0), (300, 300))
    
    def update(self):
        if not self.app.is_modal(self): return
        
        keystate = pg.key.get_pressed()
        if keystate[pg.K_e] and keystate[pg.K_f]:
            if self.first_pressed:
                self.first_pressed = False 
                # if self.app.ui_tech.enabled: return
                self.is_open = not self.is_open
                if self.is_open:
                    self.app.ui_tech_bp.hide()
        else:
            self.first_pressed = True
            
        mouse_button = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        if self.is_open:
            self.hover_cell_num, item = self.get_cell(mouse_pos)
            # self.app.info.debug((0,60), f'{self.cells_cell_num}')
            if mouse_button[0]:
                if self.first_click:
                    self.first_click = False 
                    if not self.hover_cell_num is None and self.hover_cell_num<len(self.cells):
                        # select item
                        self.selected_cell = self.hover_cell_num
                        self.app.mouse.setcursor_with_item(item)
            else:
                self.first_click = True
        else:
            self.app.mouse.setcursor_noitem()    

        if not self.selected_cell is None:
            self.app.mouse.setcursor_with_item(self.cells[self.selected_cell])
        else:
            self.app.mouse.setcursor_noitem()    

    
    def draw(self):
        
        if not self.is_open: return
        self.surface.fill(pg.Color(33,40,45)) 

        #  draw backpack cells
        for i in range(INV_CELL_COUNT):
            pos = (i%INV_CELL_CW*INV_CELL_W+i%INV_CELL_CW+INV_MARGIN, i//INV_CELL_CH*INV_CELL_H+i//INV_CELL_CH+INV_MARGIN)
            if self.hover_cell_num==i:
                # hover
                self.surface.blit(self.bgimgactive, pos)
            else:
                # normal
                self.surface.blit(self.bgimg, pos)
        
        # draw backpack items
        i=-1
        for item in self.cells:
            i+=1
            pos = (i%10*INV_CELL_W+i%INV_CELL_CW+INV_MARGIN, i//INV_CELL_CH*INV_CELL_H+i//INV_CELL_CH+INV_MARGIN)
            item_pos = (pos[0]+8, pos[1]+8)
            #img
            pic = pg.transform.scale(self.app.terrain.block_img[item['id']], (32, 32))
            self.surface.blit(pic, item_pos)
            #count
            text = self.font.render(str(item['count']),True, pg.Color('white'))
            count_text_pos = (pos[0]+INV_CELL_W-text.get_width()-3, pos[1]+INV_CELL_H-text.get_height()-3)
            self.surface.blit(text, count_text_pos)
        
        self.app.screen.blit(self.surface, INV_POS)

        
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
        if self.cells[self.selected_cell]['count'] == 1: 
            del self.cells[self.selected_cell]
            self.selected_cell = None
            # self.item = {}
        elif self.cells[self.selected_cell]['count'] > 1:
            self.cells[self.selected_cell]['count'] -= 1
    
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
            self.selected_cell = None
            idx=0
            for i in self.cells:
                if i==item:
                    self.selected_cell = idx
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
            
            