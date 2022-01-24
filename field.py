from distutils.command import build
from distutils.util import strtobool
import numpy as np
from numpy.lib.function_base import append, select
import pygame as pg
import random as rnd
import json

from pygame.event import Event

from info import info
from options import *

class field:
    def __init__(self, app, width, height, pos=[50, 50]):
        self.app = app
        self.pos = [pos[0], pos[1]]
        self.selection = [-1, -1]
        self.dig_site = ()
        # self.mouseclick = 0,0
        # self.mousebutton = 0
        self.surface = pg.Surface((FIELD_WIDTH, FIELD_HIGHT))
        self.field = np.zeros((height, width), dtype='i')
        self.building_map = np.zeros((height, width), dtype='i')
        self.first_click = True
        
        f = open('data/data.json',)
        self.data = json.load(f)
        f.close
        
       
        self.field.fill(self.FindTInfo("id", "ground"))

        for i in range(100):
            self.field[rnd.randint(0,99), rnd.randint(0,99)] = 0

        # for i in range(100):
        #     self.building_map[rnd.randint(0,99), rnd.randint(0,99)] = rnd.randrange(1, 3)

        #self.field[50, 50] = 1
        # for i in range(100):
        #    self.field[i,0] = 1
        #    self.field[i,99] = 1
        #    self.field[0,i] = 1
        #   self.field[99,i] = 1

        
        self.field_img = [0 for i in self.data['terrain_type']]
        for img in self.data['terrain_type']:
            self.field_img[img['id']] = (pg.image.load(path.join(img_dir, img['pic'])).convert())
        self.field_rect = self.field_img[0].get_rect()

        self.building_img = [0 for i in self.data['building_type']]
        for img in self.data['building_type']:
            self.building_img[img['id']] = (pg.image.load(path.join(img_dir, img['pic'])).convert_alpha())
        self.building_img_rect = self.building_img[1].get_rect()

        self.field_bg = pg.image.load(path.join(img_dir, "bg.jpg")).convert()
        self.field_bgrect = self.field_bg.get_rect()


    def mapping(self, scPos):
        tilepos = (self.pos[0]+(scPos[1]-P_UP)//TILE-HALF_HIGHT, self.pos[1]+scPos[0]//TILE-HALF_WIDTH)
        if tilepos[0] < 0 or tilepos[1] < 0 or tilepos[0] > PLANET_WIDTH-1 or tilepos[1] > PLANET_HIGHT-1:
            return ()
        else:
            return (tilepos)

    def select(self, mouse_coord):
        a = self.mapping(mouse_coord)
        # self.selection[0] = self.pos[0]+a[0]-HALF_HIGHT
        # self.selection[1] = self.pos[1]+a[1]-HALF_WIDTH
        # data = self.data.get("terrain_type")[self.field[self.selection[0], self.selection[1]]]['name']
        # pic = self.data.get("terrain_type")[self.field[self.selection[0], self.selection[1]]]['id']

        # self.text = f'Coordinate {self.selection}<br>{data}'

        # self.app.info.set(self.text, pic)
    def GetTileInfo(self, name, tilepos):
        if not tilepos:
            pic_idx = self.FindTInfo("id", "hyperspace")
            return (self.GetInfo(name, pic_idx))

        return(self.data.get("terrain_type")[self.field[tilepos[0], tilepos[1]]][name])

    def GetInfo(self, name, id):
        return(self.data.get("terrain_type")[id][name])

    def FindBInfo(self, name, stroke):
        for item in self.data.get("building_type"):
            if item['name'] == stroke:
                return(item[name])

    def FindTInfo(self, name, stroke):
        for item in self.data.get("terrain_type"):
            if item['name'] == stroke:
                return(item[name])
            
    def FindInfo(self, name, stroke, build_type):
        if build_type=='building':
            return(self.FindBInfo(name, stroke))
        elif build_type=='terrain':
            return(self.FindTInfo(name, stroke))
        
    def Get_info_build_placed(self, use_item, place):
        for item in self.data.get("terrain_type"):
            if item['id']==use_item['item']: 
                type_result = ''
                rule = item.get('build',False)
                if rule:
                    for item_rule in rule:
                        if place in item_rule:
                            type_result = item_rule.get('type_result','terrain')
                            result_item_idx = self.FindInfo('id', item_rule[place], type_result)
                            return({'item':result_item_idx}, type_result)
                    else:
                        return(use_item, type_result)
                else:
                    return(use_item, type_result)
           

    def view_Tileinfo(self, tilepos):
        if not tilepos:
            pic_idx = self.FindTInfo("id", "hyperspace")
            data = self.GetInfo("name", pic_idx)
            self.text = f'(???,???)<br>{data}'
            self.app.info.set(self.text, pic_idx)
            return

        data = self.GetTileInfo("name", tilepos)
        pic_idx = self.GetTileInfo("id", tilepos)

        self.text = f'{tilepos}<br>{data}'

        self.app.info.set(self.text, pic_idx)

    # def process_events(self, event):
    #     if event.type == pg.MOUSEBUTTONDOWN:
    #         if pointInRect(event.pos, VIEW_RECT):
    #             self.mouseclick = event.pos
    #             self.mousebutton = event.button
    #             self.select(event.pos)
    #     if event.type == pg.MOUSEMOTION:
    #         if pointInRect(event.pos, VIEW_RECT):
    #             # self.mousebutton = event.button
    #             # self.select(event.pos)
    #             self.view_Tileinfo(self.mapping(event.pos))

    def Get_img(self, item, build_type):
        if build_type=='terrain':
            return(self.field_img[item['item']])
        elif build_type=='building':
            return(self.building_img[item['item']])
    
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
            
            self.view_Tileinfo(self.tile_pos)
            
            if not mouse_button[0]: self.first_click = True
            self.app.info.debug((0,60), f'{self.first_click}')
            if mouse_button[0] and len(self.tile_pos)>0:
                if self.app.player.inv.selected_Item>-1:
                    
                    if self.first_click:
                        self.first_click = False 

                        # build
                        if self.building_map[self.tile_pos[0], self.tile_pos[1]] == 0:
                            self.build(self.app.player, self.tile_pos)
                    
                        
                        
                else:
                    if self.first_click:
                        # dig
                        if self.building_map[self.tile_pos[0], self.tile_pos[1]] == 0 and strtobool(self.GetTileInfo('allow_dig', self.tile_pos)):
                            self.app.player.manual_dig(self, self.tile_pos)
                            self.dig_site = self.tile_pos

                # building select
            else:
                self.app.player.stop_dig()
                self.dig_site = ()
                
                
            if mouse_button[2] and not mouse_button[0] and len(self.tile_pos)>0:
                self.app.player.inv.selected_Item=-1
                self.app.player.inv.item = {}
        else:
            self.app.player.stop_dig()
            self.dig_site = ()
                
            

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
                if self.field[y, x] != 0:
                    self.surface.blit(self.field_img[self.field[y, x]], xyRect)
                if self.building_map[y, x] != 0:
                    self.surface.blit(
                        self.building_img[self.building_map[y, x]], xyRect)

        # draw selection
        if self.selection != [-1, -1]:
            xyRect = pg.Rect((self.selection[1]-self.pos[1]+HALF_WIDTH)*TILE,
                             (self.selection[0]-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
            pg.draw.rect(self.surface, pg.Color('yellow'), xyRect, 3)
            

        # draw dig_site
        if self.dig_site:
            xyRect = pg.Rect((self.dig_site[1]-self.pos[1]+HALF_WIDTH)*TILE,
                             (self.dig_site[0]-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
            pg.draw.rect(self.surface, pg.Color('gray'), xyRect, 1)
            
        # draw pointed field
        # if self.app.player.inv.selected_Item:
        if self.tile_pos:
            xyRect = pg.Rect((self.tile_pos[1]-self.pos[1]+HALF_WIDTH)*TILE,
                             (self.tile_pos[0]-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
            if self.app.player.inv.selected_Item==-1:
                pg.draw.rect(self.surface, pg.Color('gray'), xyRect, 1)
            else:
                # Ghost cursor
                item = self.app.player.inv.item
                place = self.GetInfo('name', self.field[self.tile_pos[0], self.tile_pos[1]])
                build_item, build_type = self.Get_info_build_placed(item, place)
                
                if build_type:
                    img = self.Get_img(build_item, build_type).copy()
                    img.set_alpha(172)
                    self.surface.blit(img, xyRect, special_flags=pg.BLEND_MULT)
                else:
                    img = self.Get_img(build_item, 'terrain').copy()
                    img.set_alpha(172)
                    colorImage = pg.Surface(img.get_size()).convert_alpha()
                    colorImage.fill(pg.Color('red'))
                    img.blit(colorImage, (0,0), special_flags = pg.BLEND_RGBA_MULT)
                    self.surface.blit(img, xyRect, special_flags=pg.BLEND_MULT)
                    
        

        # draw in viewport
        self.app.screen.blit(self.surface, VIEW_RECT)

    def dig_succes(self, player, tile_pos):
        loot = self.field[tile_pos[0], tile_pos[1]]
        self.field[tile_pos[0], tile_pos[1]] = self.FindTInfo("id", "pit")
        player.pickup(loot)
        
    # Place the item selected from the inventory on the ground
    # player.inv.selected_Item - selected inventory item 
    # tile_pos - place for installation
    def build(self, player, tile_pos):
        if player.inv.selected_Item>-1:
            item = self.app.player.inv.item
            place = self.GetInfo('name', self.field[self.tile_pos[0], self.tile_pos[1]])
            build_item, build_type = self.Get_info_build_placed(item, place)   
            if build_type=='terrain':
                self.field[tile_pos[0], tile_pos[1]] = build_item['item']
                player.use_selected()
            elif build_type=='building':
                self.building_map[tile_pos[0], tile_pos[1]]=build_item['item']
                player.use_selected()
                
            

                    
                    
                    
                
            