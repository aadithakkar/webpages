import pygame
import sys
import time
import asyncio

# Initialize pygame mixer
pygame.init()

saved = {}

def play(pitch):
    if pitch not in saved:
        saved[pitch] = pygame.mixer.Sound(f"note_set/note{pitch}.wav")
    saved[pitch].play()

screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("PlayPad")

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
cols = [(150, 0, 0),
        (150, 75, 0),
        (150, 150, 0),
        (75, 150, 0),
        (0, 150, 0),
        (0, 150, 75),
        (0, 150, 150),
        (0, 75, 150),
        (0, 0, 150),
        (75, 0, 150),
        (150, 0, 150),
        (255, 0, 125)]

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        if isinstance(self, MusicTile):
            self.groups = all_sprites
        else:
            self.groups = all_sprites, tabs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pygame.Surface([100, 100])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill((18, 18, 18))
        dx, dy = self.x // 100, self.y // 100
        colindex = dx + dy
        self.col = cols[colindex]
        self.times = 0
        pygame.draw.rect(self.image, self.col, pygame.Rect(5, 5, 90, 90), border_radius=8)
        pygame.draw.rect(self.image, (18, 18, 18), pygame.Rect(10, 10, 80, 80), border_radius=8)
        # self.image.fill((180, 18, 18))
        self.index = None
    def update(self):
        if self.times:
            self.times -= 1
            if not self.times:
                self.tempcol = self.col
            else:
                self.tempcol = [self.tempcol[i] + self.dists[i] for i in range(3)]
            self.image.fill((18, 18, 18))
            pygame.draw.rect(self.image, self.tempcol, pygame.Rect(5, 5, 90, 90), border_radius=8)
            pygame.draw.rect(self.image, (18, 18, 18), pygame.Rect(10, 10, 80, 80), border_radius=8)
            write(self.text(), (50, 50), self.tempcol, 50, self.image)
    def anim(self):
        self.times = 20
        self.tempcol = [220, 220, 220]
        self.dists = [int((self.col[i] - self.tempcol[i]) / 20) for i in range(3)]

class RecTile(Tile):
    def __init__(self, x, y, game):
        super().__init__(x, y)
        self.game = game
        self.state = "-"
        self.state = "REC"
        write(self.state, (50, 50), self.col, 50, self.image)
    def play(self):
        self.state = "REC" if self.state == "-" else "-"
        if self.state == "REC":
            self.game.rec = 1
        else:
            self.game.rec = 0
            self.game.last = time.perf_counter()
        self.anim()
    def text(self):
        return self.state

class ChordTile(Tile):
    def __init__(self, x, y, game):
        super().__init__(x, y)
        self.game = game
        self.arp = 0
    def play(self):
        self.arp = (self.arp + 1) % 4
        self.game.bass_index = 0
        match self.arp:
            case 0:
                self.game.played_bass = self.game.bass
            case 2:
                nl = []
                for n in self.game.bass:
                    nl += [n, n + 4, n + 7, n + 9, n + 7, n + 4, n, n + 4]
                self.game.played_bass = nl
            case 1:
                nl = []
                for n in self.game.bass:
                    nl += [n, n + 4, n + 7, n + 4]
                self.game.played_bass = nl
            case 3:
                nl = []
                for n in self.game.bass:
                    # nl += [n, n + 7, n + 4, n + 7] * 2
                    nl += [n, n + 4, n + 2, n + 4] * 2
                self.game.played_bass = nl
        self.anim()
    def text(self):
        return ["", "3C", "4C", "3I"][self.arp]

class SpeedTile(Tile):
    def __init__(self, x, y, game):
        super().__init__(x, y)
        self.game = game
        self.speed = round(1 / self.game.gap)
        write(self.text(), (50, 50), self.col, 50, self.image)
    def play(self):
        self.speed = self.speed % 4 + 1
        self.game.gap = 1 / self.speed
        self.anim()
    def text(self):
        return f'{self.speed}x'

class MusicTile(Tile):
    def __init__(self, x, y, pitch, index=None):
        self.groups = all_sprites
        super().__init__(x, y)
        self.pitch = pitch
        write(notes[pitch % 12], (50, 50), self.col, 50, self.image)
        self.shade = 100
        self.index = index
        self.times = 0
    def play(self):
        print(self.pitch)
        if self.index is None:
            place = pygame.mouse.get_pos()[0] - self.rect.x
            if 10 < place < 90:
                pitch = self.pitch
                self.anim()
            elif place > 90:
                pitch = self.pitch + 1
            else:
                pitch = self.pitch - 1
        else:
            pitch = self.pitch
            self.anim()
        play(pitch)
    def text(self):
        return notes[self.pitch % 12]

class ResetTile(Tile):
    def __init__(self, x, y, game):
        super().__init__(x, y)
        self.game = game
        write(self.text(), (50, 50), self.col, 50, self.image)
    def play(self):
        self.game.bass = []
        self.game.bass_index = 0
        self.game.played_bass = self.game.bass
        self.anim()
    def text(self):
        return "RST"

class MoreTile(Tile):
    def __init__(self, x, y, game):
        super().__init__(x, y)
        self.game = game
        write(self.text(), (50, 50), self.col, 50, self.image)
    def play(self):
        self.game.tab = 1 - self.game.tab
        self.game.load_tab()
    def text(self):
        return ". . ."

class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        # malkauns = [0, 3, 5, 8, 10]
        scale = [0, 2, 4, 5, 7, 9, 11]
        # scale = [0, 2, 3, 5, 7, 8, 10]
        # scale = [0, 2, 3, 5, 7, 8, 10, 11]
        # scale = [0, 2, 3, 5, 7, 8, 11]
        # scale = malkauns
        # scale = [i for i in range(12)]
        offset = 2
        index = 0
        self.tab = 0
        for y in range(6):
            for x in range(3):
                pitch = scale[index % len(scale)] + (index // len(scale)) * 12 + offset
                MusicTile(300 + x * 100, y * 100, pitch)
                index += 1
        self.last = time.perf_counter()
        self.gap = 0.5
        self.bass_tiles = {}
        index = 0
        for y in range(5):
            for x in range(3):
                pitch = scale[index % len(scale)] + (index // len(scale)) * 12 + offset - 12
                self.bass_tiles[index] = MusicTile(x * 100, y * 100 + 100, pitch, index)
                index += 1
        self.bass = []
        self.played_bass = self.bass
        self.bass_index = 0
        # RecTile(0, 0, self)
        # SpeedTile(100, 0, self)
        self.rec = 1
        self.load_tab()
    def load_tab(self):
        for spr in tabs:
            spr.kill()
        if self.tab == 0:
            RecTile(0, 0, self)
            ResetTile(100, 0, self)
            MoreTile(200, 0, self)
        else:
            ChordTile(0, 0, self)
            SpeedTile(100, 0, self)
            MoreTile(200, 0, self)
    async def run(self):
        while self.running:
            # print(self.bass)
            all_sprites.update()
            draw_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for tile in all_sprites:
                        if tile.rect.collidepoint(pygame.mouse.get_pos()):
                            tile.play()
                            if self.rec and tile.index is not None:
                                self.bass.append(tile.index)
                                print()
                elif event.type == pygame.KEYDOWN:
                    self.bass_index = 0
            if not self.rec:
                if time.perf_counter() - self.last > self.gap and self.played_bass:
                    # self.last = time.perf_counter()
                    self.last += self.gap
                    self.bass_tiles[self.played_bass[self.bass_index]].play()
                    self.bass_index = (self.bass_index + 1) % len(self.played_bass)
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)

def draw_screen(screen):
    screen.fill((18, 18, 18))
    all_sprites.draw(screen)

all_sprites = pygame.sprite.LayeredUpdates()
tabs = pygame.sprite.Group()

def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))

def main():
    asyncio.run(Game().run())

main()
