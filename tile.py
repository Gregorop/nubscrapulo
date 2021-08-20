import pygame as pg
import pickle
import os

class TileInFile():
    '''a map file builds with this tiles'''
    def __init__(self,surface_file:str,cor:list=[0,0],types:list=[],name:str=""):
        self.cor = cor
        self.surface_file = surface_file
        self.types = types
        self.name = name
        self.save()
    
    def save(self):
        with open(os.path.join("tiles",self.name+".tile"),mode="wb") as file:
            pickle.dump(self, file)

class GameTile():
    '''a tile that we draw on screen'''
    def __init__(self,tyile_file:str):
        
        self.tyile_file = tyile_file
        self.load()
        self.surface = pg.image.load(self.loaded.surface_file)
        self.cor = self.loaded.cor
        self.types = self.loaded.types
        self.name = self.loaded.name

    def load(self):
        with open(os.path.join("tiles",self.tyile_file+".tile"),mode="rb") as file:
            self.loaded = pickle.load(file)

    def draw(self,screen):
        screen.blit(self.surface, self.cor)

def createAllTileFiles():
    TileInFile(os.path.join("samples","png","loc1.png"),name="bookcase")
    TileInFile(os.path.join("samples","png","loc2.png"),name="filler1")
    TileInFile(os.path.join("samples","png","loc3.png"),name="sofa")

if __name__ == "__main__":
    
    window = pg.display.set_mode((800,600))
    test = GameTile("sofa")
    test.draw(window)
    while True:
        pg.display.update()