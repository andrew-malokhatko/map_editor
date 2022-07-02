import pygame 
import struct

x_offset = 200
y_offset = 200
size = 10

ids = {
    0: (100, 160, 250),
    1: (200, 20, 120)
}

SCREENSIZE = (1600, 900)
screen = pygame.display.set_mode(SCREENSIZE)

blocks = pygame.sprite.Group()

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, id):
        super().__init__()
        self.x = x * size + x_offset
        self.y = y * size + y_offset
        self.id = id
        self.image = pygame.Surface((size, size))
        self.image.fill(ids[id])
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

    def display_values(self): # _ = cringe
        print(self.x)
        print(self.y)
        print(self.id)


with open("map.bin", "rb") as f:
    data = f.read(5)
    while len(data) == 5:
        xdata, ydata, id = struct.unpack("hhb", data)
        data = f.read(5)
        block = Block(xdata, ydata, id)
        blocks.add(block)

game_on = True

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

    blocks.draw(screen)
    pygame.display.flip()

    

