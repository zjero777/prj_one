from distutils.util import strtobool
from math import ceil
from sys import flags
import numpy as np
import pygame as pg
import random as rnd
import json
import pygame_gui as gui


from pygame.event import Event
from factory import factory_list

from info import info
from options import *
from waterfall import *


class terrain:
    def __init__(self, app, width, height):
        self.app = app
        
        # self.enabled = True
        # self.first_pressed = [False, False, False]
        
        # self.area = pg.Rect(0,0,0,0)
        # self.start = self.area
      
        
        self.pos = (PLANET_WIDTH//2, PLANET_HIGHT//2)
        # self.selection = [-1, -1]
        self.surface = pg.Surface((FIELD_WIDTH, FIELD_HIGHT))
        self.field = np.zeros((width, height), dtype='i')
        self.dark_cover = np.ones((width, height), dtype=np.bool)
        # self.fog_of_war = np.ones((width, height), dtype=np.bool)
        self.operate = np.zeros((width, height), dtype=np.int)
        self.building_map = np.zeros((width, height), dtype='i')
        self.bp_field = np.zeros((width, height), dtype=np.int)
        self.bp_block = np.zeros((width, height), dtype=np.int)
        self.first_click = True
        self.tile_pos = ()

        self.field.fill(self.app.data.FindTInfo('id', 'ground'))

        for i in range(5000):
            self.field[rnd.randint(0, PLANET_WIDTH-1),
                       rnd.randint(0, PLANET_HIGHT-1)] = 0
        for i in range(15000):
            self.field[rnd.randint(0, PLANET_WIDTH-1),
                       rnd.randint(0, PLANET_HIGHT-1)] = 4
        for i in range(15000):
            self.field[rnd.randint(0, PLANET_WIDTH-1),
                       rnd.randint(0, PLANET_HIGHT-1)] = 6
        for i in range(500):
            self.field[rnd.randint(0, PLANET_WIDTH-1),
                       rnd.randint(0, PLANET_HIGHT-1)] = 9

        for i in range(2500):
            self.building_map[rnd.randint(0, PLANET_WIDTH-1), rnd.randint(
                0, PLANET_HIGHT-1)] = 1
        for i in range(5000):
            self.building_map[rnd.randint(0, PLANET_WIDTH-1), rnd.randint(
                0, PLANET_HIGHT-1)] = 6
                
                
        #self.field[50, 50] = 1
        # for i in range(100):
        self.building_map[9, 7] = 2
        self.building_map[10, 7] = 1
        #    self.field[i,99] = 1
        #    self.field[0,i] = 1
        #   self.field[99,i] = 1

        self.field_bg = pg.image.load(
            path.join(img_dir, 'bg.jpg')).convert_alpha()
        self.field_bgrect = self.field_bg.get_rect()
        
        self.bg_blue = pg.Surface((TILE,TILE), pg.SRCALPHA)
        pg.draw.rect(self.bg_blue, pg.Color(64,128,255,128), (0,0,TILE, TILE))
        self.bg_red = pg.Surface((TILE,TILE), pg.SRCALPHA)
        pg.draw.rect(self.bg_red, pg.Color(255,32,128,128), (0,0,TILE, TILE))

        

    def onMap(self, tile_x, tile_y):
        return(tile_x >= 0 and tile_y >= 0 and tile_x < PLANET_WIDTH and tile_y < PLANET_HIGHT)

    def complete_factory(self):
        x, y = self.tile_pos
        for bp in self.data['factory_type']:
            if not bp['open']: continue
            factory_width = bp['dim']['w']
            factory_hight = bp['dim']['h']
            if 'plan' in bp.keys():
                factory_plan = np.transpose(np.array(bp['plan']))
                if np.sum(factory_plan) == 0:
                    continue
            else:
                continue
            for find_x in range(x-factory_width+1, x+1):
                for find_y in range(y-factory_hight+1, y+1):

                    if not self.onMap(find_x, find_y):
                        continue
                    if not self.onMap(find_x+factory_width, find_y+factory_hight):
                        continue
                    lookup = self.building_map[find_x:find_x +
                                               factory_width, find_y:find_y + factory_hight]
                    if np.all(lookup == factory_plan):
                        self.app.factories.add(
                            bp, self.building_map, find_x, find_y)

    def mapping(self, scPos):
        tilepos = (self.pos[0]+scPos[0]//TILE-HALF_WIDTH, self.pos[1]+(scPos[1]-P_UP)//TILE -
                   HALF_HIGHT)
        if tilepos[0] < 0 or tilepos[1] < 0 or tilepos[0] > PLANET_WIDTH-1 or tilepos[1] > PLANET_HIGHT-1:
            return ()
        else:
            return (tilepos)

    def demapping(self, tile_pos):
        if not self.onMap(tile_pos[0], tile_pos[1]):
            return()
        screen_pos = (
            (tile_pos[0]-self.pos[0]+HALF_WIDTH)*TILE,
            (tile_pos[1]-self.pos[1]+HALF_HIGHT)*TILE
        )
        return(screen_pos)

    # def select(self, mouse_coord):
    #     a = self.mapping(mouse_coord)
        # self.selection[0] = self.pos[0]+a[0]-HALF_HIGHT
        # self.selection[1] = self.pos[1]+a[1]-HALF_WIDTH
        # data = self.data.get('terrain_type')[self.field[self.selection[0], self.selection[1]]]['name']
        # pic = self.data.get('terrain_type')[self.field[self.selection[0], self.selection[1]]]['id']

        # self.text = f'Coordinate {self.selection}<br>{data}'

        # self.app.info.set(self.text, pic)

    def Get_info_block_placed(self, use_item, place):
        result_item = use_item
        result_type = ''
        if not use_item: return(None, '')
        for item in self.data.get('block_type'):
            if use_item['id'] == item['id']:
                rules = item.get('build', False)
                if rules:
                    rule = rules.get(place)
                    if rule:  # {'id':'1','count':3}
                        result_type = rule.get('type')
                        if not result_type:
                            result_type = 'block'
                        result_item_name = rule.get('result')
                        # if not result: result = self.FindInfo('id', use_item['id'], result_type)
                        result_item = {'id': self.FindInfo(
                            'id', result_item_name, result_type), 'count': 1}

                    elif rule == {}:  # {}
                        result_type = 'block'
                        break
                    else:  # None
                        break
        return(result_item, result_type)

    def view_Tileinfo(self, tilepos=()):
        # if not tilepos:
        #     pic_idx = self.FindTInfo('id', 'hyperspace')
        #     data = self.GetInfo('name', pic_idx)
        #     # self.app.info.set(self.text, pic_idx)
        #     self.app.info.start()
        #     self.app.info.append_pic(self.field_img[pic_idx][0])
        #     self.app.info.append_text(f'<b>{data}</b><br>(???,???)')
        #     self.app.info.stop()
        #     return

        # if self.dark_cover[tilepos]:
        #     self.app.info.start()
        #     self.app.info.append_text(f'Территория не открыта')
        #     self.app.info.stop()
        #     return

        # select_terrain = self.field[tilepos[0], tilepos[1]]
        # select_building = self.building_map[tilepos[0], tilepos[1]]
        # self.app.info.start()

        # terrain_data = self.GetTData('id', select_terrain)
        # terrain_name = terrain_data['name']
        # terrain_pic = self.field_img[select_terrain][0]

        # self.app.info.append_pic(terrain_pic)
        # self.app.info.append_text(f'<b>{terrain_name}</b><br>{tilepos}</b>')

        # if strtobool(self.GetTileInfo('allow_dig', tilepos)) and select_building == 0:
        #     time = terrain_data['dig']['time']
        #     loot = terrain_data['dig']['loot']
        #     self.app.info.append_text('Ожидаемые ресурсы:')
        #     self.app.info.append_list_items(loot)
        #     self.app.info.append_text(f'Время добычи(сек): {time}')

        # if select_building > 0:
        #     block_data = self.GetBData('id', select_building)
        #     block_name = block_data['name']
        #     time = block_data['demolition']
        #     loot = select_building
        #     lootcount = 1
        #     self.app.info.append_item(
        #         {'id': select_building, 'count': -1}, justify='center')
        #     self.app.info.append_text(f'<b>{block_name}</b>')
        #     self.app.info.append_text('Ресурсы при разборе:')
        #     self.app.info.append_item(
        #         {'id': loot, 'count': lootcount}, 'item_label_m')
        #     self.app.info.append_text(f'Время разбора(сек): {time}')
        pass

    def view_Build_info(self, tilepos):
        if not tilepos:
            pic_idx = self.FindTInfo('id', 'hyperspace')
            data = self.GetInfo('name', pic_idx)
            self.app.info.start()
            self.app.info.append_pic(self.field_img[pic_idx][0])
            self.app.info.append_text(f'<b>{data}</b><br>(???,???)')
            self.app.info.stop()
            return

        if self.dark_cover[self.tile_pos]:
            return

        selected_item = self.app.player.inv.item
        select_terrain = self.field[tilepos[0], tilepos[1]]
        select_building = self.building_map[tilepos[0], tilepos[1]]

        self.app.info.start()
        self.app.info.append_item(selected_item, justify='center')
        self.app.info.stop()

    def Get_img(self, item, b_type):
        if b_type == 'terrain':
            return(self.field_img[item['id']][0])
        elif b_type == 'block':
            return(self.block_img[item['id']])

    def update(self):
        if not self.app.is_modal(self): return

        pos_change = False
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            dx = -1
            dy = 0
            pos_change = True
            # self.pos[0] += -1
        if keystate[pg.K_d]:
            dx = 1
            dy = 0
            pos_change = True
            # self.pos[0] += 1

        if keystate[pg.K_w]:
            # self.pos[1] += -1
            dx = 0
            dy = -1
            pos_change = True

        if keystate[pg.K_s]:
            # self.pos[1] += 1
            dx = 0
            dy = 1
            pos_change = True
        if pos_change and self.onMap(self.pos[0]+dx, self.pos[1]+dy):
            self.pos = (self.pos[0]+dx, self.pos[1]+dy)

        if keystate[pg.K_HOME]:
            self.app.player.go_spawn()
         

        if self.app.inv_recipe.is_open: return
        if self.app.inv_toolbar.is_hover: return
        if self.app.inv_place_block.is_open: return
        
        if self.app.ui_tech_bp.visible: return
        

        if not self.app.inv_toolbar.item is None: 
            if not self.app.inv_toolbar.item['id']==TOOL_REMOVE: return
            
        mouse_status_type = self.app.mouse.status['tile_action']
        mouse_status_button = self.app.mouse.status['button']
        mouse_status_area = self.app.mouse.status['area']

        if mouse_status_type==MOUSE_TYPE_CLICK and mouse_status_button==MOUSE_RBUTTON: # Rigth mouse button click
            self.app.inv_toolbar.unselect()
            self.app.mouse.setcursor_noitem()
            # self.app.mouse.setcursor(cursor_type.normal)

            
        if mouse_status_type==MOUSE_TYPE_DRAG and mouse_status_button==MOUSE_LBUTTON: # Rigth mouse button click
            pass



    def draw(self):
        # draw bg
        self.surface.blit(self.field_bg, self.field_bgrect)
        
        
        # draw field and buildings
        for y in range(self.pos[1]-HALF_HIGHT, self.pos[1]+HALF_HIGHT+1):
            for x in range(self.pos[0]-HALF_WIDTH, self.pos[0]+HALF_WIDTH+1):
                if not self.onMap(x, y):
                    continue
                xyRect = pg.Rect(
                    (x-self.pos[0]+HALF_WIDTH)*TILE, (y-self.pos[1]+HALF_HIGHT)*TILE, TILE, TILE)
                
                if self.field[x, y] > 0:
                    field = self.app.data.data['terrain_type'][self.field[x, y]]
                    if self.operate[x, y]:
                        self.surface.blit(field['img'], xyRect)
                    else:
                        self.surface.blit(field['img_bw'], xyRect)
                if self.building_map[x, y] > 0:
                    factory = self.app.data.data['block_type'][self.building_map[x, y]]
                    self.surface.blit(factory['img'], xyRect)
                # self.app.info.debug(xyRect.move(0,P_UP), self.building_map[x,y])

        # draw factory
        self.app.factories.draw(self.surface)
        
        # draw tech areas
        self.app.ui_tech.draw(self.surface)
        
        # draw place areas
        self.app.player.draw(self.surface)


        # # draw selection
        # if self.selection != [-1, -1]:
        #     xyRect = pg.Rect((self.selection[0]-self.pos[0]+HALF_WIDTH)*TILE,
        #                      (self.selection[1]-self.pos[1]+HALF_HIGHT)*TILE, TILE, TILE)
        #     pg.draw.rect(self.surface, pg.Color('yellow'), xyRect, 3)

        # draw dig_site
        # if self.dig_site:
        #     xyRect = pg.Rect((self.dig_site[1]-self.pos[1]+HALF_WIDTH)*TILE,
        #                      (self.dig_site[0]-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
        #     pg.draw.rect(self.surface, pg.Color('gray'), xyRect, 1)

        # draw pointed field
        # if self.app.player.inv.selected_backpack_cell:
        if self.tile_pos:
            xyRect = pg.Rect((self.tile_pos[0]-self.pos[0]+HALF_WIDTH)*TILE,
                             (self.tile_pos[1]-self.pos[1]+HALF_HIGHT)*TILE, TILE, TILE)
            # cursor
            if self.app.player.inv.item is None and not self.app.inv_toolbar.is_hover and not self.app.inv_recipe.is_hover:
                if not self.app.player.inv.is_open: # and not self.app.inv_recipe.is_open:
                    pg.draw.rect(self.surface, pg.Color('gray'), xyRect, 1)
        
        # dark cover
        for y in range(self.pos[1]-HALF_HIGHT, self.pos[1]+HALF_HIGHT+1):
            for x in range(self.pos[0]-HALF_WIDTH, self.pos[0]+HALF_WIDTH+1):
                if not self.onMap(x, y):
                    continue
                xyRect = pg.Rect(
                    (x-self.pos[0]+HALF_WIDTH)*TILE, (y-self.pos[1]+HALF_HIGHT)*TILE, TILE, TILE)

                if self.dark_cover[x, y]:
                    self.surface.blit(self.app.data.data['terrain_type'][0]['img'], xyRect)

        # draw cursor area
        # if self.app.mouse.status['area']:
        #     if self.app.mouse.status['area'].size!=(1,1):
        #         area = self.app.mouse.status['area']
        #         for i in range(area.left, area.right):
        #             for j in range(area.top, area.bottom):
        #                 screen_pos = self.app.terrain.demapping((i,j))
        #                 f_rect = pg.Rect(screen_pos, (TILE, TILE))
        #                 if self.allow:
        #                     self.surface.blit(self.bg_blue, f_rect.topleft)
        #                 else:
        #                     self.surface.blit(self.bg_red, f_rect.topleft)


        # draw in viewport
        self.app.screen.blit(self.surface, VIEW_RECT)

    def dig_succes(self, player, tile_pos):
        self.app.player.stop_dig()
        site = self.field[tile_pos[0], tile_pos[1]]
        diginfo = self.GetInfo('dig', site)
        loot = diginfo['loot']
        self.field[tile_pos[0], tile_pos[1]] = self.FindTInfo(
            'id', diginfo['after'])
        for iLoot in loot:
            player.pickup(iLoot['id'], iLoot['count'])

    def demolition_succes(self, player, tile_pos):
        site = self.building_map[tile_pos[0], tile_pos[1]]
        if site == -1:  # demolition factory
            select_factory = self.app.factories.factory(tile_pos)
            # resourses = select_factory.get_resources(100, 100)
            # i = 0
            # for count in resourses[1]:
            #     if resourses[0][i] != 0 and resourses[0][i]:
            #         player.pickup(resourses[0][i], count)
            #     i += 1
            self.app.factories.delete(self.building_map, select_factory)

        if site > 0:  # demolition block
            player.pickup(site, 1)
            self.building_map[tile_pos[0], tile_pos[1]] = 0
            self.app.ui_tech.refresh_site_content(tile_pos)

        # diginfo = self.GetBInfo('dig',site)

        # loot =  self.FindBInfo('id', diginfo['loot'])
        # self.field[tile_pos[0], tile_pos[1]] = self.FindTInfo('id', diginfo['after'])
        # player.pickup(loot, diginfo['count'])

    def set_discover(self, x: int, y: int, radius):

        for i in range(-radius, radius):
            for j in range(-radius, radius):
                if (i+0.5)*(i+0.5)+(j+0.5)*(j+0.5) <= radius*radius:
                    if self.onMap(i+x, j+y):
                        self.dark_cover[ceil(i+x), ceil(j+y)] = False

    def set_operate(self, x, y, radius, value=1):
        for i in range(-radius, radius):
            for j in range(-radius, radius):
                if (i+0.5)*(i+0.5)+(j+0.5)*(j+0.5) <= radius*radius:
                    if self.onMap(i+x, j+y):
                        self.operate[ceil(i+x), ceil(j+y)] += value
        
    def water_arround(self, pos):
        def _is_water(pos):
            water_id = self.GetTData('name', 'water')['id']
            if self.onMap(pos[0], pos[1]):
                return self.field[pos]==water_id
            else:
                return False
            
        result = False
        result = _is_water((pos[0]-1, pos[1])) or result
        result = _is_water((pos[0]+1, pos[1])) or result
        result = _is_water((pos[0], pos[1]-1)) or result
        result = _is_water((pos[0], pos[1]+1)) or result
        return result

    
        