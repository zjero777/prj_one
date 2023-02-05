from numpy import mat
import pygame as pg
from options import *
from animatedsprite import *
from distutils.util import strtobool
        

class mouse:
    def __init__(self, app):
        self.app = app

        self.status = {'type':None, 'button': None, 'area': None}
        self.first_pressed = [False, False, False]
        
        self.init_animate_cursors()


    def init_animate_cursors(self):
        pg.mouse.set_visible(False)
        self.cursors = [0 for cursor in cursor_type]

        ss = spritesheet(path.join(img_dir, 'cur1.png'))
        ani_cur_dig = ss.load_strip(ss.sheet.get_rect(), 1)
        self.cursors[cursor_type.normal.value] = AnimatedSprite(pg.mouse.get_pos(), ani_cur_dig)
                
        ss = spritesheet(path.join(img_dir, 'anicurdigv3.png'))
        ani_cur_dig = ss.load_strip((0,0,32,32), 6)
        self.cursors[cursor_type.dig.value] = AnimatedSprite(pg.mouse.get_pos(), ani_cur_dig)
            
        ss = spritesheet(path.join(img_dir, 'cur_tech.png'))
        cur = ss.load_strip(ss.sheet.get_rect(), 1)
        self.cursors[cursor_type.tech.value] = AnimatedSprite(pg.mouse.get_pos(), cur)

        self.setcursor(cursor_type.normal)
        self.setcursor_noitem() #item on cursor

    def setcursor_with_item(self, item):
        self.item = int(item['id'])
    
    def setcursor_noitem(self):
        self.item = None
            

    def update(self):
        self.pos = pg.mouse.get_pos()
        self.cursors[cursor_type.normal.value].SetRect(self.pos)
        self.cursors[cursor_type.dig.value].SetRect(self.pos)
        self.cursors[cursor_type.tech.value].SetRect(self.pos)

        keystate = pg.key.get_pressed()
        
        
        
        self.button = pg.mouse.get_pressed()
        self.pos = pg.mouse.get_pos()
        self.tile_pos = self.app.terrain.mapping(self.pos)
        
        self.status['button'] = None
        
        # RIGHT BUTTON
        if not self.button[0]:
            if self.button[2] and not self.first_pressed[2]:
                # Rigth mouse button
                # first push button
                self.first_pressed[2] = True
                self.status = {'type':MOUSE_TYPE_BUTTON_DOWN, 'button': 2, 'area': pg.Rect(self.tile_pos, (1,1))}
                
            elif self.first_pressed[2] and not self.button[2]:
                # release button
                self.first_pressed[2] = False
                if self.status['area'].size==(1,1):
                    # click
                    click_area_screen = pg.Rect((0,0),self.pos)
                    if click_area_screen.colliderect(VIEW_RECT):
                        self.status['type'] = MOUSE_TYPE_CLICK
                        self.status['button'] = 2
                        self.app.mouse.setcursor(cursor_type.normal)
                else:
                    # drop
                    self.status['type'] = MOUSE_TYPE_DROP
                    self.status['button'] = 2
                    # self.status['area'] = None
            elif self.button[2]:
                # on drag
                pass

            
            
        # LEFT BUTTON
        if not self.button[2]:
            if self.button[0] and not self.first_pressed[0]:
                # first push button - drag
                self.first_pressed[0] = True
                self.status = {'type':MOUSE_TYPE_BUTTON_DOWN, 'button': 0, 'area': pg.Rect(self.tile_pos, (1,1))}
                self.start = self.status['area'].topleft
            elif self.first_pressed[0] and not self.button[0]:
                # release button
                self.first_pressed[0] = False
                if self.status['area'].size==(1,1):
                    # click
                    self.status = {'type':MOUSE_TYPE_CLICK, 'button': 0, 'area': pg.Rect(self.tile_pos, (1,1))}
                else:
                    # drop
                    self.status['type'] = MOUSE_TYPE_DROP
                    self.status['button'] = 0
            elif self.button[0]:
                # on drag - process
                self.status['type'] = MOUSE_TYPE_DRAG
                self.status['area'] = pg.Rect((min(self.tile_pos[0], self.start[0]),min(self.tile_pos[1], self.start[1])), (abs(self.start[0]-self.tile_pos[0])+1, abs(self.start[1]-self.tile_pos[1])+1))
                self.status['button'] = 0
        
        

        # if self.app.ui_tech_bp.visible: 
        #     self.app.info.clear_info()
        #     return

        # if self.app.ui_tech.enabled:
        #     # self.app.info.clear_info()
        #     return

        # if not pg.Rect(VIEW_RECT).collidepoint(self.pos):
        #     self.app.info.clear_info()


        # if pg.Rect(VIEW_RECT).collidepoint(self.pos) and not self.app.player.inv.is_open and keystate[pg.K_f]:


        #     if not mouse_button[0]:
        #         self.first_click = True
        #     if not self.tile_pos:
        #         area = pg.Rect(-1,-1,1,1)
        #     else:
        #         area = pg.Rect(self.tile_pos, (1,1))

        #     click_area_screen = pg.Rect((0,0),self.pos)
        #     if click_area_screen.colliderect(VIEW_RECT):
        #         area_num = area.collidelist(self.app.ui_tech.tech_sites.rect_list_all)
        #         site = self.app.ui_tech.site(area_num)
        #         if site:
        #             site_progress = (site.status==TECH_A_PROGRESS)
        #         else:
        #             site_progress = False
        #     else:
        #         site_progress = False

        #     if mouse_button[0] and len(self.tile_pos) > 0 and not self.app.terrain.dark_cover[self.tile_pos] and self.app.terrain.operate[self.tile_pos] and not site_progress:
        #         if not self.app.player.inv.selected_cell is None:

        #             if self.first_click:
        #                 self.first_click = False

        #                 # build
        #                 if self.app.terrain.building_map[self.tile_pos[0], self.tile_pos[1]] == 0:
        #                     self.app.player.build(self.app.terrain)
        #                     if self.app.terrain.building_map[self.tile_pos] == self.app.terrain.GetBData('name', 'not_growed_corall')['id']:
        #                             self.app.corall_growings.add(self.tile_pos)
        #                     self.app.terrain.complete_factory()

        #         else:

        #             if self.first_click:
        #                 select_building = self.app.terrain.building_map[self.tile_pos[0],
        #                                                     self.tile_pos[1]]
        #                 select_terrain = self.app.terrain.field[self.tile_pos[0],
        #                                             self.tile_pos[1]]
        #                 select_factory = self.app.factories.factory(
        #                     self.tile_pos)
        #                 # dig
        #                 if select_building == 0 and strtobool(self.app.terrain.GetTileInfo('allow_dig', self.tile_pos)):
        #                     data = self.app.terrain.GetTData('id', select_terrain)
        #                     time = data['dig']['time']
        #                     if self.app.player.manual_dig(self.app.terrain, self.tile_pos, time):
        #                         self.first_click = True
        #                         if self.app.terrain.field[self.tile_pos] == self.app.terrain.GetTData('name', 'pit')['id']:
        #                             self.app.moss_spawns.add(self.tile_pos)
        #                             if self.app.terrain.water_arround(self.tile_pos):
        #                                self.app.water_falls.add(self.tile_pos)
        #                 # demolition
        #                 elif select_building > 0:
        #                     data = self.app.terrain.GetBData('id', select_building)
        #                     time = data['demolition']
        #                     if self.app.player.manual_demolition(self.app.terrain, self.tile_pos, time):
        #                         self.first_click = False
        #                 elif select_factory:
        #                     time = select_factory.demolition
        #                     if self.app.player.manual_demolition(self.app.terrain, self.tile_pos, time):
        #                         self.first_click = False

        #                 else:
        #                     self.app.player.stop_dig()
        #                     self.app.player.stop_demolition()

        #                 # building select
        #             else:
        #                 self.app.player.stop_dig()
        #                 self.app.player.stop_demolition()
        #     else:
        #         self.app.player.stop_dig()
        #         self.app.player.stop_demolition()

        #     if mouse_button[2] and not mouse_button[0] and len(self.tile_pos) > 0:
        #         self.app.player.inv.selected_cell = None
        #         # self.app.player.inv.item = {}
        # else:
        #      self.app.player.stop_dig()
        #      self.app.player.stop_demolition()

        
        
        
    def setcursor(self, idx):
        self.app.allsprites = pg.sprite.Group(self.cursors[idx.value])
        self.cursor = idx
        

    # def process_events(self, event):
    #     if event.type == pg.MOUSEMOTION:
    #         self.pos = event.pos
        
    
    def draw(self):
        if self.item and self.app.player.inv.is_open:
            pic = pg.transform.scale(self.app.terrain.block_img[self.item], (32, 32))
            self.app.screen.blit(pic, pg.Rect(self.pos,self.pos).move(10,20))
        # i=self.cursor.value
        # self.app.screen.blit(self.cursors[i], self.pos)
    
    
            
    