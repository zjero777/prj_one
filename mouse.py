from numpy import mat
import pygame as pg
from options import *
from animatedsprite import *

        

class mouse:
    def __init__(self, app):
        
        self.app = app
        pg.mouse.set_visible(False)
        self.pos = pg.mouse.get_pos()
        
        self.cursors = [0 for cursor in cursor_type]

        ss = spritesheet(path.join(img_dir, 'cur1.png'))
        ani_cur_dig = ss.load_strip(ss.sheet.get_rect(), 1)
        self.cursors[cursor_type.normal.value] = AnimatedSprite(self.pos, ani_cur_dig)
                
        ss = spritesheet(path.join(img_dir, 'anicurdigv3.png'))
        ani_cur_dig = ss.load_strip((0,0,32,32), 6)
        self.cursors[cursor_type.dig.value] = AnimatedSprite(self.pos, ani_cur_dig)
            
        ss = spritesheet(path.join(img_dir, 'cur_tech.png'))
        cur = ss.load_strip(ss.sheet.get_rect(), 1)
        self.cursors[cursor_type.tech.value] = AnimatedSprite(self.pos, cur)
      
        
        # self.cursor.append(pg.image.load(path.join(img_dir, "cur2.png")).convert_alpha())
        
        

        self.setcursor(cursor_type.normal)
        
        
        self.setcursor_noitem() #item on cursor

    def setcursor_with_item(self, item):
        self.item = int(item['id'])
    
    def setcursor_noitem(self):
        self.item = -1
        
            

    def update(self):
        self.pos = pg.mouse.get_pos()
        self.cursors[cursor_type.normal.value].SetRect(self.pos)
        self.cursors[cursor_type.dig.value].SetRect(self.pos)
        self.cursors[cursor_type.tech.value].SetRect(self.pos)
        
        
    def setcursor(self, idx):
        match idx:
            case cursor_type.normal: 
                self.app.allsprites = pg.sprite.Group(self.cursors[cursor_type.normal.value])
            case cursor_type.dig: 
                self.app.allsprites = pg.sprite.Group(self.cursors[cursor_type.dig.value])
            case cursor_type.tech:
                self.app.allsprites = pg.sprite.Group(self.cursors[cursor_type.tech.value])


            
        self.cursor = idx
        

    # def process_events(self, event):
    #     if event.type == pg.MOUSEMOTION:
    #         self.pos = event.pos
        
    
    def draw(self):
        if self.item > -1 and self.app.player.is_openinv:
            pic = pg.transform.scale(self.app.terrain.block_img[self.item], (32, 32))
            self.app.screen.blit(pic, pg.Rect(self.pos,self.pos).move(10,20))
        # i=self.cursor.value
        # self.app.screen.blit(self.cursors[i], self.pos)
    
    
            
    