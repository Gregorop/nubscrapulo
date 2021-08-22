import pygame as pg
from map_manager import Map
from tile import GameTile, TileInFile
from constants import *

class Game:
    def __init__(self,res=(1920,1080)):
        self.res = res
        self.window = pg.display.set_mode(res,flags=pg.FULLSCREEN)

        self.map = Map(self.window,
                      [GameTile("sofa"),
                        GameTile("filler1"),
                        GameTile("bookcase"),
                        GameTile("filler1"),
                        GameTile("filler1")])

    def control(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                if event.key == pg.K_d:
                    self.map.move(direcrionx=1,step=1)
                if event.key == pg.K_a:
                    self.map.move(direcrionx=-1,step=1)

    def start(self):
        while True:
            self.window.fill(BLACK)
            self.map.draw_map()
            self.control()
            pg.display.update()

if __name__ == "__main__":
    Game().start()