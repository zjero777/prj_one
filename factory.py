import pygame as pg
from options import *
from storage  import *
import random as rnd
import numpy as np
from data import *


class factory:
    def __init__(self, app, data, blueprint,  x, y):
        self.app = app
        self.data = data
        self.id = blueprint['id']
        self.name = blueprint['name']
        self.tile_pos = (x, y)
        self.size = (blueprint['dim']['w'], blueprint['dim']['h'])
        self.status = None  #None, Prod, Chg_Recipe, Remove
        self.command = None  # 
        self.storage = None
        self.in_storage = None
        self.out_storage = None
        self._allow_recipe_list = []
        
        if 'plan' in blueprint.keys():
            self.plan = np.transpose(blueprint['plan'])
        else:
            self.plan = None
        self.demolition = blueprint['demolition']
        self.pic_id = blueprint['id']

        self.recipe = None
        self.command_step = None
        if 'use_recipes' in blueprint.keys():
            self.recipe = self.data.get_recipe_by_id(blueprint['use_recipes']['selected_id'])
            self._allow_recipe_list = blueprint['use_recipes']['allowed_id']
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
        self.pause = False
        self.timer = pg.time
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
        
    def get_resources(self, minproc=100, maxproc=100):
        if minproc==maxproc: 
            proc=maxproc
        else:
            proc = rnd.randrange(minproc, maxproc)
        res, count = np.unique(self.plan, return_counts=True)
        all_res = (res, np.int64(count*(proc/100)))
        return(all_res)
    
    @property
    def allow_recipe_list(self):
        if '_allow_recipe_list' in vars(self):
            return(self._allow_recipe_list)
        else:
            return([])
    
    @allow_recipe_list.setter
    def allow_recipe_list(self, value):
        self._allow_recipe_list = value
    
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
                surface.blit(self.data.factory_img[self.pic_id], f_rect)
                pg.draw.rect(surface, pg.Color('gray'), f_rect, 1)
            else:
                surface.blit(self.data.factory_img[self.pic_id], f_rect)
            
    def update(self):
        if self.status is None: return
        if self.status == FSTAT_NONE: return
        if self.status == FSTAT_CHG_RECIPE: 
            if self.command_step is None: return
            if self.recipe is None: return
            # command = self.data.seq_chg_recipe.get_command(self.command_step)
            if self.command_step == CHG_INSPECT_IN:
                    result_command = self.inspect_storage(self.in_storage, self.incom_recipe)
            elif self.command_step == CHG_CHANGE_IN:
                    result_command = self.create_storage_in(self.incom_recipe)
            elif self.command_step == CHG_INSPECT_OUT:
                    result_command = self.inspect_storage(self.out_storage, self.outcom_recipe)
            elif self.command_step == CHG_CHANGE_OUT:
                    result_command = self.create_storage_out(self.outcom_recipe)
            elif self.command_step == CHG_PURGE_IN:
                    result_command = self.inspect_storage(self.in_storage, self.incom_recipe)
            elif self.command_step == CHG_PURGE_OUT:
                    result_command = self.inspect_storage(self.out_storage, self.outcom_recipe)
            elif self.command_step == CHG_ALLOW_RECIPE:
                    result_command = True
                    self.command_step = 0
                    self.status = FSTAT_PROD
            self.msg = self.data.seq_chg_recipe.get_msg(self.command_step, result_command)
            self.command_step = self.data.seq_chg_recipe.go_next(self.command_step, result_command)
        if self.status == FSTAT_PROD: 
            if self.command_step is None: return
            if self.recipe is None: return
            if self.pause: return
            command = self.data.seq_prod.get_command(self.command_step)
            if self.command_step == PROD_INSPECT_IN:
                if self.incom_recipe:
                    result_command = self.in_storage.inspect_resources(self.incom_recipe)  # if res is exist
                else:
                    result_command = True
            elif self.command_step == PROD_BEGIN_PROD:
                result_command = self.begin_prod()  # if del res, set timer
            elif self.command_step == PROD_WAIT_FOR_COMPLETE:
                result_command = self.prod_in_progress()  # if complete
            elif self.command_step == PROD_INSPECT_OUT:
                result_command = self.inspect_free_place_and_store(self.out_storage, self.outcom_recipe) # if store result res
            self.msg = self.data.seq_prod.get_msg(self.command_step, result_command)
            self.command_step = self.data.seq_prod.go_next(self.command_step, result_command)
            
    def inspect_free_place_and_store(self, storage: storage, recipe):
        if storage.add_resources_by_recipe(recipe): 
            
            return(True)
        return(False)

    def prod_in_progress(self):
        if self.pause:
            self.time =+ self.timer.get_ticks()-self.time
        
        dt = self.timer.get_ticks()-self.time    
            
        if dt>self.recipe['time']*1000:
            self.working = False
            return(True)
        return(False)

    def begin_prod(self):
        if not self.in_storage is None:
            if not self.in_storage.inspect_resources(self.incom_recipe): return(False)
            self.in_storage.remove_resources(self.incom_recipe)
        self.time = self.timer.get_ticks()
        self.working = True
        return(True)
        
    def inspect_storage(self, storage, recipe):
        if storage is None: return(True)
        return(storage.is_need_purge_by_recipe(recipe))
        
    def create_storage_in(self, recipe):
        if recipe is None:
            self.in_storage = None
            return(True)

        if self.in_storage is None:
            self.in_storage = storage(self.app, self)
        else:
            self.in_storage.remove_non_recipe_cells(recipe)
        self.in_storage.append_recipe_cells(recipe)
        self.in_storage.sort_by_recipe(recipe)
        return(True)

    def create_storage_out(self, recipe):
        if self.out_storage is None:
            self.out_storage = storage(self.app, self)
        else:
            self.out_storage.remove_non_recipe_cells(recipe)
        self.out_storage.append_recipe_cells(recipe)
        self.out_storage.sort_by_recipe(recipe)
        return(True)

    @property
    def message(self) :
        if not ('msg' in vars(self)): return()
        return(self.msg)
        
    
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
        return(None)

class factory_list:
    def __init__(self, app):
        self.app = app
        self.list = []
        self.active = None

        # self.factory_img = [0 for i in data['factory_type']]
        # for img in data['factory_type']:
        #     self.factory_img[img['id']] = (pg.image.load(
        #         path.join(img_dir, img['pic'])).convert_alpha())
        # self.factory_img_rect = self.factory_img[0].get_rect()

    def add(self, bp, b_map, x, y):
        width = bp['dim']['w']
        hight = bp['dim']['h']

        for j in range(y, y+hight):
            for i in range(x, x+width):
                b_map[i,j] = -1

        new_factory = factory(self.app, self.app.data, bp, x,y)
        self.list.append(new_factory)
      
            
        return(new_factory)
            
        

    def delete(self,b_map, factory):
        self.list.remove(factory)
        factory.remove(b_map)

        
    def factory(self, tile_pos):
        if not tile_pos: return
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
            
        if self.app.inv_recipe.is_open: return
        # control
        
        mouse_status_type = self.app.mouse.status['type']
        mouse_status_button = self.app.mouse.status['button']
        mouse_status_area = self.app.mouse.status['area']

        if mouse_status_type==MOUSE_TYPE_CLICK and mouse_status_button==MOUSE_LBUTTON: 
            click_area_screen = pg.Rect((0,0),mouse_status_area.topleft)
            if click_area_screen.colliderect(VIEW_RECT):
                factory_num = mouse_status_area.collidelist(self.rect_list_all)
                if factory_num!=-1: 
                    self.app.ui_tech.tech_sites.unselect()
                    self.app.factories.select(factory_num)
                    self.app.inv_toolbar.select_building = self.selected
            

        if mouse_status_type==MOUSE_TYPE_CLICK and mouse_status_button==MOUSE_RBUTTON: 
            if not self.app.factories.unselect(): #if no one select tech
                if not self.app.inv_toolbar.select_building is None:
                    self.app.inv_toolbar.unselect()
            self.app.mouse.setcursor(cursor_type.normal)
            
        if mouse_status_type==MOUSE_TYPE_DRAG and mouse_status_button==MOUSE_LBUTTON: 
            pass
        
        
            
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
        if self.active is None: return(False)
        self.active = None
        return(True)
    
    def get_by_num(self, num):
        if num>-1 and num<len(self.list):
            return self.list[num]
        else:
            return None
