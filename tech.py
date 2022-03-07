from random import randint
import numpy as np
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *

class UI_tech_blueprints:
    def __init__(self, app):
        self.app = app
        self.visible = False
        self.keypressed = False
        self.wnd = None
        self.create_wnd()

    def create_wnd(self, visible=False):
        self.wnd = gui.elements.UIWindow(pg.Rect(TECH_WND_RECT), 
                                         self.app.manager,
                                         'Чертежи технологий:',
                                         visible=visible,
                                         )
        
    def hide(self):
        self.wnd.hide()
        self.visible = False
        
    def update(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_b]:
            if not self.keypressed:
                self.keypressed = True
                if not self.wnd.visible:
                    self.wnd.show()
                    self.app.player.is_openinv = False
                else:
                    self.wnd.hide()
                self.visible = bool(self.wnd.visible)
        else:
            self.keypressed = False



        
            
        
    def draw(self):
        pass
    
class ui_tech:
    def __init__(self, app):
        self.app = app
        self.data = app.terrain.data['factory_type']
        self.enabled = False
        self.first_pressed = False
        self.area = pg.Rect(0,0,0,0)
        self.start = self.area
        self.allow = True
        # self.selected_site = None
        # close bp all factory 
        for item in self.data:
            item['open'] = False

        self.tech_sites = tech_sites(self.app)
        self.bg_blue = pg.Surface((TILE,TILE), pg.SRCALPHA)
        pg.draw.rect(self.bg_blue, pg.Color(64,128,255,128), (0,0,TILE, TILE))
        self.bg_red = pg.Surface((TILE,TILE), pg.SRCALPHA)
        pg.draw.rect(self.bg_red, pg.Color(255,32,128,128), (0,0,TILE, TILE))
        
    @property
    def selected_site(self):
        return self.tech_sites.selected_site
        
    def view_tech_site_ui(self):
        self.app.info.start()
        self.app.info.append_text(f'Лаборатория: {self.selected_site.name}')
        self.app.info.append_text(f' - размер: {self.selected_site.rect.size}')
        self.app.info.stop()
    
    
    def update(self):
        self.tech_sites.update()
        keystate = pg.key.get_pressed()
        if keystate[pg.K_t]:
            if not self.keypressed:
                self.keypressed = True
                if  (self.app.ui_tech_bp.visible or
                    self.app.player.is_openinv):
                    return
                
                if not self.enabled:
                    self.enabled = True
                    self.app.mouse.setcursor(cursor_type.tech)
                    self.app.player.inv.selected_backpack_cell = -1
                else:
                    self.enabled = False
                    self.app.mouse.setcursor(cursor_type.normal)
        else:
            self.keypressed = False
        
        
        
        if not self.enabled: 
            return()
            
        mouse_button = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        mouse_tile_pos = self.app.terrain.mapping(mouse_pos)
        if not mouse_tile_pos: return

        if self.selected_site:
            self.view_tech_site_ui()
        else:
            self.app.info.clear_info()

            

        
        if mouse_button[0] and not self.first_pressed:
            # first push button
            self.first_pressed = True
            self.area.topleft = mouse_tile_pos
            self.area.size = (1,1)
            self.start = self.area.copy()
        elif self.first_pressed and not mouse_button[0]:
            # release button
            self.first_pressed = False
            if self.area.size==(1,1):
                # click to cell
                click_area_screen = pg.Rect((0,0),mouse_pos)
                if click_area_screen.colliderect(VIEW_RECT):
                    area_num = self.area.collidelist(self.tech_sites.rect_list_all)
                    self.tech_sites.select(area_num)
                    # self.selected_site = self.tech_sites.get_by_num(area_num)
            else:
                # add area
                if self.allow:
                    content = self.app.terrain.building_map[self.area.left:self.area.right,
                                                self.area.top:self.area.bottom]
                    # self.selected_site = self.tech_sites.add(self.area, content)
                    self.tech_sites.add(self.area, content)
                self.area = pg.Rect(0,0,0,0)
        elif mouse_button[0]:
            # on drag
            self.area.left = min(mouse_tile_pos[0], self.start.left)
            self.area.top = min(mouse_tile_pos[1], self.start.top)
            self.area.size = (abs(self.start.left-mouse_tile_pos[0])+1, abs(self.start.top-mouse_tile_pos[1])+1)
            self.allow = (self.area.collidelist(self.app.factories.rect_list_all)==-1)
            self.allow = self.allow and (self.area.collidelist(self.tech_sites.rect_list_all)==-1)
            lookup = self.app.terrain.operate[self.area.left:self.area.right, self.area.top:self.area.bottom]
            self.allow = self.allow and np.min(lookup)
            
    def draw(self, surface):
        self.tech_sites.draw(surface)
        
        # draw cursor area
        if self.area.size!=(1,1):
            for i in range(self.area.left, self.area.right):
                for j in range(self.area.top, self.area.bottom):
                    screen_pos = self.app.terrain.demapping((i,j))
                    f_rect = pg.Rect(screen_pos, (TILE, TILE))
                    if self.allow:
                        surface.blit(self.bg_blue, f_rect.topleft)
                    else:
                        surface.blit(self.bg_red, f_rect.topleft)
        
        
    
        


class tech_sites:
    def __init__(self, app):
        self.app = app
        self.list = []
        self.active = None
        # load pic resources 
        self.img = [0 for i in self.app.data['tech-ui_img']]
        for img in self.app.data['tech-ui_img']:
            self.img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())

    @property
    def rect_list_all(self):
        f_list = []
        for item in self.list:
            f_list.append(item.rect)
        return f_list
    
    @property
    def selected_site(self):
        return self.active
    
    def select(self, num):
        if num!=-1: 
            self.active = self.list[num]
    
    def get_by_num(self, num):
        if num>-1 and num<len(self.list):
            return self.list[num]
        else:
            return None
    
    def add(self, area, content):
        # print(f'{area}')
        t_site = tech_area(self, self.app, area.copy(), content)
        self.active = t_site
        self.list.append(t_site)
        return t_site
    
    def draw(self, surface):
        for item in self.list:
            item.draw(surface)
    
    def update(self):
        pass
    
    
class tech_area:
    def __init__(self, list, app, rect, content):
        self.rect = rect
        self.app = app
        self.list = list
        self.result = np.zeros(rect.size, dtype=np.integer)
        # self.content = np.zeros(rect.size, dtype=np.integer)
        self.content = np.array(content)
        self.pic = self.create_pic(is_select=False)
        self.pic_selected = self.create_pic(is_select=True)
        num = randint(0,99999999)
        self.name = f'lab{num:0>8d}'
        self.status = TECH_A_NEW
        
        
    def draw(self, surface):
        screen_pos = self.app.terrain.demapping(self.rect.topleft)
        a_rect = pg.Rect(screen_pos, (self.rect.size[0]*TILE, self.rect.size[1]*TILE))
        if pg.Rect(VIEW_RECT).colliderect(a_rect):
            if self.list.selected_site!=self:
                surface.blit(self.pic, a_rect)
            else:
                surface.blit(self.pic_selected, a_rect)
        
    def create_pic(self, is_select):
        pic = pg.Surface((self.rect.size[0]*TILE, self.rect.size[1]*TILE), flags=pg.SRCALPHA)
        
        if is_select: 
            pic_res = 0
            pg.Surface.fill(pic, pg.Color(64,128,255,64))
            
        else:
            pic_res = 3
            pg.Surface.fill(pic, pg.Color(128,128,128,128))
            
        down_img = pygame.transform.rotate(self.list.img[pic_res], 180)
        left_img = pygame.transform.rotate(self.list.img[pic_res], 270)
        rigth_img = pygame.transform.rotate(self.list.img[pic_res], 90)
        tr_img = pygame.transform.rotate(self.list.img[1], 90)
        br_img = pygame.transform.rotate(self.list.img[1], 180)
        bl_img = pygame.transform.rotate(self.list.img[1], 270)
        for i in range(TILE,(self.rect.w-1)*TILE, TILE):
            a_rect = pg.Rect((i,0), self.rect.size)
            pic.blit(self.list.img[pic_res], a_rect)
            b_rect = pg.Rect((i,(self.rect.h-1)*TILE), self.rect.size)
            pic.blit(down_img, b_rect)
            
        for j in range(TILE,(self.rect.h-1)*TILE, TILE):
            a_rect = pg.Rect((0,j), self.rect.size)
            pic.blit(rigth_img, a_rect)
            b_rect = pg.Rect(((self.rect.w-1)*TILE,j), self.rect.size)
            pic.blit(left_img, b_rect)
            
        c_rect = pg.Rect((0,0), self.rect.size)
        pic.blit(self.list.img[1], c_rect)
        c_rect = pg.Rect(((self.rect.w-1)*TILE,0), self.rect.size)
        pic.blit(bl_img, c_rect)
        c_rect = pg.Rect(((self.rect.w-1)*TILE,(self.rect.h-1)*TILE), self.rect.size)
        pic.blit(br_img, c_rect)
        c_rect = pg.Rect((0,(self.rect.h-1)*TILE), self.rect.size)
        pic.blit(tr_img, c_rect)
        return pic
