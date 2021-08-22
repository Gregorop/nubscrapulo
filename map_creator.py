import pygame as pg
from tile import GameTile, TileInFile
from constants import *
import pickle
import os

class MapCreator():
    def __init__(self,map_name):
        self.map_name = map_name
        self.tiles_folder = "tiles"
        self.load_all_tiles()
        self.tiles = list()

    def create_file(self):
        with open(os.path.join("maps",self.map_name+".map"),mode="wb") as file:
            pickle.dump(self, file)

    def load_all_tiles(self):
        self.all_tile_names = list(map(lambda name:name[:-5],os.listdir(self.tiles_folder)))

    def control(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.create_file()
                    exit()

    def create_cycle(self):
        window = pg.display.set_mode((1920,1080),flags=pg.FULLSCREEN)
        while True:
            self.control()
            pg.display.update()

if __name__ == "__main__":
    MapCreator("test").create_cycle()