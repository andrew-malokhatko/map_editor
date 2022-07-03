import pathlib
import pygame 
import struct
from buttons import *
from pathlib import Path

x_offset = 200
y_offset = 200
size = 30
file_block_size = (300, 50)
file_block_color = (30, 30, 30)
text_color = (200,200,200)
RED = (255,0,0)

this_dir = Path(__file__).parent
cur_map = "map.bin"

ids = {
    0: (100, 160, 250),
    1: (200, 20, 120),
    2: (255, 100, 200),
    3: (47, 183, 21)
}

id_len = len(ids)

SCREENSIZE = (1600, 900)
screen = pygame.display.set_mode(SCREENSIZE)

blocks = pygame.sprite.Group()
buttons = pygame.sprite.Group()
files = pygame.sprite.Group()

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
            self.id = (self.id + 1) % id_len
        self.image.fill(ids[self.id])


class File_block(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.x = x
        self.red = False
        self.text = text
        self.cur_color = RED if self.text == "map.bin" else text_color
        self.y = y
        self.rtext = font.render(text, False, self.cur_color, None)
        self.image = pygame.Surface(file_block_size)
        self.image.fill(file_block_color)
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    
    def update(self, check_press, to_render, surface: pygame.Surface):
        global cur_map
        if check_press:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                cur_map = self.text
                load()
                for fbl in files:
                    fbl.cur_color = text_color
                self.cur_color = RED

        if to_render:
            self.rtext = font.render(self.text, False, self.cur_color, None)

        surface.blit(self.image, self.rect)
        surface.blit(self.rtext, self.rect)

def load():
    for block in blocks:
        block.kill()

    with open(this_dir / cur_map, "rb") as f:
        data = f.read(5)
        while len(data) == 5:
            xdata, ydata, id = struct.unpack("hhb", data)
            block = Block(xdata, ydata, id)
            blocks.add(block)
            data = f.read(5)

def save():
    with open(this_dir / cur_map, "wb") as f:
        for block in blocks:
            data = struct.pack("hhb", block.to_load_x, block.to_load_y, block.id)
            f.write(data)

def get_all_files():
    global files
    for file in files:
        file.kill()
    i = 0
    for file in this_dir.iterdir():
        if file.name.endswith(".bin"):
            fblock = File_block(1200, y_offset + (file_block_size[1] + 10) * i, file.name)
            files.add(fblock)
            i += 1

load_button = Button(SCREENSIZE[0] / 2 + 200, y_offset, 100, 50, (30,30,30), text_color, "Load", screen, load)
save_button = Button(SCREENSIZE[0] / 2 + 200, y_offset + 100, 100, 50, (30,30,30), text_color, "Save", screen, save)

buttons.add(load_button, save_button)
get_all_files()
load()
game_on = True

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            load_button.check_pressed()
            save_button.check_pressed()

            blocks.update()
            files.update(True, False, screen)
            files.update(False, True, screen)

    buttons.update(None)
    files.update(False, False, screen)
    blocks.draw(screen)
    pygame.display.flip()

    

