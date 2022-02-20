from typing import Tuple
import pygame as pg
from options import *
import random as rnd
import numpy as np


class factory:
    def __init__(self, list, app, blueprint,  x, y):
        self.app = app
        self.list = list
        self.id = blueprint['id']
        self.name = blueprint['name']
        self.tile_pos = (x, y)
        self.size = (blueprint['dim']['h'], blueprint['dim']['w'])
        self.plan = np.array(blueprint['plan'])
        self.demolition = blueprint['demolition']
        self.pic = list.factory_img[blueprint['id']]
        self.incom = blueprint['in']
        self.outcom = (blueprint['out'])
        self.process_time = blueprint['time']
        self.working = False
        self.timer = app.timer
        self.time = 0
        
        
    def get_resources(self, minproc=100, maxproc=100):
        if minproc==maxproc: 
            proc=maxproc
        else:
            proc = rnd.randrange(minproc, maxproc)
        res, count = np.unique(self.plan, return_counts=True)
        all_res = (res, np.int64(count*(proc/100)))
        return(all_res)
    
    @property
    def demolition_list_items_100(self):
        res = self.get_resources()
        list_items = []
        i=0
        for item in res[0]:
            if item!=0:
                list_items.append({'id':item,'count':res[1][i]})
            i+=1
        return(list_items)
    
    def draw(self, surface):
        screen_pos = self.app.terrain.demapping(self.tile_pos)
        f_rect = pg.Rect(screen_pos, (self.size[0]*TILE, self.size[1]*TILE))
        if pg.Rect(VIEW_RECT).colliderect(f_rect):
            surface.blit(self.pic, f_rect)
            
    def update(self):
        if not self.working:
            if self.app.player.inv.exist(self.incom):
                self.app.player.inv.delete(self.incom)
                self.time = self.timer.get_ticks()
                self.working = True
        else:
            if self.timer.get_ticks()-self.time>self.process_time*1000:
                self.app.player.inv.insert(self.outcom)
                self.working = False
        
    @property
    def progress(self):
        if self.working:
            now = self.timer.get_ticks()
            return(((now-self.time)/self.process_time)//10)      
        else:
            return(0)


class factory_list:
    def __init__(self, app):
        self.app = app
        self.active = []

        self.factory_img = [0 for i in app.terrain.data['factory_type']]
        for img in app.terrain.data['factory_type']:
            self.factory_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())
        # self.factory_img_rect = self.factory_img[0].get_rect()

    def add(self, bp, b_map, x, y):
        width = bp['dim']['w']
        hight = bp['dim']['h']
        for j in range(y, y+hight):
            for i in range(x, x+width):
            
                b_map[j,i] = -1

        new_factory = factory(self, self.app, bp, y,x)
        self.active.append(new_factory)
        

    def delete(self, b_map, factory):
        width, hight = factory.size
        x, y = factory.tile_pos
        for i in range(x, x+width):
            for j in range(y, y+hight):
                b_map[i, j] = 0
        self.active.remove(factory)

        
    def factory(self, tile_pos):
        for f in self.active:
            if pg.Rect(f.tile_pos,f.size).collidepoint(tile_pos):
                return(f)
        return()

    def draw(self, surface):
        for f in self.active:
            f.draw(surface)
            
    def update(self):
        for f in self.active:
            f.update()
        


