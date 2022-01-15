import pygame as pg
import pygame_gui
from inv import * 
from options import *
from field import *
from info import *

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE)
        self.surface = pg.Surface(WIN_SIZE)
        self.manager = pygame_gui.UIManager(WIN_SIZE)
        self.clock = pg.time.Clock()
        self.field = field(self, PLANET_WIDTH, PLANET_HIGHT)
        self.info = info(self)
        self.inv = inv(self)
        self.is_runing = True
                
    def update(self):
        self.field.update() 
        self.info.update()
        self.inv.update()
    
    def draw(self):
        self.surface.fill(pg.Color('cyan'))
        self.screen.blit(self.surface, (0,0))
        self.field.draw() 
        self.info.draw()
        self.inv.draw()
        self.manager.draw_ui(self.screen)
        
        
    def run(self):
        while self.is_runing:
            self.clock.tick(FPS)
            dt = self.clock.tick(60)/1000.0
            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    self.is_runing = False
                    
#                if event.type == pg.USEREVENT:
#                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
#                        if event.ui_element == self.hello_button:
#                            print('Hello World!')                
                self.field.process_events(event)
                self.manager.process_events(event)
         
            self.update()
            self.draw()
            self.manager.update(dt)                   
            
            pg.display.update()
    
if __name__ == '__main__':
    app = game()
    app.run()
    