import pygame as pg
from map_manager import Map,Tile
from constants import *

class Game():
    def __init__(self,res=(1920,1080)):
        self.res = res
        self.window = pg.display.set_mode(res,flags=pg.FULLSCREEN)

        self.map = Map(self.window,
                      [Tile(pg.image.load("samples/png/loc1.png"), [0,200]),
                        Tile(pg.image.load("samples/png/loc2.png"), [100,200])])

    def control(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()

    def start(self):
        while True:
            self.control()
            self.window.fill(BLACK)
            self.map.move(direcrionx=1,step=1)
            pg.display.update()

if __name__ == "__main__":
    Game().start()