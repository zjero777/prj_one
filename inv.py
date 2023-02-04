from logging import warn
from random import randrange
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *


class inv:
    # # inventory
    # INV_MARGIN = 15
    # INV_CELL_W = 48
    # INV_CELL_H = 48
    # INV_CELL_SIZE = (INV_CELL_W, INV_CELL_H)
    # INV_CELL_COUNT = 100
    # INV_CELL_CW = 10
    # INV_CELL_CH = INV_CELL_COUNT // INV_CELL_CW
    # INV_WIDTH = INV_CELL_W*INV_CELL_CW+(INV_CELL_CW-1)+INV_MARGIN*2
    # INV_HIGHT = INV_CELL_H*INV_CELL_CH+(INV_CELL_CH-1)+INV_MARGIN*2
    # INV_SIZE = (INV_WIDTH, INV_HIGHT)
    # INV_POS = (FIELD_WIDTH // 2 - INV_WIDTH // 2+INV_MARGIN, FIELD_HIGHT // 2 - INV_HIGHT // 2+INV_MARGIN)
    # INV_RECT = (INV_POS[0], INV_POS[1], INV_WIDTH, INV_HIGHT)

    def __init__(self, app, pos=(-2, -2), inv_cells=(10, 10), inv_cell_h=48, inv_margin=15):
        '''
        pos x = -1 - left,  -2 - center, -3 rigth, y = -1 top, -2 center, -3 left
        '''
        self.app = app

        self.selected_cell = None
        self.cells = []
        self.hover_cell_num = None
        self.is_open = False

        # calculate const position and view
        self.inv_cell_cw, self.inv_cell_ch = inv_cells
        self.inv_margin = inv_margin
        self.inv_cell_w = inv_cell_h
        self.inv_cell_h = inv_cell_h
        self.inv_cell_size = (self.inv_cell_w, self.inv_cell_h)
        self.inv_cell_count = self.inv_cell_cw * self.inv_cell_ch
        self.inv_width, self.inv_hight = self.inv_cell_w*self.inv_cell_cw + \
            (self.inv_cell_cw-1)+self.inv_margin*2, self.inv_cell_h * \
            self.inv_cell_ch+(self.inv_cell_ch-1)+self.inv_margin*2
        self.inv_size = (self.inv_width, self.inv_hight)
        self.inv_pos_x, self.inv_pos_y = pos
        if self.inv_pos_x < 0:
            if self.inv_pos_x == -1:
                self.inv_pos_x = 0
            if self.inv_pos_x == -2:
                self.inv_pos_x = FIELD_WIDTH // 2 - self.inv_width // 2
            if self.inv_pos_x == -3:
                self.inv_pos_x = FIELD_WIDTH - self.inv_width
        if self.inv_pos_y < 0:
            if self.inv_pos_y == -1:
                self.inv_pos_y = 0
            if self.inv_pos_y == -2:
                self.inv_pos_y = FIELD_HIGHT // 2 - self.inv_hight // 2
            if self.inv_pos_y == -3:
                self.inv_pos_y = FIELD_HIGHT - self.inv_hight
        self.inv_pos = (self.inv_pos_x, self.inv_pos_y)

        self.surface = pg.Surface(self.inv_size)
        self.bgimg = pg.image.load(path.join(img_dir, 'invbg.png')).convert()
        self.bgimgactive = pg.image.load(
            path.join(img_dir, 'invbgactive.png')).convert()
        self.bgrect = self.bgimg.get_rect()
        self.font = pg.font.Font(None, 15)

        self.first_pressed = True
        self.first_click = True

    @property
    def item(self):
        if self.selected_cell is None:
            return(None)
        return(self.cells[self.selected_cell])

    def get_cell(self, pos):
        pos2 = ((pos[0]-self.inv_pos_x-self.inv_margin)//(self.inv_cell_w+1),
                (pos[1]-self.inv_pos_y-self.inv_margin)//(self.inv_cell_h+1))
        cell = (pos[0]-self.inv_pos_x-self.inv_margin)//(self.inv_cell_w+1) + \
            (pos[1]-self.inv_pos_y-self.inv_margin)//(self.inv_cell_h+1) * \
            self.inv_cell_cw
        if cell < 0 or cell > self.inv_cell_count or pos2[0] < 0 or pos2[0] > self.inv_cell_cw-1:
            return(None, None)
        else:
            if cell > -1 and cell < len(self.cells):
                block = self.cells[cell]
            else:
                block = None
            return(cell, block)

    def get_pos(self, cell_number):
        col = cell_number % self.inv_cell_cw
        row = cell_number // self.inv_cell_cw
        return (col * (self.inv_cell_w+1) + self.inv_margin, row *(self.inv_cell_h+1)+self.inv_margin)

    def update(self):
        if not self.app.is_modal(self):
            return
        self.keystate = pg.key.get_pressed()
        self.mouse_button = pg.mouse.get_pressed()
        self.mouse_pos = pg.mouse.get_pos()

    def draw(self):
        if not self.is_open:
            return

        self.surface.fill(pg.Color(33, 40, 45))

        #  draw bg cells
        for i in range(self.inv_cell_count):
            pos = self.get_pos(i)
            if self.hover_cell_num == i:
                # hover
                self.surface.blit(self.bgimgactive, pos)
            else:
                # normal
                self.surface.blit(self.bgimg, pos)
