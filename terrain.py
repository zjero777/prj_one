from distutils.util import strtobool
import numpy as np
from numpy.lib.function_base import append, select
import pygame as pg
import random as rnd
import json
import pygame_gui as gui

from pygame.event import Event
from factory import factory_list

from info import info
from options import *


class terrain:
    def __init__(self, app, width, height, pos=[50, 50]):
        self.app = app
        self.pos = [pos[0], pos[1]]
        self.selection = [-1, -1]
        self.surface = pg.Surface((FIELD_WIDTH, FIELD_HIGHT))
        self.field = np.zeros((height, width), dtype='i')
        self.building_map = np.zeros((height, width), dtype='i')
        self.first_click = True
        self.tile_pos = ()
        f = open('data/data.json',)
        self.data = json.load(f)
        f.close

        self.field.fill(self.FindTInfo('id', 'ground'))

        for i in range(100):
            self.field[rnd.randint(0, 99), rnd.randint(0, 99)] = 0

        for i in range(100):
            self.building_map[rnd.randint(0, 99), rnd.randint(
                0, 99)] = rnd.randrange(1, 3)

        #self.field[50, 50] = 1
        # for i in range(100):
        #    self.field[i,0] = 1
        #    self.field[i,99] = 1
        #    self.field[0,i] = 1
        #   self.field[99,i] = 1

        self.field_img = [0 for i in self.data['terrain_type']]
        for img in self.data['terrain_type']:
            self.field_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert())
        self.field_rect = self.field_img[0].get_rect()

        self.block_img = [0 for i in self.data['block_type']]
        for img in self.data['block_type']:
            self.block_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())
        self.block_img_rect = self.block_img[1].get_rect()

        self.field_bg = pg.image.load(path.join(img_dir, 'bg.jpg')).convert()
        self.field_bgrect = self.field_bg.get_rect()

    def onMap(self, tile_x, tile_y):
        return(not tile_x < 0 or tile_y < 0 or tile_x > PLANET_WIDTH-1 or tile_y > PLANET_HIGHT-1)

    def complete_factory(self):
        x, y = self.tile_pos
        for bp in self.data['factory_type']:
            factory_width = bp['dim']['w']
            factory_hight = bp['dim']['h']
            factory_plan = np.array(bp['plan'])
            for find_x in range(x-factory_width+1, x+1):
                for find_y in range(y-factory_hight+1, y+1):
                    if not self.onMap(find_x, find_y):
                        continue
                    if not self.onMap(find_x+factory_width, find_y+factory_hight):
                        continue
                    lookup = self.building_map[find_x:find_x +
                                               factory_width, find_y:find_y+factory_hight]
                    if np.all(lookup == factory_plan):
                        self.app.factories.add(
                            bp, self.building_map, find_x, find_y)

    def mapping(self, scPos):
        tilepos = (self.pos[0]+(scPos[1]-P_UP)//TILE -
                   HALF_HIGHT, self.pos[1]+scPos[0]//TILE-HALF_WIDTH)
        if tilepos[0] < 0 or tilepos[1] < 0 or tilepos[0] > PLANET_WIDTH-1 or tilepos[1] > PLANET_HIGHT-1:
            return ()
        else:
            return (tilepos)

    def demapping(self, tile_pos):
        if not self.onMap(tile_pos[0], tile_pos[1]):
            return()
        screen_pos = (
            (tile_pos[1]-self.pos[1]+HALF_WIDTH)*TILE,
            (tile_pos[0]-self.pos[0]+HALF_HIGHT)*TILE
        )
        return(screen_pos)

    def select(self, mouse_coord):
        a = self.mapping(mouse_coord)
        # self.selection[0] = self.pos[0]+a[0]-HALF_HIGHT
        # self.selection[1] = self.pos[1]+a[1]-HALF_WIDTH
        # data = self.data.get('terrain_type')[self.field[self.selection[0], self.selection[1]]]['name']
        # pic = self.data.get('terrain_type')[self.field[self.selection[0], self.selection[1]]]['id']

        # self.text = f'Coordinate {self.selection}<br>{data}'

        # self.app.info.set(self.text, pic)
    def GetTileInfo(self, name, tilepos):
        if not tilepos:
            pic_idx = self.FindTInfo('id', 'hyperspace')
            return (self.GetInfo(name, pic_idx))

        return(self.data.get('terrain_type')[self.field[tilepos[0], tilepos[1]]][name])

    def GetInfo(self, name, id):
        return(self.data.get('terrain_type')[id][name])

    def FindBInfo(self, name, stroke):
        for item in self.data.get('block_type'):
            if item['name'] == stroke:
                return(item[name])

    def GetBData(self, key, stroke):
        for item in self.data.get('block_type'):
            if item[key] == stroke:
                return(item)

    def GetTData(self, key, stroke):
        for item in self.data.get('terrain_type'):
            if item[key] == stroke:
                return(item)

    def GetFData(self, key, stroke):
        for item in self.data.get('factory_type'):
            if item[key] == stroke:
                return(item)

    def FindTInfo(self, name, stroke):
        for item in self.data.get('terrain_type'):
            if item['name'] == stroke:
                return(item[name])

    def FindInfo(self, name, stroke, b_type):
        if b_type == 'block':
            return(self.FindBInfo(name, stroke))
        elif b_type == 'terrain':
            return(self.FindTInfo(name, stroke))

    def Get_info_block_placed(self, use_item, place):
        for item in self.data.get('block_type'):
            if item['id'] == use_item['id']:
                type_result = ''
                rule = item.get('build', False)
                if rule:
                    for item_rule in rule:
                        if place in item_rule:
                            type_result = item_rule.get(
                                'type_result', 'terrain')
                            result_item_idx = self.FindInfo(
                                'id', item_rule[place], type_result)
                            return({'id': result_item_idx}, type_result)
                    else:
                        return(use_item, type_result)
                else:
                    return(use_item, type_result)

    def view_Tileinfo(self, tilepos):
        if not tilepos:
            pic_idx = self.FindTInfo('id', 'hyperspace')
            data = self.GetInfo('name', pic_idx)
            # self.app.info.set(self.text, pic_idx)
            self.app.info.start()
            self.app.info.append_pic(self.field_img[pic_idx])
            self.app.info.append_text(f'<b>{data}</b><br>(???,???)')
            self.app.info.stop()
            return

        select_terrain = self.field[tilepos[0], tilepos[1]]
        select_building = self.building_map[tilepos[0], tilepos[1]]
        terrain_data = self.GetTData('id', select_terrain)
        terrain_name = terrain_data['name']
        terrain_pic = self.field_img[select_terrain]

        dig_txt = ''
        demolition_txt = ''

        self.app.info.start()
        self.app.info.append_pic(terrain_pic)
        self.app.info.append_text(f'<b>{terrain_name}</b><br>{tilepos}</b>')

        if strtobool(self.GetTileInfo('allow_dig', tilepos)) and select_building == 0:
            time = terrain_data['dig']['time']
            loot = terrain_data['dig']['loot']
            lootcount = terrain_data['dig']['count']
            dig_txt = f'Ожидаемые ресурсы: {loot} - {lootcount} шт.<br>Время добычи: {time} сек.'
            self.app.info.append_text(dig_txt)
            # self.app.info.append_blockinfo(loot, lootcount)

        if select_building > 0:
            block_data = self.GetBData('id', select_building)
            block_name = block_data['name']
            block_pic = self.block_img[select_building]
            time = block_data['demolition']
            loot = block_data['name']
            lootcount = 1
            demolition_txt = f'Ресурсы при разборе: {loot} - {lootcount} шт.<br>Время разбора: {time} сек.'
            self.app.info.append_pic(block_pic)
            self.app.info.append_text(f'<b>{block_name}</b>')
            self.app.info.append_text(demolition_txt)

        self.app.info.stop()
        
    def view_Build_info(self, tilepos):
        if not tilepos:
            pic_idx = self.FindTInfo('id', 'hyperspace')
            data = self.GetInfo('name', pic_idx)
            # self.app.info.set(self.text, pic_idx)
            self.app.info.start()
            self.app.info.append_pic(self.field_img[pic_idx])
            self.app.info.append_text(f'<b>{data}</b><br>(???,???)')
            self.app.info.stop()
            return
        selected_item = self.app.player.inv.item
        select_terrain = self.field[tilepos[0], tilepos[1]]
        select_building = self.building_map[tilepos[0], tilepos[1]]
        
        self.app.info.start()
        # self.app.info.append_text(f'Строительство:')
        self.app.info.append_item(selected_item)
        # self.app.info.append_pic(self.block_img[pic_idx])
        
        self.app.info.stop()
        
        
    
    def Get_img(self, item, b_type):
        if b_type == 'terrain':
            return(self.field_img[item['id']])
        elif b_type == 'block':
            return(self.block_img[item['id']])

    def update(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.pos[1] += -1
        if keystate[pg.K_d]:
            self.pos[1] += 1
        if keystate[pg.K_w]:
            self.pos[0] += -1
        if keystate[pg.K_s]:
            self.pos[0] += 1
        if self.pos[1] > self.field.shape[0]-1:
            self.pos[1] = self.field.shape[0]-1
        if self.pos[1] < 0:
            self.pos[1] = 0

        if self.pos[0] > self.field.shape[1]-1:
            self.pos[0] = self.field.shape[1]-1
        if self.pos[0] < 0:
            self.pos[0] = 0

        mouse_button = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        if pg.Rect(VIEW_RECT).collidepoint(mouse_pos) and not self.app.player.is_openinv:
            self.tile_pos = self.mapping(mouse_pos)
            if self.app.player.inv.selected_Item == -1:
                self.view_Tileinfo(self.tile_pos)
            else:
                self.view_Build_info(self.tile_pos)

            if not mouse_button[0]:
                self.first_click = True
            # self.app.info.debug((0,60), f'{self.first_click}')

            if mouse_button[0] and len(self.tile_pos) > 0:
                if self.app.player.inv.selected_Item > -1:

                    if self.first_click:
                        self.first_click = False

                        # build
                        if self.building_map[self.tile_pos[0], self.tile_pos[1]] == 0:
                            self.app.player.build(self)
                            self.complete_factory()

                else:

                    if self.first_click:
                        select_building = self.building_map[self.tile_pos[0],
                                                            self.tile_pos[1]]
                        select_terrain = self.field[self.tile_pos[0],
                                                    self.tile_pos[1]]
                        select_factory = self.app.factories.factory(
                            self.tile_pos)
                        # dig
                        if select_building == 0 and strtobool(self.GetTileInfo('allow_dig', self.tile_pos)):
                            data = self.GetTData('id', select_terrain)
                            time = data['dig']['time']
                            if self.app.player.manual_dig(self, self.tile_pos, time):
                                self.first_click = True
                        # demolition
                        elif select_building > 0:
                            data = self.GetBData('id', select_building)
                            time = data['demolition']
                            if self.app.player.manual_demolition(self, self.tile_pos, time):
                                self.first_click = False
                        elif select_factory:
                            time = select_factory.demolition
                            if self.app.player.manual_demolition(self, self.tile_pos, time):
                                self.first_click = False

                        else:
                            self.app.player.stop_dig()
                            self.app.player.stop_demolition()

                        # building select
                    else:
                        self.app.player.stop_dig()
                        self.app.player.stop_demolition()
            else:
                self.app.player.stop_dig()
                self.app.player.stop_demolition()

            if mouse_button[2] and not mouse_button[0] and len(self.tile_pos) > 0:
                self.app.player.inv.selected_Item = -1
                self.app.player.inv.item = {}
        else:
            self.app.player.stop_dig()
            self.app.player.stop_demolition()

    def draw(self):
        # draw bg
        self.surface.blit(self.field_bg, self.field_bgrect)
        # draw field and buildings
        for y in range(self.pos[0]-HALF_HIGHT, self.pos[0]+HALF_HIGHT+1):
            for x in range(self.pos[1]-HALF_WIDTH, self.pos[1]+HALF_WIDTH+1):
                if (x < 0) or (y < 0) or (x >= self.field.shape[1]) or (y >= self.field.shape[0]):
                    continue
                xyRect = pg.Rect(
                    (x-self.pos[1]+HALF_WIDTH)*TILE, (y-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
                if self.field[y, x] > 0:
                    self.surface.blit(self.field_img[self.field[y, x]], xyRect)
                if self.building_map[y, x] > 0:
                    self.surface.blit(
                        self.block_img[self.building_map[y, x]], xyRect)

        # draw factory
        self.app.factories.draw(self.surface)

        # draw selection
        if self.selection != [-1, -1]:
            xyRect = pg.Rect((self.selection[1]-self.pos[1]+HALF_WIDTH)*TILE,
                             (self.selection[0]-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
            pg.draw.rect(self.surface, pg.Color('yellow'), xyRect, 3)

        # draw dig_site
        # if self.dig_site:
        #     xyRect = pg.Rect((self.dig_site[1]-self.pos[1]+HALF_WIDTH)*TILE,
        #                      (self.dig_site[0]-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
        #     pg.draw.rect(self.surface, pg.Color('gray'), xyRect, 1)

        # draw pointed field
        # if self.app.player.inv.selected_Item:
        if self.tile_pos:
            xyRect = pg.Rect((self.tile_pos[1]-self.pos[1]+HALF_WIDTH)*TILE,
                             (self.tile_pos[0]-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
            if self.app.player.inv.selected_Item == -1:
                if not self.app.player.is_openinv:
                    pg.draw.rect(self.surface, pg.Color('gray'), xyRect, 1)
            else:
                if not self.app.player.is_openinv:
                    # Ghost cursor
                    item = self.app.player.inv.item
                    place = self.GetInfo(
                        'name', self.field[self.tile_pos[0], self.tile_pos[1]])
                    build_item, b_type = self.Get_info_block_placed(item, place)

                    if b_type:
                        img = self.Get_img(build_item, b_type).copy()
                        img.set_alpha(172)
                        self.surface.blit(img, xyRect)
                    else:
                        img = self.Get_img(build_item, 'terrain').copy()
                        img.set_alpha(172)
                        colorImage = pg.Surface(img.get_size()).convert_alpha()
                        colorImage.fill(pg.Color('red'))
                        img.blit(colorImage, (0, 0),
                                special_flags=pg.BLEND_RGBA_MULT)
                        self.surface.blit(
                            img, xyRect, special_flags=pg.BLEND_RGBA_MIN)

        # draw in viewport
        self.app.screen.blit(self.surface, VIEW_RECT)

    def dig_succes(self, player, tile_pos):
        self.app.player.stop_dig()
        site = self.field[tile_pos[0], tile_pos[1]]
        diginfo = self.GetInfo('dig', site)
        loot = self.FindBInfo('id', diginfo['loot'])
        self.field[tile_pos[0], tile_pos[1]] = self.FindTInfo(
            'id', diginfo['after'])
        player.pickup(loot, diginfo['count'])

    def demolition_succes(self, player, tile_pos):
        site = self.building_map[tile_pos[0], tile_pos[1]]
        if site == -1:  # demolition factory
            select_factory = self.app.factories.factory(tile_pos)
            resourses = select_factory.get_resources(100, 100)
            i = -1
            for count in resourses[1]:
                i += 1
                player.pickup(resourses[0][i], count)

            self.app.factories.delete(self.building_map, select_factory)

        if site > 0:  # demolition block
            player.pickup(site, 1)
            self.building_map[tile_pos[0], tile_pos[1]] = 0

        # diginfo = self.GetBInfo('dig',site)

        # loot =  self.FindBInfo('id', diginfo['loot'])
        # self.field[tile_pos[0], tile_pos[1]] = self.FindTInfo('id', diginfo['after'])
        # player.pickup(loot, diginfo['count'])
