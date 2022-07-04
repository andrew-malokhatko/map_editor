from posixpath import splitdrive
import pygame 
import struct
from buttons import *
from pathlib import Path
from pygame.locals import *

x_offset = 200
y_offset = 200
size = 30
file_block_size = (300, 50)
file_block_color = (30, 30, 30)
text_color = (200,200,200)
RED = (255,0,0)
typing = False
last_file = 0
K_ENTER = 13

this_dir = Path(__file__).parent
cur_map = ""

ids = {
    0: (100, 160, 250),
    1: (200, 20, 120),
    2: (255, 100, 200),
    3: (47, 183, 21)
}

id_len = len(ids)

SCREENSIZE = (1600, 900)
screen = pygame.display.set_mode(SCREENSIZE)
button_left = SCREENSIZE[0] / 2 + 100

blocks = pygame.sprite.Group()
buttons = pygame.sprite.Group()
files = pygame.sprite.Group()
entries = pygame.sprite.Group()

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
        self.cur_color = RED if self.text == cur_map else text_color
        self.y = y
        self.rtext = font.render(text, False, self.cur_color, None)
        self.image = pygame.Surface(file_block_size)
        self.image.fill(file_block_color)
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

    def update(self, check_press, to_render, surface: pygame.Surface):
        global cur_map
        save()
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
    if cur_map == "" or len(files) == 0:
        return

    blocks.empty()

    with open(this_dir / cur_map, "rb") as f:
        data = f.read(5)
        while len(data) == 5:
            xdata, ydata, id = struct.unpack("hhb", data)
            block = Block(xdata, ydata, id)
            blocks.add(block)
            data = f.read(5)

def save():
    if cur_map == "" or len(files) == 0:
        return

    with open(this_dir / cur_map, "wb") as f:
        for block in blocks:
            data = struct.pack("hhb", block.to_load_x, block.to_load_y, block.id)
            f.write(data)

def get_all_files():
    global files
    global last_file
    global cur_map

    for file in files:
        file.kill()

    last_file = 0
    for file in this_dir.iterdir():
        if file.name.endswith(".map"):
            if last_file == 0: 
                cur_map = file.name
            fblock = File_block(1200, y_offset + (file_block_size[1] + 10) * last_file, file.name)
            files.add(fblock)
            last_file += 1

def fill_map():
    with open(this_dir / cur_map, "wb") as f:
        for i in range(20):
            for k in range(20):
                data = struct.pack("hhb", i, k, 0)
                f.write(data)

def new_file():
    global fblock
    global cur_map
    global last_file
    global typing

    typing = True
    fblock = File_block(1200, y_offset + (file_block_size[1] + 10) * last_file, "")
    files.add(fblock)
    last_file += 1

def create_new_file():
    global typing
    global cur_map
    global fblock

    typing = False
    cur_map = fblock.text
    fill_map()
    #fblock = None

def get_sprite(map: str, sprites):
    for sprite in sprites:
        if sprite.text == cur_map:
            return sprite

def delete_file():
    global cur_map

    sprites = files.sprites()
    sprite = get_sprite(cur_map, sprites)

    if not sprite or sprite == fblock and typing:
        return

    files.remove(sprite)
    sprite.kill()
    to_delete = this_dir / cur_map
    to_delete.unlink()
    cur_map = sprites[0]

    get_all_files()

load_button = Button(button_left, y_offset, 150, 50, (30,30,30), text_color, "Load", screen, load)
save_button = Button(button_left, y_offset + 100, 150, 50, (30,30,30), text_color, "Save", screen, save)
new_button = Button(button_left, y_offset + 200, 150, 50, (30,30,30), text_color, "New File", screen, new_file)
delete_button = Button(button_left, y_offset + 300, 150, 50, (30,30,30), text_color, "Delete File", screen, delete_file)

buttons.add(load_button, save_button, new_button, delete_button)
get_all_files()
load()
game_on = True

while game_on:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            load_button.check_pressed()
            save_button.check_pressed()
            new_button.check_pressed()
            delete_button.check_pressed()

            blocks.update()
            files.update(True, False, screen)
            files.update(False, True, screen)

        if event.type == pygame.KEYDOWN and typing:
            if event.key == K_ENTER and fblock.text != "": create_new_file()
            elif event.key == K_BACKSPACE: fblock.text = fblock.text[:-1]
            else:
                if event.unicode:
                    fblock.text += (event.unicode)
            fblock.update(False, True, screen)

    buttons.update(None)
    files.update(False, False, screen)
    blocks.draw(screen)
    pygame.display.flip()