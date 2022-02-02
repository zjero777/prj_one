import pygame as pg
from options import *


class factory:
    def __init__(self, app):
        self.app = app
        self.active = []

        self.factory_img = [0 for i in app.field.data['factory_type']]
        for img in app.field.data['factory_type']:
            self.factory_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())
        self.factory_img_rect = self.factory_img[0].get_rect()

    def add(self, bp, b_map, x, y):
        width = bp['dim']['w']
        hight = bp['dim']['h']
        id = bp['id']
        self.active.append({'id': id, 'coord': (x, y), 'wh': (width, hight)})
        # b_map[x,y]=1
        for i in range(x, x+width):
            for j in range(y, y+hight):
                b_map[i, j] = -1

    def draw(self, surface: pg.Surface):
        for f in self.active:
            screen_pos = self.app.field.demapping(f['coord'])
            f_rect = pg.Rect(screen_pos, (f['wh'][0]*TILE, f['wh'][1]*TILE))
            if pg.Rect(VIEW_RECT).colliderect(f_rect):
                surface.blit(self.factory_img[int(
                    f['id'])], f_rect)
