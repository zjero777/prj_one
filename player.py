from hmac import digest
import pygame as pg
import pygame_gui as gui
from options import *
from inv import *

class player:
    def __init__(self, app):
        self.app = app
        self.inv = inv(self.app, self)
        self.dig = False
        self.timer = app.timer
        self.start_dig = 0
        self.is_openinv = False
        
    def update(self):
        self.inv.update()
    
    def draw(self):
        if self.is_openinv:
            self.inv.draw()
        # self.surface.fill(pg.Color(255,0,0))
        # self.app.screen.blit(self.surface, INV_RECT)
    
       
    
    def manual_dig(self, field, tilepos):
        if not self.dig:
            self.tile_pos = tilepos
            self.dig = True
            self.hp = 100
            self.app.mouse.setcursor(1)
            self.start_dig = self.timer.get_ticks()
        else:
            dt = self.timer.get_ticks()-self.start_dig
            if dt>10:
                if tilepos==self.tile_pos:
                    self.start_dig = self.timer.get_ticks()
                    self.hp -= 20
                    if self.hp<0:
                        field.dig_succes(self, tilepos)
                else:
                    self.dig = False
            self.app.info.debug((0,0), f'{self.hp} - {self.start_dig}:{dt} - dig: {self.dig}')
    
    def stop_dig(self):
        if self.dig:
            self.app.mouse.setcursor(0)
            self.dig = False
            self.hp = 100
            self.app.info.debug((0,30), f'{self.hp} - dig: {self.dig}')
            
    def pickup(self, loot):
        self.inv.add(loot)
     
    def use_selected(self):
        self.inv.delete()
        
