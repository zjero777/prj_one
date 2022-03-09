from random import randrange
import pygame as pg

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1920, 1080))
        self.clock = pg.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
            
            self.screen.fill(pg.Color(0,0,0))
            x1 = randrange(0,1919)
            x2 = randrange(0,1919)
            y1 = randrange(0,1079)
            y2 = randrange(0,1079)
            
            pg.draw.line(self.screen, pg.Color(255,0,0), (x1,y1), (x2,y2),5)
            pg.display.flip()
        


if __name__ == '__main__':
    game_app = game()
    game_app.run()