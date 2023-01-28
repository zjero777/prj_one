import json
from options import *
import pygame as pg

class data:
    def __init__(self) -> None:
        f = open('data/data.json', encoding='utf-8')
        self.data = json.load(f)
        f.close

        self.factory_img = [None for i in self.data['factory_type']]


    def init_sprites(self):
        for img in self.data['factory_type']:
            self.factory_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())

        
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
    
