from random import randrange
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *

class inv:
    def __init__(self, app, player):
        self.app = app
        self.player = player
        self.backpack = [{'id':1, 'count':7}]
        self.selected_Item = -1
        self.item = {}
        # for item in range(3):
            # self.add(randrange(0,4))
        self.surface = pg.Surface(INV_SIZE)
        
        self.bgimg = pg.image.load(path.join(img_dir, 'invbg.png')).convert()
        self.bgimgactive = pg.image.load(path.join(img_dir, 'invbgactive.png')).convert()
        self.bgrect = self.bgimg.get_rect()        
        self.font = pg.font.Font(None, 15)
        
        


        # self.panel_info = gui.elements.UIPanel(relative_rect=pg.Rect(INV_RECT), 
        #                                        starting_layer_height=0, 
        #                                        manager=self.app.manager, 
        #                                        margins={'left':0,'top':0,'right':0,'bottom':0}
        #                                        )
        self.text_rect = pg.Rect((0, 0), (300, 300))
        self.first_pressed = True
        self.first_click = True
        
    def get_cell(self, pos):
        pos2=((pos[0]-INV_POS[0]-INV_MARGIN)//INV_CELL_W, (pos[1]-INV_POS[1]-INV_MARGIN)//INV_CELL_H)
        cell=(pos[0]-INV_POS[0]-INV_MARGIN)//INV_CELL_W+(pos[1]-INV_POS[1]-INV_MARGIN)//INV_CELL_H*INV_CELL_CW
        # self.app.info.debug((0,80), f'{pos2}')
        # i = (i%10*INV_CELL_W+i%10+INV_MARGIN, i//10*INV_CELL_H+i//10+INV_MARGIN)
        if cell<0 or cell>INV_CELL_COUNT or pos2[0]<0 or pos2[0]>INV_CELL_CW-1:
            return(-1, -1)
        else:
            if cell>-1 and cell<len(self.backpack):
                item = self.backpack[cell]
            else:
                item = -1
            return(cell,item)
        
    def update(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_e]:
            if self.first_pressed:
                self.first_pressed = False 
                self.player.is_openinv = not self.player.is_openinv
        else:
            self.first_pressed = True
            
        mouse_button = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        if self.selected_Item>-1:
            self.app.mouse.setcursor_with_item(self.backpack[self.selected_Item])
        else:
            self.app.mouse.setcursor_noitem()    
        
        if self.player.is_openinv:
            self.cover, item = self.get_cell(mouse_pos)
            # self.app.info.debug((0,60), f'{self.cover}')
            if mouse_button[0]:
                if self.first_click:
                    self.first_click = False 
                    if self.cover>-1 and self.cover<len(self.backpack):
                        # select item
                        self.selected_Item = self.cover
                        self.item = item
            else:
                self.first_click = True
        else:
            self.app.mouse.setcursor_noitem()    
    
    def draw(self):
        self.surface.fill(pg.Color(33,40,45))

        #  draw backpack cells
        for i in range(INV_CELL_COUNT):
            pos = (i%INV_CELL_CW*INV_CELL_W+i%INV_CELL_CW+INV_MARGIN, i//INV_CELL_CH*INV_CELL_H+i//INV_CELL_CH+INV_MARGIN)
            if self.cover==i:
                # hover
                self.surface.blit(self.bgimgactive, pos)
            else:
                # normal
                self.surface.blit(self.bgimg, pos)
        
        # draw backpack items
        i=-1
        for item in self.backpack:
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
        if self.backpack == []: return(False, idx)
        for i in self.backpack:
            idx += 1
            if i['id'] == int(item):
                return(True, idx)
        return(False, idx)
            
    def append(self, item, count=1):
        self.backpack.append({'id':int(item), 'count':count})
        
    def stack(self, item, stack_number, count=1):
        self.backpack[stack_number]['id'] = item
        self.backpack[stack_number]['count'] += count
        
    def add(self, item, count=1):
        isIncomplete, stack_number = self.incomplete_stack(item)
        if isIncomplete:
            self.stack(item, stack_number, count)
        else:
            self.append(item, count)

    def delete_selected_item(self):
        if self.backpack[self.selected_Item]['count'] == 1: 
            del self.backpack[self.selected_Item]
            self.selected_Item = -1
            self.item = {}
        elif self.backpack[self.selected_Item]['count'] > 1:
            self.backpack[self.selected_Item]['count'] -= 1
    
    def item_exist(self, item):
        use_item = 0
        if self.item: use_item = (self.item['id']==item['id'])*1
        finditem = next((x for x in self.backpack if x['id'] == item['id']), {'id':0,'count':0})
        return(finditem['count']-use_item>item['count']-1)
        
    def exist(self, items):
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
        index, item = self.find_by_key(self.backpack, 'id', block['id'])
        if index>-1:
            self.backpack[index] = {'id': block['id'], 'count': block['count']+item['count']}  
        else:
            self.backpack.append(block)
            

    def delete_item(self, block):
        finditem = next((x for x in self.backpack if x['id'] == block['id']), False)
        if not finditem: return
        if finditem['count']==block['count']: 
            self.backpack.remove(finditem)
        elif finditem['count'] > block['count']:
            finditem['count'] = finditem['count'] - block['count']

    def delete(self, items):
        for block in items:
            self.delete_item(block)
            
    def insert(self, items):
        for block in items:
            self.add_item(block)
            
            