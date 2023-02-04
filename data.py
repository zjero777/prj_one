import json
from options import *
import pygame as pg
from sequence import *

class data:
    def __init__(self) -> None:
        f = open('data/data.json', encoding='utf-8')
        self.data = json.load(f)
        f.close

        self.factory_img = [None for i in self.data['factory_type']]
        self.recipe_img = [None for i in self.data['recipes']]
        self.toolbar_img = [None for i in self.data['toolbar']]
        
        self.seq_chg_recipe = sequence(self, 'data/chg_recipe.json')
        self.seq_prod = sequence(self, 'data/prod.json')
        # self.seq_remove = sequence(self)
        

    def get_recipe_by_id(self, id):    
        result = -1
        for i in self.data['recipes']:
            if i['id']==id: 
                return i
        return result

    def init_sprites(self):
        for img in self.data['factory_type']:
            self.factory_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())

        for img in self.data['recipes']:
            self.recipe_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())

        for img in self.data['toolbar']:
            self.toolbar_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['icon'])).convert_alpha())

        
    def get_bdata(self, key, stroke):
        for item in self.data.get('block_type'):
            if item[key] == stroke:
                return(item)

    def get_tdata(self, key, stroke):
        for item in self.data.get('terrain_type'):
            if item[key] == stroke:
                return(item)

    def get_fdata(self, key, stroke):
        for item in self.data.get('factory_type'):
            if item[key] == stroke:
                return(item)
    
