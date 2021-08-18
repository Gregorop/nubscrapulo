import pygame as pg

class Game():
    def __init__(self,res=(1920,1080)):
        self.res = res
        self.window = pg.display.set_mode(res,flags=pg.FULLSCREEN)

    def control(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

    def start(self):
        while True:
            self.control()
            pg.display.update()

if __name__ == "__main__":
    Game().start()