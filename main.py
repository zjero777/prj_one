import pygame as pg
import pygame_gui
from inv import *
from mouse import mouse 
from options import *
from terrain import * 
from info import *
from player import *
from factory import *
from waterfall import *
from tech import *

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE, pg.SRCALPHA)
        self.surface = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.manager = pygame_gui.UIManager(WIN_SIZE, path.join(data_dir, 'theme.json'))
        self.clock = pg.time.Clock()
        self.timer = pg.time
        self.allsprites = pg.sprite.Group()
        self.data = self.load_resources()
        self.terrain = terrain(self, PLANET_WIDTH, PLANET_HIGHT)
        self.player = player(self)
        self.info = info(self)
        self.is_runing = True
        self.mouse = mouse(self)
        self.factories = factory_list(self)
        self.player.fall((PLANET_WIDTH//2,PLANET_HIGHT//2))
        self.water_falls = waterfalls(self)
        self.ui_tech_bp = UI_tech_blueprints(self)
        self.ui_tech = ui_tech(self)
                
    def update(self, dt):
        self.player.update()
        self.terrain.update() 
        self.allsprites.update(dt)
        self.factories.update()
        self.mouse.update()
        self.info.update()
        self.water_falls.update()
        self.ui_tech.update()
        self.ui_tech_bp.update()
        
    
    def draw(self):
        self.surface.fill(pg.Color('cyan'))        
        self.screen.blit(self.surface, (0,0))
        self.terrain.draw() 
        # self.player.draw()
        self.player.draw()
        self.manager.draw_ui(self.screen)
        self.mouse.draw()  
        self.allsprites.draw(self.screen)
        self.info.draw()
        
              
        
    def run(self):
        while self.is_runing:
            dt = self.clock.tick(FPS)/1000
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
         
            dt = self.clock.tick(60)/1000.0
            self.manager.update(dt)                   
            self.update(dt)
            self.draw()
            fps = self.clock.get_fps()
            self.info.debug((0,0), f'FPS:{int(fps)}')
            pg.display.update()
    
    def load_resources(self):
        f = open('data/res.json',)
        data = json.load(f)
        f.close
        return data

if __name__ == '__main__':
    app = game()
    app.run()
    