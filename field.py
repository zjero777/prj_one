from typing import Mapping
import numpy as np
from numpy.lib.function_base import append, select
import pygame as pg
import random as rnd
import json

from pygame.event import Event

from info import info
from options import *


class field:
    def __init__(self, app, width, height, pos=[50,50]):
        self.app = app
        self.pos = [pos[0], pos[1]]
        self.selection = [0,0]
        self.mouseclick = 0,0
        self.mousebutton = 0
        self.surface = pg.Surface((FIELD_WIDTH, FIELD_HIGHT))
        self.field = np.zeros((height, width), dtype='i')
        self.building_map = np.zeros((height, width), dtype='i')
        self.field.fill(1)
        for i in range(100):
            self.field[rnd.randint(0,99), rnd.randint(0,99)] = 0

        for i in range(100):
            self.building_map[rnd.randint(0,99), rnd.randint(0,99)] = rnd.randrange(1, 3)

        #self.field[50, 50] = 1
        #for i in range(100):
        #    self.field[i,0] = 1
        #    self.field[i,99] = 1
        #    self.field[0,i] = 1
        #   self.field[99,i] = 1

        
        
        self.field_img = []
        self.field_img = append(self.field_img, 0)
        self.field_img = append(self.field_img, pg.image.load(path.join(img_dir, "e1.png")).convert())
        self.field_rect = self.field_img[1].get_rect()        

        self.building_img = []
        self.building_img = append(self.building_img, 0)
        self.building_img = append(self.building_img, pg.image.load(path.join(img_dir, "b1.png")).convert_alpha())
        self.building_img = append(self.building_img, pg.image.load(path.join(img_dir, "b2.png")).convert_alpha())
        self.building_img_rect = self.building_img[1].get_rect()        

        
        self.field_bg = pg.image.load(path.join(img_dir, "bg.jpg")).convert()
        self.field_bgrect = self.field_bg.get_rect()
        
        f = open('data/data.json',)
        self.data = json.load(f)
        f.close
        

    def mapping(self, scPos):
        return [self.pos[0]+(scPos[1]-P_UP)//TILE-HALF_HIGHT, self.pos[1]+scPos[0]//TILE-HALF_WIDTH]

    
    def select(self, mouse_coord):
        a = self.mapping(mouse_coord)
        # self.selection[0] = self.pos[0]+a[0]-HALF_HIGHT
        # self.selection[1] = self.pos[1]+a[1]-HALF_WIDTH
        # data = self.data.get("terrain_type")[self.field[self.selection[0], self.selection[1]]]['name']
        # pic = self.data.get("terrain_type")[self.field[self.selection[0], self.selection[1]]]['id']
        
        # self.text = f'Coordinate {self.selection}<br>{data}'
        
        # self.app.info.set(self.text, pic)
    
    def view_Tileinfo(self, tilepos):
        if tilepos[0]<0 or tilepos[1]<0 or tilepos[0]>PLANET_WIDTH-1 or tilepos[1]>PLANET_HIGHT-1: 
            pic = self.data.get("terrain_type")[2]['id']
            data = self.data.get("terrain_type")[2]['name']
            self.text = f'(???,???)<br>{data}'
            self.app.info.set(self.text, pic)
            return
        data = self.data.get("terrain_type")[self.field[tilepos[0], tilepos[1]]]['name']
        pic = self.data.get("terrain_type")[self.field[tilepos[0], tilepos[1]]]['id']
        
        self.text = f'{tilepos}<br>{data}'
        
        self.app.info.set(self.text, pic)
    
    def pointInRect(self, point,rect):
        x1, y1, w, h = rect
        x2, y2 = x1+w, y1+h
        x, y = point
        if (x1 < x and x < x2):
            if (y1 < y and y < y2):
                return True
        return False    
    
    def process_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.pointInRect(event.pos, VIEW_RECT):
                self.mouseclick = event.pos
                self.mousebutton = event.button
                self.select(event.pos)
        if event.type == pg.MOUSEMOTION:
            if self.pointInRect(event.pos, VIEW_RECT):
                # self.mousebutton = event.button
                # self.select(event.pos)
                self.view_Tileinfo(self.mapping(event.pos))
            
                
        
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
            

     
            
        
    def draw(self):
        self.surface.blit(self.field_bg, self.field_bgrect)
        for y in range(self.pos[0]-HALF_HIGHT,self.pos[0]+HALF_HIGHT+1):
            for x in range(self.pos[1]-HALF_WIDTH,self.pos[1]+HALF_WIDTH+1):
                xyRect = pg.Rect((x-self.pos[1]+HALF_WIDTH)*TILE,(y-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
                if (x<0) or (y<0) or (x>=self.field.shape[1]) or (y>=self.field.shape[0]): continue
                if self.field[y,x]!=0: 
                    self.surface.blit(self.field_img[self.field[y,x]], xyRect)
                if self.building_map[y,x]!=0: 
                    self.surface.blit(self.building_img[self.building_map[y,x]], xyRect)
        xyRect = pg.Rect((self.selection[1]-self.pos[1]+HALF_WIDTH)*TILE,(self.selection[0]-self.pos[0]+HALF_HIGHT)*TILE, TILE, TILE)
        pg.draw.rect(self.surface, pg.Color('yellow'), xyRect, 3)
        self.app.screen.blit(self.surface, VIEW_RECT)
        
        
  
    