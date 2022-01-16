import pygame as pg
from options import *

class mouse:
    def __init__(self, app):
        self.app = app
        pg.mouse.set_visible(False)
        self.cursors = []
        self.cursors.append(pg.image.load(path.join(img_dir, "cur1.png")).convert_alpha())
        self.cursors.append(pg.image.load(path.join(img_dir, "cur2.png")).convert_alpha())
        self.cursor = 0;

    def update(self):
        self.pos = pg.mouse.get_pos()
        
    def setcursor(self, idx):
        self.cursor = idx
        

    # def process_events(self, event):
    #     if event.type == pg.MOUSEMOTION:
    #         self.pos = event.pos
        
    
    def draw(self):
        self.app.screen.blit(self.cursors[self.cursor], self.pos)
    
    