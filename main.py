import pygame as pg
import pygame_gui
from inv import *
from mouse import mouse 
from options import *
from field import *
from info import *
from player import *

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE)
        self.surface = pg.Surface(WIN_SIZE)
        self.manager = pygame_gui.UIManager(WIN_SIZE)
        self.clock = pg.time.Clock()
        self.timer = pg.time
        self.field = field(self, PLANET_WIDTH, PLANET_HIGHT, [10,10])
        self.player = player(self)
        self.info = info(self)
        self.mouse = mouse(self)
        self.is_runing = True
        
                
    def update(self):
        self.field.update() 
        self.mouse.update()
        self.info.update()
    
    def draw(self):
        self.surface.fill(pg.Color('cyan'))
        self.screen.blit(self.surface, (0,0))
        self.field.draw() 
        self.player.draw()
        self.manager.draw_ui(self.screen)
        self.info.draw()
        self.mouse.draw()        
        
    def run(self):
        while self.is_runing:
            self.clock.tick(FPS)
            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    self.is_runing = False
                    
#                if event.type == pg.USEREVENT:
#                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
#                        if event.ui_element == self.hello_button:
#                            print('Hello World!')                
                # self.mouse.process_events(event)
                # self.field.process_events(event)
                self.manager.process_events(event)
         
            self.update()
            self.draw()
            dt = self.clock.tick(60)/1000.0
            self.manager.update(dt)                   
            
            pg.display.update()
    
if __name__ == '__main__':
    app = game()
    app.run()
    