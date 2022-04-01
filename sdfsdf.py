import json
from random import randrange
import pygame as pg
import pygame_gui as gui
from myui import UIItemsList, myUIImage
from options import *
import cv2

from utils import convert_opencv_img_to_pygame, cvimage_grayscale


class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE, pg.SRCALPHA)
        self.surface = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.clock = pg.time.Clock()
        self.manager = gui.UIManager(WIN_SIZE, path.join(data_dir, 'theme.json'))
        
        f = open('data/data.json', encoding='utf-8')
        self.data = json.load(f)
        f.close
        
        self.field_img = [[0, 0] for i in self.data['terrain_type']]
        for img in self.data['terrain_type']:
            pic = pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha()
            cvimg = cv2.imread(path.join(img_dir, img['pic']))
            gray_image = cvimage_grayscale(cvimg)
            pic_gray = convert_opencv_img_to_pygame(gray_image)
            self.field_img[img['id']][0] = pic
            self.field_img[img['id']][1] = pic_gray

        self.block_img = [0 for i in self.data['block_type']]
        for img in self.data['block_type']:
            self.block_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())
        self.block_img_rect = self.block_img[1].get_rect()
        
        self.factory_img = [0 for i in self.data['factory_type']]
        for img in self.data['factory_type']:
            self.factory_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())
        
        
        
        self.wnd = gui.elements.UIWindow(pg.Rect(TECHINFO_WND_RECT), 
                                         self.manager,
                                         'Технология:',
                                         visible=False,
                                         object_id='tech_wnd'
                                         )        
        
        self.info_img = None 
        self.info_name = None
        self.info_text = None
        self.in_img = None
        self.out_img = None
        self.in_text = None
        self.out_text = None
        self.ok_button = None
        self.turn_text = None
        
        
    def show_window(self, bp_id):
        
        bp = self.data['factory_type'][bp_id]
        
        wnd_width = self.wnd.get_relative_rect().width-self.wnd.border_width*2-self.wnd.shadow_width*2
        pos = 0
        paddind = (10,0,10,0)
        pic = self.factory_img[bp_id]
        pic_size = pic.get_size()
        if self.info_img:
            self.info_img.set_image(pic)
            self.info_img.set_relative_position((wnd_width//2-pic_size[0]//2,pos))
            pos += self.info_img.get_relative_rect().h
        else:
            self.info_img = myUIImage(pg.Rect((wnd_width//2-pic_size[0]//2,pos),pic_size), pic, self.manager, container=self.wnd)
            pos += self.info_img.get_relative_rect().h
            
        name = bp['name']
        if self.info_name:
            self.info_name.set_text(name)
            self.info_name.set_relative_position((0,pos))
            pos += self.info_name.get_relative_rect().h
        else:
            self.info_name = gui.elements.UILabel(pg.Rect(0,pos,wnd_width,-1), name, self.manager, container=self.wnd)
            pos += self.info_name.get_relative_rect().h

        info_text = bp.get('info')
        if info_text:
            if self.info_text:
                self.info_text.set_text(info_text)
                self.info_text.set_relative_position((0, pos))
                pos += self.info_text.get_relative_rect().h
            else:
                self.info_text = gui.elements.UITextBox(
                    info_text, 
                    pg.Rect(0,pos,wnd_width,-1), 
                    self.manager, 
                    container=self.wnd, 
                    wrap_to_height=True,
                    object_id='wnd_info_text')
                pos += self.info_text.get_relative_rect().h
        elif self.info_text:
            self.info_text.kill()
            self.info_text = None

    
        res_in = bp.get('in')
        if res_in:
            if self.in_text:
                self.in_text.set_relative_position((paddind[0],pos))
                pos += self.in_text.get_relative_rect().h
                self.in_img.set_items_list(self._create_items_list(res_in))
                self.in_img.set_relative_position((paddind[0],pos))
                pos += self.in_img.get_relative_rect().h
            else:
                self.in_text = gui.elements.UILabel(pg.Rect(paddind[0],pos,wnd_width-paddind[2]-paddind[0],-1), 'Вход:', self.manager, container=self.wnd, object_id='label_left')
                pos += self.in_text.get_relative_rect().h
                self.in_img = UIItemsList(pg.Rect(paddind[0],pos,-1,-1), self._create_items_list(res_in), self.manager, container=self.wnd, object_id='item_label_m')
                pos += self.in_img.get_relative_rect().h
        elif self.in_text:
            self.in_text.kill()
            self.in_text = None
            self.in_img.kill()
            self.in_img = None
        
        res_out = bp.get('out')
        if res_out:
            if self.out_text:
                self.out_text.set_relative_position((paddind[0],pos))
                pos += self.out_text.get_relative_rect().h
                self.out_img.set_items_list(self._create_items_list(res_out))
                self.out_img.set_relative_position((paddind[0],pos))
                pos += self.out_img.get_relative_rect().h
            else:
                self.out_text = gui.elements.UILabel(pg.Rect(paddind[0],pos,wnd_width-paddind[2]-paddind[0],-1), 'Выход:', self.manager, container=self.wnd, object_id='label_left')
                pos += self.out_text.get_relative_rect().h
                self.out_img = UIItemsList(pg.Rect(paddind[0],pos,-1,-1), self._create_items_list(res_out), self.manager, container=self.wnd, object_id='item_label_m')
                pos += self.out_img.get_relative_rect().h
        elif self.out_text:
            self.out_text.kill()
            self.out_text = None
            self.out_img.kill()
            self.out_img = None

        turn = bp.get('time')
        if turn:
            if self.turn_text:
                self.turn_text.set_text(f'Производственный цикл (сек): {turn}')
                self.turn_text.set_relative_position((paddind[0],pos))
                pos += self.turn_text.get_relative_rect().h
            else:
                self.turn_text = gui.elements.UILabel(pg.Rect(paddind[0],pos,wnd_width-paddind[2]-paddind[0],-1), f'Производственный цикл (сек): {turn}', self.manager, container=self.wnd, object_id='label_left')
                pos += self.turn_text.get_relative_rect().h
        elif self.turn_text:
            self.turn_text.kill()
            self.turn_text = None


        if not self.ok_button:
            ok_rect = pg.Rect(paddind[0],0,wnd_width-paddind[2]-paddind[0],-1)
            ok_rect.bottomright = (-10,-10)
            self.ok_button = gui.elements.UIButton(ok_rect,'OK', self.manager, container=self.wnd, 
                                                   anchors={'left': 'right',
                                                            'right': 'right',
                                                            'top': 'bottom',
                                                            'bottom': 'bottom'})
            pos += self.ok_button.get_relative_rect().h

        self.wnd.show()

        
        
    def hide_window(self):
        self.wnd.hide()        
        

    def run(self):
        # self.show_window(0)
        while True:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                
                if event.type == pg.USEREVENT:
                    if event.user_type == gui.UI_BUTTON_PRESSED:
                        if event.ui_element.text == 'OK':
                            self.hide_window()
                self.manager.process_events(event)
            keystate = pg.key.get_pressed()
            if keystate[pg.K_1]: 
                self.show_window(0)
            if keystate[pg.K_2]: 
                self.show_window(1)
            if keystate[pg.K_3]: 
                self.show_window(2)
            dt = self.clock.tick(60)/1000.0
            self.update(dt)
            self.draw()    
            pg.display.flip()
       
    def update(self, dt):
        self.manager.update(dt)                   
        
    def draw(self):
        self.surface.fill(pg.Color('gray30'))        
        self.screen.blit(self.surface, (0,0))
        self.manager.draw_ui(self.screen)

    def _create_items_list(self, block_list):
        list = []
        for item in block_list:
            image_surface=self.block_img[int(item['id'])]
            list.append({'img':image_surface, 'count': item['count']})
        return(list)




if __name__ == '__main__':
    game_app = game()
    game_app.run()