from enum import Enum
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

SC_WIDTH = 1920
SC_HIGHT = 1080
FPS = 60
P_INFO = 320
P_UP = 30
P_BOTTOM = 32

TILE = 64 
WIN_SIZE = (SC_WIDTH, SC_HIGHT)
# WIN_RECT = (0,0,SC_WIDTH,SC_HIGHT)
VIEW_RECT = (0,P_UP,SC_WIDTH-P_INFO-1,SC_HIGHT-P_BOTTOM-P_UP-1)
HALF_WIDTH = int((SC_WIDTH-P_INFO) / 2 / TILE)
HALF_HIGHT = int((SC_HIGHT-P_BOTTOM) / 2 / TILE)
FIELD_WIDTH = SC_WIDTH-P_INFO
FIELD_HIGHT = SC_HIGHT-P_BOTTOM-P_UP

INFO_WIDTH = P_INFO
INFO_HIGHT = SC_HIGHT
INFO_RECT = (FIELD_WIDTH, 0, SC_WIDTH-FIELD_WIDTH-1, SC_HIGHT-1)


PLANET_WIDTH = 100
PLANET_HIGHT = 100

# inventory
INV_MARGIN = 15
INV_CELL_W = 48
INV_CELL_H = 48
INV_CELL_SIZE = (INV_CELL_W, INV_CELL_H)
INV_CELL_COUNT = 100
INV_CELL_CW = 10
INV_CELL_CH = INV_CELL_COUNT // INV_CELL_CW
INV_WIDTH = INV_CELL_W*INV_CELL_CW+(INV_CELL_CW-1)+INV_MARGIN*2
INV_HIGHT = INV_CELL_H*INV_CELL_CH+(INV_CELL_CH-1)+INV_MARGIN*2
INV_SIZE = (INV_WIDTH, INV_HIGHT)
INV_POS = (FIELD_WIDTH // 2 - INV_WIDTH // 2+INV_MARGIN, FIELD_HIGHT // 2 - INV_HIGHT // 2+INV_MARGIN)
INV_RECT = (INV_POS[0], INV_POS[1], INV_WIDTH, INV_HIGHT)

class cursor_type(Enum):
    normal = 0
    dig = 1
