import pygame as pg
from options import *
import json


class sequence:
    def __init__(self, app, file):
        self.app = app
        f = open(file, encoding='utf-8')
        self.data = json.load(f)
        f.close
        
    def get_command(self, command_step):
        return(self.data[command_step])
    
    def go_next(self, command_step, result):
        if command_step is None: return
        if result: 
            if 'go_succ' in self.data[command_step].keys():
                return(self.data[command_step]['go_succ'])
            else:
                return(command_step)
        else:
            if 'go_fail' in self.data[command_step].keys():
                return(self.data[command_step]['go_fail'])
            else:
                return(command_step)
        
    def get_msg(self, command_step, result):
        if command_step is None: return
        if result: 
            if 'msg_succ' in self.data[command_step].keys():
                return(self.data[command_step]['msg_succ'])
            else:
                return('')
        else:
            if 'msg_fail' in self.data[command_step].keys():
                return(self.data[command_step]['msg_fail'])
            else:
                return('')
            
    
    def update(self, step, owner):
        pass
