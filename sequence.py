import pygame as pg
from options import *
import json


class sequence:
    def __init__(self, app, file):
        self.app = app
        f = open(file, encoding='utf-8')
        self.data = json.load(f)
        f.close
        
    def update(self, step, owner):
        pass
