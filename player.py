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
        self.place_rect = None  
        self.one_place_fit = None  
        self.one_place_rect = None  
        self.remove_fit = None    
        self.remove_rect = None  
        self.remove_start = None
        
        
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

    def get_dig_field(self, lookup):
        result = np.zeros(lookup.shape, 'bool')
        for i, row in enumerate(lookup):
            for j, el in enumerate(row):
                terrain = self.app.data.get_terrain_by_id(el)
                result[i,j] = terrain['allow_dig']=='True'
        return result
        

    def get_place_fit(self, terrain, area: pg.Rect, place_item):
        building_lookup = terrain.building_map[area.left:area.left+area.width, area.top:area.top+area.height]
        field_lookup = terrain.field[area.left:area.left+area.width, area.top:area.top+area.height]
        operate_lookup = terrain.operate[area.left:area.left+area.width, area.top:area.top+area.height]
        bp_block_lookup = terrain.bp_block[area.left:area.left+area.width, area.top:area.top+area.height]
        bp_field_lookup = terrain.bp_field[area.left:area.left+area.width, area.top:area.top+area.height]
        # calc place block 0-no block placed, !=0 set new block
        block_result = self.get_place_block(field_lookup, place_item)
        # calc place field 0-no field change, !=0 change field
        field_result = self.get_place_field(field_lookup, place_item)
        # calc allow
        building_result = np.logical_and(np.logical_and((building_lookup == 0), (np.logical_or((block_result != 0),(field_result != 0)))) , (operate_lookup !=0))
        # calc bp
        building_result = np.logical_and(building_result, np.logical_and((bp_block_lookup == 0), (bp_field_lookup == 0)))
        result = {'allow': building_result, 'block': block_result, 'field': field_result}
        return result
        
    def get_remove_fit(self, terrain, area: pg.Rect, start_pos):
        # if not start_pos: return
        building_lookup = terrain.building_map[area.left:area.left+area.width, area.top:area.top+area.height]
        field_lookup = terrain.field[area.left:area.left+area.width, area.top:area.top+area.height]
        operate_lookup = terrain.operate[area.left:area.left+area.width, area.top:area.top+area.height]
        bp_block_lookup = terrain.bp_block[area.left:area.left+area.width, area.top:area.top+area.height]
        bp_field_lookup = terrain.bp_field[area.left:area.left+area.width, area.top:area.top+area.height]
        is_bp = terrain.bp_block[start_pos] != 0 or terrain.bp_field[start_pos] != 0
        is_block = False
        is_factory = False
        is_field = False
        
        if not is_bp:
            is_block = terrain.building_map[start_pos] > 0 
            is_factory = terrain.building_map[start_pos] == -1
            
        if not (is_block or is_factory or is_bp):
            is_field = terrain.field[start_pos] != 0
        # bp_lookup = np.logical_or((bp_block_lookup == 1), (bp_field_lookup == 1))
        if is_bp:
            # blueprint
            bp_lookup = bp_block_lookup + bp_field_lookup
            remove_result = np.logical_and(bp_lookup!=0, operate_lookup!=0)
        elif is_factory:
            # building
            remove_result = np.logical_and(building_lookup==-1, operate_lookup!=0)
        elif is_block:
            # block
            remove_result = np.logical_and(building_lookup>0, operate_lookup !=0)
        elif is_field:
            # field
            # calc dig field 0-no dig field , !=0 dig field
            field_result = self.get_dig_field(field_lookup)
            field_result = np.logical_and(field_result, building_lookup==0)
            field_result = np.logical_and(field_result, bp_block_lookup==0)
            field_result = np.logical_and(field_result, bp_field_lookup==0)
            remove_result = np.logical_and(field_result, operate_lookup!=0)
        else:
            remove_result = np.logical_and(field_lookup!=0, operate_lookup!=0)

        result = {'remove': remove_result, 'is_block': is_block, 'is_bp': is_bp, 'is_factory': is_factory, 'is_field': is_field}
        return result
        
    
    def set_place(self, terrain, fit, area):
        bp_field_lookup = terrain.bp_field[area.left:area.left+area.width, area.top:area.top+area.height]
        bp_block_lookup = terrain.bp_block[area.left:area.left+area.width, area.top:area.top+area.height]
        for i, row in enumerate(fit['allow']):
            for j, el in enumerate(row):
                if el:
                    if fit['field'][i,j]>0: bp_field_lookup[i,j] = fit['field'][i,j]
                    if fit['block'][i,j]>0: bp_block_lookup[i,j] = fit['block'][i,j]

    def set_remove(self, terrain, fit, area):
        if not area: return
        bp_field_lookup = terrain.bp_field[area.left:area.left+area.width, area.top:area.top+area.height]
        bp_block_lookup = terrain.bp_block[area.left:area.left+area.width, area.top:area.top+area.height]
        
        

        
        for i, row in enumerate(fit['remove']):
            for j, el in enumerate(row):
                if el:
                    if fit['is_bp']:
                        bp_field_lookup[i,j] = 0
                        bp_block_lookup[i,j] = 0
                    if fit['is_block']:
                        bp_block_lookup[i,j] = -1
                    if fit['is_field']:
                        bp_field_lookup[i,j] = -1
                    if fit['is_factory']:
                        factory = self.app.factories.factory((i+area.left, j+area.top))
                        factory.set_on_remove()
                            
                        

        
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
        
        if not self.app.inv_toolbar.item is None and self.app.inv_toolbar.item['id'] == TOOL_PLACE and self.app.inv_place_block.item: 
            if mouse_status_area and self.app.mouse.tile_pos:
                self.one_place_rect = pg.Rect(self.app.mouse.tile_pos, (1,1))
                self.one_place_fit = self.get_place_fit(self.app.terrain, self.one_place_rect, self.app.inv_place_block.item)
            
            if mouse_status_type==MOUSE_TYPE_DRAG and mouse_status_button==MOUSE_LBUTTON: 
                if mouse_status_area and self.app.mouse.tile_pos:
                    self.place_rect = mouse_status_area
                    self.place_fit = self.get_place_fit(self.app.terrain, self.place_rect, self.app.inv_place_block.item)
               

            if mouse_status_type==MOUSE_TYPE_DROP and mouse_status_button==MOUSE_LBUTTON or mouse_status_action==MOUSE_TYPE_DROP and mouse_status_button==MOUSE_LBUTTON: 
                if self.app.mouse.tile_pos:
                    self.set_place(self.app.terrain, self.place_fit, self.place_rect)
                    # self.app.mouse.status['area'] = None
                    # self.app.mouse.status['rect'] = None
                self.place_rect = None
                self.place_fit = None     
                           
            if mouse_status_type==MOUSE_TYPE_CLICK and mouse_status_button==MOUSE_LBUTTON:
                self.set_place(self.app.terrain, self.one_place_fit, self.one_place_rect)
                self.one_place_rect = None
                self.one_place_fit = None     
     
        # remove
        if not self.app.inv_toolbar.item is None and self.app.inv_toolbar.item['id'] == TOOL_REMOVE: 
            if mouse_status_type==MOUSE_TYPE_BUTTON_DOWN and mouse_status_button==MOUSE_LBUTTON: 
                if mouse_status_area:
                    self.remove_start = mouse_status_area.topleft


            if mouse_status_type==MOUSE_TYPE_DRAG and mouse_status_button==MOUSE_LBUTTON: 
                if mouse_status_area and self.app.mouse.tile_pos and self.remove_start:
                    self.remove_rect = mouse_status_area
                    self.remove_fit = self.get_remove_fit(self.app.terrain, self.remove_rect, self.remove_start)
                    
            if mouse_status_type==MOUSE_TYPE_DROP and mouse_status_button==MOUSE_LBUTTON or mouse_status_action==MOUSE_TYPE_DROP and mouse_status_button==MOUSE_LBUTTON or (mouse_status_type==MOUSE_TYPE_CLICK and mouse_status_button==MOUSE_LBUTTON): 
                if self.app.mouse.tile_pos and self.remove_start:
                    self.set_remove(self.app.terrain, self.remove_fit, self.remove_rect)
                self.remove_start = None
                self.remove_rect = None
                self.remove_fit = None     
                

    
    def draw_place_fit(self, surface, place_rect, place_fit):
        if not place_fit is None:
            for i, row in enumerate(place_fit['allow']):
                for j, el in enumerate(row):
                    screen_pos = self.app.terrain.demapping((i+place_rect[0],j+place_rect[1]))
                    f_rect = pg.Rect(screen_pos, (TILE, TILE))
                    if el:
                        if place_fit['block'][i,j] !=0:
                            surface.blit(self.app.data.get_block_by_id(place_fit['block'][i,j])['img_bp'], f_rect.topleft)    
                        if place_fit['field'][i,j] !=0:
                            surface.blit(self.app.data.get_terrain_by_id(place_fit['field'][i,j])['img_bp'], f_rect.topleft)          
        
    def draw_remove_fit(self, surface, remove_rect, remove_fit):
        if not remove_fit is None:
            for i, row in enumerate(remove_fit['remove']):
                for j, el in enumerate(row):
                    screen_pos = self.app.terrain.demapping((i+remove_rect[0],j+remove_rect[1]))
                    f_rect = pg.Rect(screen_pos, (TILE, TILE))
                    if el:
                        if remove_fit['is_block']:
                            # remove block cursor
                            surface.blit(self.app.terrain.rem_block_mark, f_rect.topleft)    
                        # if place_fit['field'][i,j] !=0:
                        #     surface.blit(self.app.data.get_terrain_by_id(place_fit['field'][i,j])['img_bp'], f_rect.topleft)          
                        if remove_fit['is_factory']:
                            # remove block cursor
                            surface.blit(self.app.terrain.dig_mark, f_rect.topleft)    
                        if remove_fit['is_field']:
                            # remove block cursor
                            surface.blit(self.app.terrain.dig_mark, f_rect.topleft)
                        if remove_fit['is_bp']:
                            # remove bp cursor
                            field_id = self.app.terrain.field[i+remove_rect.topleft[0], j+remove_rect.topleft[1]]
                            block_id = self.app.terrain.building_map[i+remove_rect.topleft[0], j+remove_rect.topleft[1]]
                            if field_id > 0:
                                terrain = self.app.data.get_terrain_by_id(field_id)
                                surface.blit(terrain['img'], f_rect.topleft)
                            if block_id > 0:
                                block = self.app.data.get_block_by_id(block_id)
                                surface.blit(block['img'], f_rect.topleft)
    
    
    def draw(self, surface):
        # self.inv.draw()
        
        if self.app.inv_toolbar.item is None: return
        if self.app.inv_toolbar.is_hover: 
            self.place_rect = None
            self.place_fit = None                
            return

        self.tile_pos = self.app.mouse.tile_pos
        if not self.tile_pos: return
        xyRect = pg.Rect(self.app.terrain.demapping(self.tile_pos), (TILE, TILE))
        pg.draw.rect(surface, pg.Color('gray'), xyRect, 1) 
        
        if self.app.inv_toolbar.item['id'] == TOOL_PLACE: 
            # self.app.info.debug((0,10), self.tile_pos)        
            # draw cursor place block
            self.draw_place_fit(surface, self.one_place_rect, self.one_place_fit)
            self.draw_place_fit(surface, self.place_rect, self.place_fit)
            
        if self.app.inv_toolbar.item['id'] == TOOL_REMOVE:
            self.draw_remove_fit(surface, self.remove_rect, self.remove_fit)
    
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
        factory.in_storage.add_items([{'id':2,'count':20}])
        
        
        item = self.app.data.GetBData('name', 'mound')
        # area = pg.Rect((pos[0]+6, pos[1]), (2,2))
        # fit = self.get_place_fit(self.app.terrain, area, item)
        # self.set_place(self.app.terrain, fit, area)
        
        self.app.terrain.field[pos[0]-6,pos[1]-3] = self.app.data.GetTData('name', 'water')['id']
        area = pg.Rect((pos[0]-7, pos[1]-3), (2,2))
        fit = self.get_place_fit(self.app.terrain, area, item)
        self.set_place(self.app.terrain, fit, area)

        
        

        
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
        
            
