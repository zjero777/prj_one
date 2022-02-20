import pygame as pg
import pygame_gui as gui
from options import *
from inv import *

class player:
    def __init__(self, app):
        self.app = app
        self.inv = inv(self.app, self)
        self.dig = False
        self.timer = app.timer
        self.start_dig = 0
        self.is_openinv = False
        self.demolition = False
        self.warmup = 0        
        
    def update(self):
        self.inv.update()
    
    def draw(self):
        if self.is_openinv:
            self.inv.draw()
    
    # Place the item selected from the inventory on titlepos the ground
    # player.inv.selected_backpack_cell - selected inventory item 
    def build(self, field):
        if self.inv.selected_backpack_cell>-1:
            item = self.inv.item
            place = field.GetInfo('name', field.field[field.tile_pos[0], field.tile_pos[1]])
            build_item, build_type = field.Get_info_block_placed(item, place)   
            if build_type=='terrain':
                field.field[field.tile_pos[0], field.tile_pos[1]] = build_item['id']
                self.use_selected()
            elif build_type=='block':
                field.building_map[field.tile_pos[0], field.tile_pos[1]]=build_item['id']
                self.use_selected()       
    
    def manual_dig(self, field, tilepos, time):
        if not self.dig:
            self.tile_pos = tilepos
            self.dig = True
            self.warmup = self.timer.get_ticks()
            self.app.mouse.setcursor(cursor_type.dig)
        else:
            dt = self.timer.get_ticks()-self.warmup
            if tilepos==self.tile_pos:
                if dt>time*1000:
                    self.warmup = self.timer.get_ticks()
                    field.dig_succes(self, tilepos)
                    self.stop_dig()
                    return(True)
            else:
                self.stop_dig()
                    
    
    def stop_dig(self):
        if self.dig:
            self.app.mouse.setcursor(cursor_type.normal)
            self.dig = False
            self.hp = 100
            
            

            self.app.info.debug((0,30), f'{self.hp} - dig: {self.dig}')
       
    def manual_demolition(self, field, tilepos, time):
        if not self.demolition:
            self.tile_pos = tilepos
            self.demolition = True
            self.warmup = self.timer.get_ticks()
            self.app.mouse.setcursor(cursor_type.dig)
            return(False)
        else:
            dt = self.timer.get_ticks()-self.warmup
            if tilepos==self.tile_pos:
                if dt>time*1000:
                    self.warmup = self.timer.get_ticks()
                    field.demolition_succes(self, tilepos)
                    self.stop_demolition()
                    return(True)
            else:
                self.stop_demolition()
                
                

    def stop_demolition(self):
        if self.demolition:
            self.app.mouse.setcursor(cursor_type.normal)
            self.demolition = False
            self.warmup = 0

            
    def pickup(self, loot, count=1):
        self.inv.add(loot, count)
     
    def use_selected(self):
        self.inv.delete_selected_backpack_cell()
        
