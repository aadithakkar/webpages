import pygame, sys, asyncio

pygame.init()

screen = pygame.display.set_mode([400, 600])
pygame.display.set_caption("Slider Puzzle")

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, dimensions, col, bgcol):
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.dimx, self.dimy = dimensions
        self.width = self.dimx * 100
        self.height = self.dimy * 100
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = x * 100
        self.rect.y = y * 100
        self.selected = 0
        pygame.draw.rect(self.image, bgcol, pygame.Rect(5, 5, self.width - 10, self.height - 10))
        pygame.draw.rect(self.image, col, pygame.Rect(15, 15, self.width - 30, self.height - 30))
    def update(self):
        if self.selected:
            mx, my = pygame.mouse.get_pos()
            distx = max(-90, min(mx - self.rect.centerx, 90))
            disty = max(-90, min(my - self.rect.centery, 90))
            self.rect.x += distx
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.right > 400:
                self.rect.x = 400 - self.width
            hits = pygame.sprite.spritecollide(self, all_sprites, False)
            hits.remove(self)
            if hits:
                if distx < 0:
                    self.rect.x = max([hit.rect.right for hit in hits])
                else:
                    self.rect.x = min([hit.rect.x for hit in hits]) - self.width
            self.rect.y += disty
            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.bottom > 500:
                self.rect.y = 500 - self.height
            hits = pygame.sprite.spritecollide(self, all_sprites, False)
            hits.remove(self)
            if hits:
                if disty < 0:
                    self.rect.y = max([hit.rect.bottom for hit in hits])
                else:
                    self.rect.y = min([hit.rect.y for hit in hits]) - self.height

def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))

def draw_screen(screen):
    screen.fill((150, 150, 150))
    # pygame.draw.rect(screen, (250, 0, 0), pygame.Rect(0, 0, 100, 100))
    all_sprites.draw(screen)
    write(f"Level {level + 1}", (200, 550), (0, 0, 0), 50, screen)

all_sprites = pygame.sprite.LayeredUpdates()


codes = [
    "11001111111130200001",
    "11013001001112211001",
    "30120010112211001100",
    "21120300000201101140",
    "14022300000214000110",
    "30120020400101404001",
    "30110040401012400040",
    "30110011001111111111"
]


def init_scene(level):
    for spr in all_sprites:
        spr.kill()
    create_blocks(level)


def create_blocks(level):
    global winner
    code = codes[level]
    for i in range(5):
        for j in range(4):
            tilenum = code[j + 4 * i]
            if tilenum == "1":
                Tile(j, i, (1, 1), (200, 150, 0), (210, 160, 15))
            elif tilenum == "2":
                Tile(j, i, (1, 2), (0, 50, 200), (0, 65, 215))
            elif tilenum == "3":
                winner = Tile(j, i, (2, 2), (200, 0, 0), (210, 30, 30))
            elif tilenum == "4":
                Tile(j, i, (2, 1), (0, 200, 50), (0, 215, 65))

async def main():
    global winner, level
    level = 0
    running = True
    clock = pygame.time.Clock()
    winner = None
    snap = 1
    create_blocks(level)
    while running:
        all_sprites.update()
        draw_screen(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if my > 500:
                    level = (level + 1) % 8
                    init_scene(level)
                else:
                    for tile in all_sprites:
                        if tile.rect.x < mx < tile.rect.x + tile.width and tile.rect.y < my < tile.rect.y + tile.height:
                            tile.selected = 1
            elif event.type == pygame.MOUSEBUTTONUP:
                for tile in all_sprites:
                    if snap and tile.selected:
                        tile.rect.x = ((tile.rect.x + 50) // 100) * 100
                        tile.rect.y = ((tile.rect.y + 50) // 100) * 100
                    tile.selected = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    init_scene(level)
                elif event.key == pygame.K_s:
                    level = (level + 1) % 8
                    init_scene(level)
        # print(winner.rect.x, winner.rect.y)
        if winner.rect.x == 100 and winner.rect.y == 300:
            level = (level + 1) % 8
            init_scene(level)
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
