import pygame as pg

class Tile():
    def __init__(self,surface,cor):
        self.cor = cor
        self.surface = surface

class Map():
    def __init__(self,screen,tiles):
        self.screen = screen
        self.tiles = tiles
        self.draw()
        
    def draw(self):
        for tile in self.tiles:
            self.screen.blit(tile.surface, tile.cor)

            
    def move(self,step,direcrionx=0,direcriony=0):
        """directions right:1,left:-1,up:1,down:-1"""
        for tile in self.tiles:
            tile.cor[0] += direcrionx*step
            tile.cor[1] += direcriony*step
        self.draw()

        