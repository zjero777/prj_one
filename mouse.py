import pygame as pg
from options import *

class mouse:
    def __init__(self, app):
        self.app = app
        pg.mouse.set_visible(False)
        self.cursors = []
        self.cursors.append(pg.image.load(path.join(img_dir, "cur1.png")).convert_alpha())
        self.cursors.append(pg.image.load(path.join(img_dir, "cur2.png")).convert_alpha())
        self.cursor = 0
        
        self.item = -1

    def setcursor_with_item(self, item):
        self.item = int(item['item'])
    
    def setcursor_noitem(self):
        self.item = -1
        
            

    def update(self):
        self.pos = pg.mouse.get_pos()
        
    def setcursor(self, idx):
        self.cursor = idx
        

    # def process_events(self, event):
    #     if event.type == pg.MOUSEMOTION:
    #         self.pos = event.pos
        
    
    def draw(self):
        if  self.item > -1:
            self.app.screen.blit(self.app.field.field_img[self.item], pg.Rect(self.pos,self.pos).move(10,20), area=(0,0,32,32))
        self.app.screen.blit(self.cursors[self.cursor], self.pos)
    
    