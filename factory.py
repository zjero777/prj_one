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
        self.size = (blueprint['dim']['w'], blueprint['dim']['h'])
        if 'plan' in blueprint.keys():
            self.plan = np.transpose(blueprint['plan'])
        else:
            self.plan = None
        self.demolition = blueprint['demolition']
        self.pic = list.factory_img[blueprint['id']]
        if 'in' in blueprint.keys():
            self.incom = blueprint['in']
        else:
            self.incom = []
        if 'out' in blueprint.keys():
            self.outcom = (blueprint['out'])
        else:
            self.outcom = []
        self.process_time = int(blueprint['time']*1000)
        if 'operate' in blueprint.keys():
            self.operate = (blueprint['operate'])
        else:
            self.operate = 0
        if 'detect' in blueprint.keys():
            self.detect = (blueprint['detect'])
        else:
            self.detect = 0
        
        
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
            if item and item!=0:
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
            # to-do: resource translate begin
            
            if self.app.player.inv.exist(self.incom):
                self.app.player.inv.delete(self.incom)
                self.time = self.timer.get_ticks()
                self.working = True
        else:
            if self.timer.get_ticks()-self.time>self.process_time:
                # to-do: resource translate end
                
                self.app.player.inv.insert(self.outcom)
                self.working = False
        
    @property
    def progress(self):
        if self.working:
            now = self.timer.get_ticks()
            return(((now-self.time)/self.process_time))      
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
                b_map[i,j] = -1

        new_factory = factory(self, self.app, bp, x,y)
        self.active.append(new_factory)
        
        if 'detect' in bp.keys():
            discover_radius = bp['detect']
            self.app.terrain.set_discover(x+new_factory.size[0]//2,y+new_factory.size[1]//2, discover_radius)
        if 'operate' in bp.keys():
            operate_radius = bp['operate']
            self.app.terrain.set_operate(x+new_factory.size[0]//2,y+new_factory.size[1]//2, operate_radius)
            
        return(new_factory)
            
        

    def delete(self,b_map, factory):
        width, hight = factory.size
        x, y = factory.tile_pos
        for i in range(x, x+width):
            for j in range(y, y+hight):
                b_map[i, j] = 0
                
        if factory.operate>0:
            self.app.terrain.set_operate(x+factory.size[0]//2,y+factory.size[1]//2, factory.operate, False)
                
                
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
        # update
        for f in self.active:
            f.update()
            
        # control
            
    @property
    def rect_list_all(self):
        f_list = []
        for item in self.active:
            f_list.append(pg.Rect(item.tile_pos, item.size))
        return f_list
        


