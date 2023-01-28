import pygame as pg
from options import *
from storage  import *
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
        self.status = None  #None, Prod, Chg_Recipe, Remove
        self.command = None  # 
        self.storage = None
        self.in_storage = None
        self.out_storage = None
        
        if 'plan' in blueprint.keys():
            self.plan = np.transpose(blueprint['plan'])
        else:
            self.plan = None
        self.demolition = blueprint['demolition']
        self.pic = list.factory_img[blueprint['id']]

        self.recipe = None
        self.command_step = None
        if 'use_recipes' in blueprint.keys():
            self.recipe = self.get_recipe_by_id(blueprint['use_recipes']['selected_id'])
            self.command_step = 0
            self.status = FSTAT_CHG_RECIPE

        if 'storage' in blueprint.keys():
            self.storage = storage(app, self, blueprint['storage'])  #add universal storage cell
        
        if 'operate' in blueprint.keys():
            self.operate = (blueprint['operate'])
            self.app.terrain.set_operate(x+self.size[0]//2,y+self.size[1]//2, self.operate)
        else:
            self.operate = 0
        if 'detect' in blueprint.keys():
            self.detect = (blueprint['detect'])
            self.app.terrain.set_discover(x+self.size[0]//2,y+self.size[1]//2, self.detect)
        else:
            self.detect = 0

        self.working = False
        self.timer = app.timer
        self.time = 0

    def remove(self, b_map):
        self.working = False
        width, hight = self.size
        x, y = self.tile_pos
               
        for i in range(x, x+width):
            for j in range(y, y+hight):
                b_map[i, j] = self.plan[i-x, j-y]

        if self.operate>0:
            self.app.terrain.set_operate(x+self.size[0]//2,y+self.size[1]//2, self.operate, -1)
        

    def change_recipe(self, recipe):
        self.status = CHG_RCPT_INIT
        self.new_recipe = recipe
        if self.recipe is None: 
            self.status = CHG_RCPT_DONE
            self.recipe = self.new_recipe
            self.new_recipe = None
            self.change_prod_storage(self.recipe) # create in and out storage cell
            return
        else:
            self.status = CHG_RCPT_PURGE_IN
            return
    
    def change_prod_storage(self, recipe):
        
        pass
        
    def get_recipe_by_id(self, id):    
        result = -1
        self.app.terrain.data['recipes']
        for i in self.app.terrain.data['recipes']:
            if i['id']==id: 
                return i
        return result
        
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
            if self.app.factories.selected==self:
                surface.blit(self.pic, f_rect)
                pg.draw.rect(surface, pg.Color('gray'), f_rect, 1)
            else:
                surface.blit(self.pic, f_rect)
            
    def update(self):
        if self.status is None: return
        if self.status == FSTAT_NONE: return
        if self.status == FSTAT_CHG_RECIPE: 
            if self.command_step is None: return
            if self.recipe is None: return
            command = self.app.seq_chg_recipe.get_command(self.command_step)
            match command['name']:
                case 'inspect_in':
                    result_command = self.in_storage.is_need_purge_by_recipe(self.incom_recipe)
                case 'change_in':
                    result_command = self.create_storage_in(self.incom_recipe)
                case 'inspect_out':
                    result_command = self.storage_is_correct(self.out_storage, self.outcom_recipe)
                case 'change_out':
                    result_command = self.create_storage_out(self.out_storage, self.outcom_recipe)
                case 'purge_in':
                    result_command = self.purge_storage_in(self.in_storage, self.incom_recipe)
                case 'purge_out':
                    result_command = self.purge_storage_out(self.out_storage, self.outcom_recipe)
                case 'allow_recipe':
                    self.status = FSTAT_PROD
            
            self.msg = self.app.seq_chg_recipe.get_msg(self.command_step, result_command)
            self.command_step = self.app.seq_chg_recipe.go_next(self.command_step, result_command)
        
        if not self.working:
            # to-do: resource translate begin
            if 'in' in self.recipe.keys(): 
                in_res=self.recipe['in']
            else: 
                in_res=None

            if self.app.player.inv.exist(in_res):
                self.app.player.inv.delete(in_res)
                self.time = self.timer.get_ticks()
                self.working = True
        else:
            if self.timer.get_ticks()-self.time>self.recipe['time']*1000:
                # to-do: resource translate end
                
                self.app.player.inv.insert(self.recipe['out'])
                self.working = False
        
    def create_storage_in(self, recipe):
        if self.in_storage is None:
            self.in_storage = storage(self.app, self)
        else:
            self.in_storage.remove_non_recipe_cells(recipe)
        self.in_storage.append_recipe_cells(recipe)
        self.in_storage.sort_by_recipe(recipe)
        return(True)
        
    @property
    def progress(self):
        if self.working:
            now = self.timer.get_ticks()
            return((now-self.time)/(self.recipe['time']*1000))      
        else:
            return(0)

    @property
    def incom_recipe(self):
        if not self.recipe is None:
            if 'in' in self.recipe.keys():
                return(self.recipe['in'])      
        return(None)

    @property
    def outcom_recipe(self):
        if not self.recipe is None:
            if 'out' in self.recipe.keys():
                return(self.recipe['out'])      
        return(None)

    @property
    def process_time(self):
        if not self.recipe is None:
            if 'time' in self.recipe.keys():
                return(self.recipe['time']*1000)      
        return(0)

class factory_list:
    def __init__(self, app):
        self.app = app
        self.list = []
        self.active = None

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
        self.list.append(new_factory)
      
            
        return(new_factory)
            
        

    def delete(self,b_map, factory):
        self.list.remove(factory)
        factory.remove(b_map)

        
    def factory(self, tile_pos):
        for f in self.list:
            if pg.Rect(f.tile_pos,f.size).collidepoint(tile_pos):
                return(f)
        return()

    def draw(self, surface):
        for f in self.list:
            f.draw(surface)
            
    def update(self):
        # update
        for f in self.list:
            f.update()
            
        # control
            
    @property
    def rect_list_all(self):
        f_list = []
        for item in self.list:
            f_list.append(pg.Rect(item.tile_pos, item.size))
        return f_list
        
    @property
    def selected(self):
        return self.active
    
    def select(self, num):
        if num!=-1: 
            self.active = self.list[num]

    def unselect(self):
        self.active = None

    def get_by_num(self, num):
        if num>-1 and num<len(self.list):
            return self.list[num]
        else:
            return None
