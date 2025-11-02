import pygame, sys, random, time, asyncio

pygame.init()

screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("Game Title")

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pygame.Surface([100, 100])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.chord = self.gen_chord()
        self.next = self.gen_chord()
        self.bpm = 60
        self.stime = time.perf_counter()
        self.last_count = 1
        self.gray = 200
    def gen_chord(self):
        tonic = random.randint(0, 11)
        if random.random() < 0.5:
            return self.note_name(tonic) + "m"
        else:
            return self.note_name(tonic)
    def note_name(self, note):
        return NOTE_NAMES[note]
    async def run(self):
        while self.running:
            all_sprites.update()
            self.draw_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.chord = self.gen_chord()
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)
    def draw_screen(self, screen):
        if self.gray < 200:
            self.gray = min(200, self.gray + 1)
        all_sprites.draw(screen)
        total = 240 / self.bpm
        prop = ((time.perf_counter()) - self.stime) / total
        wid = 800 - prop * 800
        if prop >= 1:
            prop = 0
            wid = 800
            self.stime += total
            self.chord, self.next = self.next, self.gen_chord()
        count = int(prop // 0.25 + 1)
        if count != self.last_count:
            # print((prop - 0.25 * (prop // 0.25)) * total)
            self.last_count = count
            self.gray = 170
        screen.fill((self.gray, self.gray, self.gray))
        write(count, (50, 50), (0, 0, 0), 50, screen)
        write(self.chord, (400, 400), (0, 0, 0), 80, screen)
        write(self.next, (400, 500), (100, 100, 100), 60, screen)
        pygame.draw.rect(screen, (250, 250, 250), pygame.Rect(0, 780, 800, 20))
        pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(0, 780, wid, 20))

all_sprites = pygame.sprite.LayeredUpdates()

def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))

def main():
    asyncio.run(Game().run())

main()
