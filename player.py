import numpy as np
import pygame as pg
import pygame_gui as gui
from numpy import cos, sin

from inv_backpack import *
from options import *
from terrain import terrain


class player:
    def __init__(self, app):
        self.app = app
        self.inv = inv_backpack(self.app, self)
        self.dig = False
        self.timer = app.timer
        self.start_dig = 0
        self.demolition = False
        self.warmup = 0
        self.pos = ()  
        self.place_fit = None      
        
    def Get_info_block_placed(self, place_item, place):
        if not place_item: return
        terrain = self.app.data.get_terrain_by_id(place)
        result_item = place_item
        result_type = ''
        rules = place_item.get('build', False)
        if rules:
            rule = rules.get(terrain['name'])
            if rule:  # {'id':'1','count':3}
                result_type = rule.get('type')
                if not result_type:
                    result_type = 'block'
                result_item_name = rule.get('result')
                if result_type == 'block':
                    result_item = self.app.data.get_block_by_name(result_item_name)
                else:
                    result_item = self.app.data.get_terrain_by_name(result_item_name)
            elif rule == {}:  # {}
                result_type = 'block'
        return(result_item, result_type)
        
    def get_place_block(self, lookup, place_item):
        result = np.zeros(lookup.shape, 'int')
        for i, row in enumerate(lookup):
            for j, el in enumerate(row):
                item, use_type = self.Get_info_block_placed(place_item, el)
                if use_type=='block':
                    result[i,j] = item['id']
        return result

    def get_place_field(self, lookup, place_item):
        result = np.zeros(lookup.shape, 'int')
        for i, row in enumerate(lookup):
            for j, el in enumerate(row):
                item, use_type = self.Get_info_block_placed(place_item, el)
                if use_type=='terrain':
                    result[i,j] = item['id']
        return result

    def get_place_fit(self, terrain, area: pg.Rect, place_item):
        building_lookup = terrain.building_map[area.left:area.left+area.width, area.top:area.top+area.height]
        field_lookup = terrain.field[area.left:area.left+area.width, area.top:area.top+area.height]
        operate_lookup = terrain.operate[area.left:area.left+area.width, area.top:area.top+area.height]
        # calc place block 0-no block placed, !=0 set new block
        block_result = self.get_place_block(field_lookup, place_item)
        # calc place field 0-no field change, !=0 change field
        field_result = self.get_place_field(field_lookup, place_item)
        # calc allow
        building_result = np.logical_and(np.logical_and((building_lookup == 0), (np.logical_or((block_result != 0),(field_result != 0)))) , (operate_lookup !=0))
        result = {'allow': building_result, 'block': block_result, 'field': field_result}
        return result
        
    def set_place(self, terrain, fit, area):
        bp_field_lookup = terrain.bp_field[area.left:area.left+area.width, area.top:area.top+area.height]
        bp_block_lookup = terrain.bp_block[area.left:area.left+area.width, area.top:area.top+area.height]
        for i, row in enumerate(fit['allow']):
            for j, el in enumerate(row):
                if el:
                    if fit['field'][i,j]>0: bp_field_lookup[i,j] = fit['field'][i,j]
                    if fit['block'][i,j]>0: bp_block_lookup[i,j] = fit['block'][i,j]
        
    def update(self):
        # self.inv.update()
        if self.app.inv_recipe.is_open: return
        if self.app.inv_place_block.is_open: return        
        if self.app.inv_toolbar.is_hover: return

        # control
        mouse_status_type = self.app.mouse.status['tile_action']
        mouse_status_action = self.app.mouse.status['action']
        mouse_status_button = self.app.mouse.status['button']
        mouse_status_area = self.app.mouse.status['area']

        
        # place block
        # if self.app.inv_toolbar.item is None: return
        if not self.app.inv_toolbar.item is None and self.app.inv_toolbar.item['id'] == TOOL_PLACE: 
            if mouse_status_type==MOUSE_TYPE_DRAG and mouse_status_button==MOUSE_LBUTTON: 
                if mouse_status_area:
                    self.place_rect = mouse_status_area
                    self.place_fit = self.get_place_fit(self.app.terrain, self.place_rect, self.app.inv_place_block.item)
               
            self.app.info.debug((0,10), self.app.mouse.status)

            if mouse_status_type==MOUSE_TYPE_DROP and mouse_status_button==MOUSE_LBUTTON or mouse_status_action==MOUSE_TYPE_DROP and mouse_status_button==MOUSE_LBUTTON: 
                self.set_place(self.app.terrain, self.place_fit, self.place_rect)
                self.app.mouse.status['area'] = None
                self.app.mouse.status['rect'] = None
                self.place_rect = None
                self.place_fit = None     
                           
                
     
        
        # remove
        
    
    def draw(self, surface):
        # self.inv.draw()
        
        
        if self.app.inv_toolbar.item is None: return
        if not self.app.inv_toolbar.item['id'] == TOOL_PLACE: 
            return
        # draw place block cursor area
        if not self.place_fit is None:
            # area = self.app.mouse.status['area']
            for i, row in enumerate(self.place_fit['allow']):
                for j, el in enumerate(row):
                    screen_pos = self.app.terrain.demapping((i+self.place_rect[0],j+self.place_rect[1]))
                    f_rect = pg.Rect(screen_pos, (TILE, TILE))
                    if el:
                        if self.place_fit['block'][i,j] !=0:
                            surface.blit(self.app.data.get_block_by_id(self.place_fit['block'][i,j])['img'], f_rect.topleft)    
                        if self.place_fit['field'][i,j] !=0:
                            surface.blit(self.app.data.get_terrain_by_id(self.place_fit['field'][i,j])['img'], f_rect.topleft)    
                            
        
        
    
    # Place the item selected from the inventory on titlepos the ground
    # player.inv.selected_backpack_cell - selected inventory item 
    def build(self, field):
        if not self.inv.selected_cell_num is None:
            item = self.inv.item
            place = field.GetInfo('name', field.field[field.tile_pos[0], field.tile_pos[1]])
            build_item, build_type = field.Get_info_block_placed(item, place)   
            if build_type=='terrain':
                field.field[field.tile_pos[0], field.tile_pos[1]] = build_item['id']
                self.use_selected()
            elif build_type=='block':
                field.building_map[field.tile_pos[0], field.tile_pos[1]]=build_item['id']
                self.use_selected()     
                self.app.ui_tech.refresh_site_content(field.tile_pos)
                
    
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
        
    def fall(self, pos):
        self.set_spawn(pos)
        terra = self.app.terrain

        bp = self.app.data.GetFData('name', 'escape_pod')
        b_map = terra.building_map

        main_factory=self.app.factories.add(bp, b_map, pos[0], pos[1])
        pos = (pos[0]+main_factory.size[0]//2, pos[1]+main_factory.size[1]//2)
        main_factory.storage.add_items([{'id':1,'count':20},{'id':16,'count':10},{'id':2, 'count':10},{'id':3,'count':10}])
        self.scorch_ground(pos, 4)
        self.add_water(pos, 7)
        self.go_pos(terra, pos)
        self.set_spawn(pos)
        
        bp = self.app.data.GetFData('name', 'miller')
        factory=self.app.factories.add(bp, b_map, pos[0]+4, pos[1])
        factory.create_storage_in(factory.incom_recipe)
        factory.in_storage.add_items([{'id':1,'count':20}])

        
        

        
    def go_pos(self, terra, pos):
        if terra.onMap(pos[0],pos[1]):
            terra.pos = pos
            
    def set_spawn(self, pos):
        self.pos = pos
        
    def go_spawn(self):
        terra = self.app.terrain
        self.go_pos(terra, self.pos)
        
    def scorch_ground(self, pos, rad):
        for angle in range(0, 360,2):
            r = randrange(0, rad)
            x = r * cos(angle)
            y = r * sin(angle)
            self.app.terrain.field[round(pos[0]+x-0.5),round(pos[1]+y-0.5)] = self.app.data.GetTData('name', 'scorched_ground')['id']
            
    def add_water(self, pos, rad):
        angle = randrange(0, 360)
        x = rad * cos(angle)
        y = rad * sin(angle)
        self.app.terrain.field[round(pos[0]+x-0.5),round(pos[1]+y-0.5)] = self.app.data.GetTData('name', 'water')['id']
        
            
