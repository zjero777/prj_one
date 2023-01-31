from enum import Enum
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
data_dir = path.join(path.dirname(__file__), 'data')
fonts_dir = path.join(path.dirname(__file__), 'fonts')

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

PLANET_WIDTH = 1000
PLANET_HIGHT = 1000

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

#tech
TECH_WND_WIDTH = int((2/3)*SC_WIDTH)
TECH_WND_HIGHT = int((2/3)*SC_HIGHT)
TECH_WND_POS = (SC_WIDTH//2-TECH_WND_WIDTH//2,SC_HIGHT//2-TECH_WND_HIGHT//2)
TECH_WND_RECT = (TECH_WND_POS[0], TECH_WND_POS[1], TECH_WND_WIDTH, TECH_WND_HIGHT)

TECHINFO_WND_WIDTH = int((1/3)*SC_WIDTH)
TECHINFO_WND_HIGHT = int((2/3)*SC_HIGHT)
TECHINFO_WND_POS = (SC_WIDTH//2-TECHINFO_WND_WIDTH//2,SC_HIGHT//2-TECHINFO_WND_HIGHT//2)
TECHINFO_WND_RECT = (TECHINFO_WND_POS[0], TECHINFO_WND_POS[1], TECHINFO_WND_WIDTH, TECHINFO_WND_HIGHT)

class cursor_type(Enum):
    normal = 0
    dig = 1
    tech = 2

TECH_A_NEW = 0
TECH_A_PROGRESS = 1
TECH_A_RESULT = 2
TECH_A_COMPLETE = 3
TECH_A_DELETE = 4


FSTAT_NONE = 0
FSTAT_CHG_RECIPE = 1
FSTAT_PROD = 2
FSTAT_REMOVE = 3

CHG_INSPECT_IN = 0
CHG_CHANGE_IN = 1
CHG_INSPECT_OUT = 2
CHG_CHANGE_OUT = 3
CHG_ALLOW_RECIPE = 4
CHG_PURGE_IN = 5
CHG_PURGE_OUT = 6

PROD_INSPECT_IN = 0
PROD_BEGIN_PROD = 1
PROD_WAIT_FOR_COMPLETE = 2
PROD_INSPECT_OUT = 3

TMPL3_2 = 0
TMPL2_3 = 1