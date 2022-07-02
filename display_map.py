import pygame 
import struct
from buttons import *

x_offset = 200
y_offset = 200
size = 30

cur_map = "map.bin"

ids = {
    0: (100, 160, 250),
    1: (200, 20, 120)
}

SCREENSIZE = (1600, 900)
screen = pygame.display.set_mode(SCREENSIZE)

blocks = pygame.sprite.Group()
buttons = pygame.sprite.Group()

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, id):
        super().__init__()
        self.x = x * size + x_offset
        self.y = y * size + y_offset
        self.to_load_x = x
        self.to_load_y = y
        self.id = id
        self.image = pygame.Surface((size, size))
        self.image.fill(ids[id])
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

    def update(self):
        self.click()

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            id = bool(self.id)
            self.id = int(not id)
            #self.id = 0 if self.id == 1 else 1
        self.image.fill(ids[self.id])

def load():

    for block in blocks:
        block.kill()

    with open(cur_map, "rb") as f:
        data = f.read(5)
        while len(data) == 5:
            xdata, ydata, id = struct.unpack("hhb", data)
            block = Block(xdata, ydata, id)
            blocks.add(block)
            data = f.read(5)

def save():
    
    with open(cur_map, "wb") as f:
        for block in blocks:
            data = struct.pack("hhb", block.to_load_x, block.to_load_y, block.id)
            f.write(data)

load_button = Button(SCREENSIZE[0] / 2 + 200, y_offset, 100, 50, (30,30,30), (200,200,200), "Load", screen, load)
save_button = Button(SCREENSIZE[0] / 2 + 200, y_offset + 100, 100, 50, (30,30,30), (200,200,200), "Save", screen, save)

buttons.add(load_button, save_button)

game_on = True

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            load_button.check_pressed()
            save_button.check_pressed()
            for block in blocks:
                block.update()

    buttons.update(None)
    blocks.draw(screen)
    pygame.display.flip()

    

