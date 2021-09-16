import pygame as pg
from tile import GameTile, TileInFile,MenuTile,MapBuilderTile
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
                tile.cor[0] = self.map_creator.w - tile_side - tile_side/2
        for tile in self.menuTile_to_show:
            tile.rect = pg.Rect(tile.cor[0], tile.cor[1],tile_side,tile_side) 

    def control(self,event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_PAGEUP:
                print("here menu going up")
            if event.key == pg.K_PAGEDOWN:
                print("here menu going down")
            if event.key == pg.K_BACKSLASH:
                self.reside()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for menu_tile in self.menuTile_to_show:
                    if menu_tile.onclick(event.pos):
                        self.map_creator.select_tile = menu_tile.onclick(event.pos)

    def load_tiles(self,map_name=""):
        for name in self.tile_name_list:
            new_menu_tile = MenuTile(name)
            ok_category = map_name in new_menu_tile.maps
            simple_tile = len(new_menu_tile.maps)==0
            if ok_category or simple_tile:
                
                new_menu_tile.cor[0] = self.rect.x + tile_side/2
                new_menu_tile.cor[1] = tile_side/2 + len(self.menuTile_to_show) * tile_side * 1.2
                new_menu_tile.rect = pg.Rect(new_menu_tile.cor[0], new_menu_tile.cor[1],tile_side,tile_side) 
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
        self.tiles_to_save = list()
        if self.full:
            self.window = pg.display.set_mode((self.w,self.h),flags=pg.FULLSCREEN)
        else:
            self.window = pg.display.set_mode((self.w,self.h))
        self.menus = list()
        self.select_tile = None

    def add_menu(self,menu):
        self.menus.append(menu)

    def create_map_file(self):
        if not os.path.exists(os.path.join("maps",self.map_name)):
            os.mkdir(os.path.join("maps",self.map_name))

        with open(os.path.join("maps",self.map_name,self.map_name+".map"),mode="wb") as file:
            pickle.dump(self.tiles_to_save, file)

    def load_map_file(self,map_name):
        with open(os.path.join("maps",self.map_name,self.map_name+".map"),mode="rb") as file:
            self.tiles_to_save = pickle.load(file)
            for tile_to_save in self.tiles_to_save:
                tmp = GameTile(tile_to_save.tile_file)
                tmp.cor = tile_to_save.cor
                self.tiles.append(tmp) 

    def load_all_tiles(self): 
        self.all_tile_names = list(map(lambda name:name[:-5],os.listdir(self.tiles_folder)))

    def clean_space_click_check(self,pos):
        for menu in self.menus:
            if menu.rect.collidepoint(pos):
                return False
        return True

    def find_repaint_tile(self,pos):
        for tile in self.tiles_to_save:
            if tile.cor[0]//tile_side == pos[0]//100 and tile.cor[1]//tile_side == pos[1]//100:
                self.tiles_to_save.remove(tile)
        for tile in self.tiles:
            if tile.cor[0]//tile_side == pos[0]//100 and tile.cor[1]//tile_side == pos[1]//100:
                 self.tiles.remove(tile)

    def control(self):
        for event in pg.event.get():
            for menu in self.menus:
                menu.control(event)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.create_map_file()
                    exit()

            if event.type == pg.MOUSEMOTION:
                if self.select_tile:
                    self.select_tile.move(event.pos)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.clean_space_click_check(event.pos):
                if "full" in self.select_tile.types:
                    x = (event.pos[0]//100) * tile_side
                    y = (event.pos[1]//100) * tile_side
                else:
                    x,y = event.pos
                keys = pg.key.get_pressed()
                if not keys[pg.K_SPACE]:
                    self.find_repaint_tile([x,y])
                if self.select_tile:
                    tile_save = MapBuilderTile(self.select_tile.tile_file,list(event.pos),self.map_name)
                    tile_show = GameTile(self.select_tile.tile_file)

                    tile_save.cor[0],tile_show.cor[0] = x,x
                    tile_save.cor[1],tile_show.cor[1] = y,y
                    
                    self.tiles_to_save.append(tile_save)
                    self.tiles.append(tile_show)

    def create_cycle(self):
        while True:
            self.control()
            self.window.fill(WHITE)
            for tile in self.tiles:
                tile.draw(self.window)
            for menu in self.menus:
                menu.draw()
            if self.select_tile:
                self.select_tile.draw(self.window)
            pg.display.update()

if __name__ == "__main__":
    map_name = "test4"
    t = MapCreator(map_name)
    if os.path.exists(os.path.join("maps",map_name)):
        t.load_map_file(map_name)
    menu = TileMenu(t.all_tile_names, t)
    t.create_cycle()