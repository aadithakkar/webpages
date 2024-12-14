import pygame
import sys
import asyncio
import random

pygame.init()
screen = pygame.display.set_mode([1000, 600])
pygame.display.set_caption("Stereogram Maker")

RES = 20
PIXPERTILE = 16
SHIFT = 10
IN_COL = 0
TILESIZE = int(400 / RES)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, code, size, layer=2):
        self.groups = tiles
        self._layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.code = code
        self.image = pygame.Surface([size, size])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        length = int(len(code)**0.5)
        pixelsize = int(size / length)
        for i in range(length):
            for j in range(length):
                if IN_COL:
                    col = list(code[length*j+i])
                    for i in range(3):
                        col[i] = col[i] * 250
                else:
                    col = [int(code[length*j+i]) * 250 for _ in range(3)]
                pygame.draw.rect(self.image, col, pygame.Rect(i*pixelsize, j*pixelsize, pixelsize, pixelsize))


def gen_code(pixpertile, incolor):
    if not incolor:
        return [random.randint(0, 1) for _ in range(pixpertile)]
    else:
        return [[random.randint(0, 1) for _ in range(3)] for _ in range(pixpertile)]

def create_stereo(hidden_image):
    for x in range(RES):
        for y in range(RES):
            code = gen_code(PIXPERTILE, IN_COL)
            char = hidden_image[RES * y + x]
            Tile(75 + TILESIZE * x, 100 + TILESIZE * y, code, TILESIZE)
            Tile(480 + TILESIZE * x, 100 + TILESIZE * y, code, TILESIZE)
            if char == "1":
                Tile(480 + TILESIZE * x - SHIFT, 100 + TILESIZE * y, code, TILESIZE, 3)
                nc = gen_code(PIXPERTILE, IN_COL)
                Tile(480 + TILESIZE * x, 100 + TILESIZE * y, nc, TILESIZE, 1)
            else:
                Tile(480 + TILESIZE * x, 100 + TILESIZE * y, code, TILESIZE)

def change_mode(tiles, hidden_image):
    global mode
    for tile in tiles:
        tile.kill()
    mode = 1 - mode
    if mode == 1:
        create_stereo(hidden_image)

running = True
clock = pygame.time.Clock()
tiles = pygame.sprite.LayeredUpdates()
# hidden_image = "0000000000000000000000000000000000000000000000000000000000000000000000011000000000000000001010000000000000011100110000000000001000000010000000000100000000010000000011010000000010000001000000001000010000001111110011000100000000001010101001000000000001011010100000000000000001101000000000000000100100000000000000000101000000000000000000100000000000000000000000000000000000000000000000000000000000000000"

async def main():
    global mode, tiles
    mode = 0
    mousedown = 0
    hidden_image = "0000001111111100000000001111111111110000001111111111111111000111111111111111111001111111000011111110011111000000001111100011000000001100110000100011000111100100000101111001111010000001011110001100100000001011000000010000000010000000000100000000010000110010000000000100011110100000000000100111110000000000001000110100000000000001000010000000000000010000100000000000000010010000000000000000100100000000"
    ntile = "0"
    while running:
        screen.fill((200, 200, 200))
        if mode == 0:
            for x in range(RES):
                for y in range(RES):
                    curtile = int(hidden_image[RES * y + x])
                    col = [(1 - curtile) * 250 for _ in range(3)]
                    pygame.draw.rect(screen, col, pygame.Rect(300 + TILESIZE * x, 100 + TILESIZE * y, TILESIZE, TILESIZE))
        tiles.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    change_mode(tiles, hidden_image)
                elif event.key == pygame.K_c:
                    hidden_image = "0" * RES ** 2
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = 1
                mouse = pygame.mouse.get_pos()
                if mode == 0:
                    if 300 < mouse[0] < 700 and 100 < mouse[1] < 500:
                        clicked = ((mouse[0] - 300) // TILESIZE, (mouse[1] - 100) // TILESIZE)
                        clickednum = clicked[1] * RES + clicked[0]
                        ntile = str(1 - int(hidden_image[clickednum]))
                        hidden_image = hidden_image[:clickednum] + ntile + hidden_image[clickednum + 1:]
                    else:
                        if mouse[0] < 500:
                            hidden_image = "0" * RES ** 2
                        else:
                            change_mode(tiles, hidden_image)
                else:
                    change_mode(tiles, hidden_image)
            elif event.type == pygame.MOUSEBUTTONUP:
                mousedown = 0
            elif event.type == pygame.MOUSEMOTION:
                if mode == 0 and mousedown:
                    mouse = pygame.mouse.get_pos()
                    if 300 < mouse[0] < 700 and 100 < mouse[1] < 500:
                        clicked = ((mouse[0] - 300) // TILESIZE, (mouse[1] - 100) // TILESIZE)
                        clickednum = clicked[1] * RES + clicked[0]
                        hidden_image = hidden_image[:clickednum] + ntile + hidden_image[clickednum + 1:]
        await asyncio.sleep(0)
        clock.tick(60)

asyncio.run(main())
