import pygame as pg
import pickle
import os

class TileInFile:
    '''a map file builds with this tiles'''
    def __init__(self,surface_files:dict,cor:list=[0,0],types:list=[],name:str="",maps=[]):
        self.cor = cor
        self.surface_files = surface_files
        self.types = types
        self.name = name
        self.maps = maps
        self.save()
    
    def save(self):
        with open(os.path.join("tiles",self.name+".tile"),mode="wb") as file:
            pickle.dump(self, file)

class MapBuilderTile:
    def __init__(self,tile_file:str,cor:list,map_name:str):
        
        self.tile_file = tile_file
        self.load()
        self.name = self.loaded.name
        self.maps = self.loaded.maps
        self.surface_files = self.loaded.surface_files
        self.cor = cor
        self.map_name = map_name

    def load(self):
        with open(os.path.join("tiles",self.tile_file+".tile"),mode="rb") as file:
            self.loaded = pickle.load(file)

    def save(self):
        with open(os.path.join("maps",self.map_name,self.name+".tile"),mode="wb") as file:
            pickle.dump(self, file)
    

class GameTile:
    '''a tile that we draw in game'''
    def __init__(self,tile_file:str):
        
        self.tile_file = tile_file
        self.load()
        self.name = self.loaded.name
        self.maps = self.loaded.maps
        self.surface_files = self.loaded.surface_files
        self.tile_pics = dict()
        for surface_name in self.surface_files.keys():
            self.tile_pics[surface_name] = pg.image.load(self.surface_files[surface_name])
        
        self.tile_pics["main"] = self.tile_pics[self.name]
        self.tile_pics["show"] = self.tile_pics["main"]
        self.cor = self.loaded.cor
        self.types = self.loaded.types
    
    def set_show_pic(self,new_pic):
        self.tile_pics["show"] =  self.tile_pics[new_pic]

    def get_pics_list(self):
        return list(self.tile_pics.keys())

    def load(self):
        with open(os.path.join("tiles",self.tile_file+".tile"),mode="rb") as file:
            self.loaded = pickle.load(file)

    def draw(self,screen):
        screen.blit(self.tile_pics["show"], self.cor)

class MenuTile(GameTile):
    def onclick(self,pos):
        if self.rect.collidepoint(pos):
            tmp = MovingTile(self.tile_file)
            tmp.move(pos)
            return tmp

class MovingTile(GameTile):
    def move(self,pos):
        self.cor = pos

def createAllTileFiles():
    TileInFile({"bookcase":os.path.join("samples","png","loc1.png")},name="bookcase")
    TileInFile({"filler1":os.path.join("samples","png","loc2.png")},name="filler1")
    TileInFile({"sofa":os.path.join("samples","png","loc3.png"),
                "bookcase":os.path.join("samples","png","loc1.png")},name="sofa")

if __name__ == "__main__":
    createAllTileFiles()
    window = pg.display.set_mode((800,600))
    test = GameTile("sofa")
    print(test.get_pics_list())
    
    while True:
        test.draw(window)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                if event.key == pg.K_d:
                    test.set_show_pic("bookcase")
                if event.key == pg.K_a:
                    test.set_show_pic("sofa")
        pg.display.update()