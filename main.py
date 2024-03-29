import pygame as pg
import pygame_gui

from data import *
from factory import *
from info import *
from inv import *
from inv_place_block import inv_place_block
from inv_recipe import *
from inv_toolbar import inv_toolbar
from mouse import mouse
from options import *
from player import *
from sequence import *
from tech import *
from terrain import *
from waterfall import *


class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE, pg.SRCALPHA)
        # self.surface = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.manager = pygame_gui.UIManager(WIN_SIZE, path.join(data_dir, 'theme.json'))
        self.clock = pg.time.Clock()
        self.timer = pg.time
        self.allsprites = pg.sprite.Group()
        self.img_res = self.load_resources()
        self.data = data()
        self.data.init_sprites() #init sprites from data (factories, items and etc)
        self.terrain = terrain(self, PLANET_WIDTH, PLANET_HIGHT)
        self.player = player(self)
        self.inv_recipe = inv_recipe(self)        
        self.inv_toolbar = inv_toolbar(self)
        self.info = info(self)
        self.is_runing = True
        self.mouse = mouse(self)
        self.factories = factory_list(self)
        self.player.fall((10,10))
        self.water_falls = waterfalls(self)
        self.moss_spawns = moss_spawns(self)
        self.corall_growings = corall_growings(self)
        self.ui_tech_bp = UI_tech_blueprints(self)
        self.ui_tech = ui_tech(self)
        self.inv_place_block = inv_place_block(self)
        self.clear_modal()
                
    def update(self, dt):
        self.mouse.update()
        self.player.update()
        self.terrain.update() 
        self.allsprites.update(dt)
        self.factories.update()
        self.info.update()
        self.water_falls.update()
        self.moss_spawns.update()
        self.corall_growings.update()
        self.ui_tech.update()
        self.inv_recipe.update()
        self.inv_toolbar.update()
        self.inv_place_block.update()
        self.ui_tech_bp.update()
        
    
    def draw(self):
        # self.screen.fill(pg.Color('cyan'))        
        # self.screen.blit(self.surface, (0,0))
        self.terrain.draw() 
        # self.player.draw()
        self.inv_recipe.draw()
        self.inv_toolbar.draw()
        self.inv_place_block.draw()
        self.manager.draw_ui(self.screen)
        self.mouse.draw()  
        self.allsprites.draw(self.screen)
        self.info.draw()
        
              
        
    def run(self):
        while self.is_runing:
            dt = self.clock.tick(FPS)/1000
            fps = self.clock.get_fps()
            self.info.debug((0,0), f'FPS:{int(fps)}')
            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    self.is_runing = False

                self.ui_tech.process_events(event)
                self.manager.process_events(event)
         
            self.manager.update(dt)                   
            self.update(dt)
            self.draw()

            pg.display.update()
    
    def load_resources(self):
        f = open('data/res.json')
        img_res = json.load(f)
        f.close
        return img_res
    
    def set_modal(self, cls): 
        self.modal_class = cls
        
    def is_modal(self, cls):
        if self.modal_class!=None:
            return self.modal_class==cls
        else:
            return True
        
    def clear_modal(self):
        self.modal_class = None

if __name__ == '__main__':
    app = game()
    app.run()
    