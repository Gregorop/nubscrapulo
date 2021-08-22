import pygame as pg
from tile import GameTile, TileInFile,MenuTile
from constants import *
import pickle
import os

class TileMenu:
    def __init__(self,tile_name_list,map_creator,side=1): #1 RIGHT 0 LEFT
        self.tile_name_list = tile_name_list
        self.menuTile_to_show = list()
        self.side = side
        self.map_creator = map_creator
        self.map_creator.add_menu(self)
        self.rect = pg.Rect(0,0,0,self.map_creator.h)
        self.change_rect()
        self.load_tiles()

    def change_rect(self):
        self.amount_column = 1
        self.rect.width =  self.amount_column * tile_side*2
        self.rect.x = self.map_creator.w - (self.rect.width)

    def reside(self):
        if self.side: 
            self.side,self.rect.x = 0,0
            for tile in self.menuTile_to_show:
                tile.cor[0] = tile_side/2
        else:
            self.side = 1
            self.change_rect()
            for tile in self.menuTile_to_show:
                tile.cor[0] =  self.map_creator.w - tile_side - tile_side/2

    def control(self,event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_PAGEUP:
                print("here menu going up")
            if event.key == pg.K_PAGEDOWN:
                print("here menu going down")
            if event.key == pg.K_BACKSLASH:
                self.reside()

    def load_tiles(self,map_name=""):
        for name in self.tile_name_list:
            new_menu_tile = MenuTile(name)
            ok_category = map_name in new_menu_tile.maps
            simple_tile = len(new_menu_tile.maps)==0
            if ok_category or simple_tile:
                
                new_menu_tile.cor[0] = self.rect.x + tile_side/2
                new_menu_tile.cor[1] = tile_side/2 + len(self.menuTile_to_show) * tile_side * 1.2 
                self.menuTile_to_show.append(new_menu_tile)

    def draw(self):
        pg.draw.rect(self.map_creator.window, BLACK, self.rect)
        for tile in self.menuTile_to_show:
            tile.draw(self.map_creator.window)

class MapCreator:
    def __init__(self,map_name,w=1920,h=1080,full=1):
        self.w,self.h,self.full = w,h,full
        self.map_name = map_name
        self.tiles_folder = "tiles"
        self.load_all_tiles()
        self.tiles = list()
        if self.full:
            self.window = pg.display.set_mode((self.w,self.h),flags=pg.FULLSCREEN)
        else:
            self.window = pg.display.set_mode((self.w,self.h))
        self.menus = list()

    def add_menu(self,menu):
        self.menus.append(menu)

    def create_file(self):
        with open(os.path.join("maps",self.map_name+".map"),mode="wb") as file:
            pickle.dump(self.tiles, file)

    def load_all_tiles(self): 
        self.all_tile_names = list(map(lambda name:name[:-5],os.listdir(self.tiles_folder)))

    def control(self):
        for event in pg.event.get():
            for menu in self.menus:
                menu.control(event)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.create_file()
                    exit()

    def create_cycle(self):
        while True:
            self.control()
            self.window.fill(WHITE)
            for menu in self.menus:
                menu.draw()
            pg.display.update()

if __name__ == "__main__":
    t = MapCreator("test")
    menu = TileMenu(t.all_tile_names, t)
    t.create_cycle()