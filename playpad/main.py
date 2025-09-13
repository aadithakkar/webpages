import pygame
import numpy as np
import io
import sys
import time
import asyncio

# Initialize pygame mixer
pygame.init()

def semitones_to_frequency(semitones):
    """Convert semitones past middle C (C4) to a frequency."""
    c4_freq = 261.63  # Middle C (C4) in Hz
    return c4_freq * (2 ** (semitones / 12))

import pygame
import numpy as np

def semitones_to_frequency(semitone):
    """Convert semitone offset from A4 (440 Hz) to frequency."""
    return 440.0 * (2 ** (semitone / 12.0))

def generate_triangle_wave(frequency, duration=1.0, sample_rate=44100, amplitude=0.5):
    """Generate a triangle wave with exponential decay."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    waveform = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1

    # Apply decay to simulate a plucked/struck instrument
    decay = np.exp(-3 * t)
    waveform = waveform * decay * amplitude

    return waveform.astype(np.float32)  # keep float until final mix

def mix_notes(semitones_list, duration=1.0):
    """Generate and mix multiple triangle waves together."""
    if not semitones_list:
        raise ValueError("At least one note must be provided.")

    sample_rate = 44100
    mixed_wave = np.zeros(int(sample_rate * duration), dtype=np.float32)

    for semitone in semitones_list:
        frequency = semitones_to_frequency(semitone)
        wave = generate_triangle_wave(frequency, duration, amplitude=0.4)
        mixed_wave[:len(wave)] += wave

    # Normalize
    max_val = np.max(np.abs(mixed_wave))
    if max_val > 0:
        mixed_wave /= max_val

    # Convert to stereo int16 for pygame
    stereo_wave = np.column_stack((mixed_wave, mixed_wave))
    stereo_wave = np.int16(stereo_wave * 32767)

    return stereo_wave

def play_notes(semitones_list, duration=1.0):
    """Generate, mix, and play notes using pygame."""
    pygame.mixer.pre_init(44100, -16, 2)
    pygame.init()

    sound_array = mix_notes(semitones_list, duration)
    sound = pygame.sndarray.make_sound(sound_array)
    sound.play()

    # pygame.time.wait(int(duration * 1000) + 100)

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
        self.anim()
    def text(self):
        return self.state

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
        play_notes([self.pitch])
        self.anim()
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
        scale = [0, 2, 4, 5, 7, 9, 11]
        # scale = [0, 2, 3, 5, 7, 8, 10]
        # scale = [i for i in range(12)]
        offset = 0
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
            SpeedTile(100, 0, self)
            MoreTile(200, 0, self)
    async def run(self):
        while self.running:
            while self.running:
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
                    if time.perf_counter() - self.last > self.gap and self.bass:
                        self.last = time.perf_counter()
                        self.bass_tiles[self.bass[self.bass_index]].play()
                        self.bass_index = (self.bass_index + 1) % len(self.bass)
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
