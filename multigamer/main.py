import pygame
import sys
import random
import time
import asyncio


pygame.init()
screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("Multigamer")


class Bird(pygame.sprite.Sprite):
    def __init__(self, layer, x, y, game):
        self._layer = layer
        self.groups = all_sprites, birds
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([20, 20])
        self.image.fill((0, 250, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.y_speed = 0
        self.shields = 1

    def update(self):
        global game_running
        self.y_speed += 0.25
        self.rect.y += self.y_speed
        if self.rect.y > self.game.y + 380:
            self.rect.y = self.game.y + 380
            self.y_speed = 0
        elif self.rect.y < self.game.y:
            self.rect.y = self.game.y
            self.y_speed = 0
        if pygame.sprite.spritecollide(self, pipes, False):
            if self.shields == 0:
                game_running = 0
            else:
                self.shields -= 1
                for pipe in pipes:
                    pipe.kill()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, layer, x, y, game, height, u):
        self._layer = layer
        self.groups = all_sprites, pipes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([40, height])
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.x_pos = x
        self.speed = -3
        self.u = u

    def update(self):
        global score
        self.x_pos += self.speed
        self.rect.x = self.x_pos
        if self.rect.right < self.game.x:
            self.kill()
        elif self.u and self.rect.x < self.game.bird.rect.x:
            self.u = 0
            TextFade(self.game.x + 200, self.game.y + 200, "+1")
            score += 1
        if score >= 75 and self.speed == -3:
            self.speed = -3.5
        elif score >= 150 and self.speed == -3.5:
            self.speed = -4
        elif score >= 250 and self.speed == -4:
            self.speed = -5


class Timer(pygame.sprite.Sprite):
    def __init__(self, x, y, total_time, fatal=1, game=None):
        self._layer = 4
        self.groups = all_sprites, timers
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([400, 15])
        self.image.fill((100, 0, 0))
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = x
        self.rect.y = y
        self.total_time = total_time
        self.fatal = fatal
        self.game = game
        self.stime = time.time()

    def update(self):
        global game_running
        self.image.fill((250, 250, 250))
        current = time.time()
        if current < self.stime:
            self.stime = current
        rectwidth = 400 - ((current - self.stime) / self.total_time) * 400
        if rectwidth <= 0:
            if self.fatal:
                game_running = 0
            else:
                self.kill()
                self.game.kill()
            return None
        pygame.draw.rect(self.image, (100, 0, 0), pygame.Rect(0, 0, rectwidth, 15))


class ReactGame(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 3
        self.groups = all_sprites, reactgames
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([400, 400])
        self.image.fill((200, 200, 200))
        self.key = str(random.randint(4, 9))
        write(f"Click '{self.key}'!", (200, 200), (0, 0, 0), 50, self.image)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = x
        self.rect.y = y
        self.timer = Timer(x, y + 385, 2, 0, self)

    def response(self, resp):
        global score
        if resp == self.key:
            for timer in timers:
                timer.stime += 5
            TextFade(self.x + 200, self.y + 200, "+5")
            score += 5
        self.timer.kill()
        self.kill()


class MemGame(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 3
        self.groups = all_sprites, memgames
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([400, 400])
        self.image.fill((180, 180, 180))
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = x
        self.rect.y = y
        self.seq = None
        self.showing = 1
        self.responses = []
        self.length = 3
        self.colors = [(150, 0, 0), (0, 0, 150), (150, 150, 0), (0, 150, 0)]
        self.labels = "RTFG"
        self.timer = Timer(x, y + 385, 25)
        self.solved = 0
        self.boost = 1

    def update(self):
        self.image.fill((180, 180, 180))
        if self.seq is None:
            self.seq = [random.randint(0, 3) for _ in range(self.length)]
            self.responses = []
            self.showing = 1
        if self.showing:
            sequence = self.seq
        else:
            sequence = self.responses
        total_len = 40 * len(sequence) + 25 * (len(sequence) - 1)
        start_pos = 200 - total_len / 2
        for i, col in enumerate(sequence):
            x = start_pos + i * 65
            pygame.draw.rect(self.image, self.colors[col], pygame.Rect(x, 60, 40, 40))
            write(self.labels[col], [x + 20, 80], (0, 0, 0), 30, self.image)
        for i in range(2):
            for j in range(2):
                x = 121 * i + 82
                y = 120 * j + 140
                count = 2 * j + i
                pygame.draw.rect(self.image, self.colors[count], pygame.Rect(x, y, 115, 115))
                write(self.labels[count], [x + 57, y + 57], (0, 0, 0), 50, self.image)

    def response(self, resp):
        global score
        if self.seq is not None:
            col = self.labels.index(resp)
            self.showing = 0
            if col == self.seq[len(self.responses)]:
                self.responses.append(col)
                if self.responses == self.seq:
                    score += self.boost
                    TextFade(self.x + 200, self.y + 200, f"+{self.boost}")
                    self.timer.stime += 10
                    self.solved += 1
                    self.seq = None
                    if self.solved > 5:
                        self.length = 4
                    if self.solved > 15:
                        self.length = 5
                        self.boost = 2
            else:
                self.timer.stime -= 3
                self.seq = None


class MathGame(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 3
        self.groups = all_sprites, mathgames
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([400, 400])
        self.image.fill((180, 180, 180))
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = x
        self.rect.y = y
        self.mathtimer = Timer(x, y + 385, 25)
        self.answer = None

    def update(self):
        if self.answer is None:
            self.a = random.randint(100, 1000)
            self.b = random.randint(100, 1000)
            self.answer = self.a + self.b
            self.question = f"{self.a} + {self.b}?"
            self.options = [self.answer]
            for _ in range(2):
                newopt = self.answer
                while newopt in self.options:
                    newopt = self.answer + random.randint(-20, 20)
                self.options.append(newopt)
            random.shuffle(self.options)
        self.image.fill((180, 180, 180))
        write(self.question, (200, 150), (0, 0, 0), 50, self.image)
        for i, opt in enumerate(self.options):
            write(f"{i + 1}) {opt}", (200, 225 + i * 50), (0, 0, 0), 40, self.image)

    def response(self, resp):
        global score, gamemode
        if self.options[int(resp) - 1] == self.answer:
            self.answer = None
            self.mathtimer.stime += 4 if gamemode == 0 else 6
            score += 1
            TextFade(self.x + 200, self.y + 200, "+1")
        else:
            self.answer = None
            self.mathtimer.stime -= 3


class Fade(pygame.sprite.Sprite):
    def __init__(self):
        self._layer = 10
        self.groups = all_sprites, fades
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([800, 800])
        self.image.fill((0, 0, 0))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.stime = time.time()
        self.toggled = 0

    def update(self):
        global score, game_running, reset_points, shield_points, next_mini
        elapsed = time.time() - self.stime
        next_mini = None
        if elapsed < 2:
            self.image.set_alpha(elapsed / 2 * 250)
        elif elapsed < 3 and not self.toggled:
            self.toggled = 1
            for sprite in all_sprites:
                if sprite != self:
                    sprite.kill()
            FlappyGame(0, 0)
        elif elapsed < 3:
            self.image.set_alpha(250 - (elapsed - 2) * 250)
        else:
            game_running = 1
            score = 0
            reset_points = 0
            shield_points = 0
            self.kill()


class ChessGame(pygame.sprite.Sprite):
    def __init__(self, x, y, drawings):
        self._layer = 3
        self.groups = all_sprites, chessgames
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([400, 400])
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = x
        self.rect.y = y
        self.pieces = drawings
        self.selected = None
        puzzle = random.choice([["-kr--R-rppp--pp--n--pq-----p---p-Q-N--b-------B-------P-R-----K-", ((3, 4), (2, 2))],
                                ["---------p--r-r-------pk--q---pp---P-------------P---NK-R-------", ((5, 6), (6, 4))],
                                ["-kr--R-rp-p--pp--np-pq-----p---p-Q----b-------B-------P-R-----K-", ((6, 5), (2, 1))],
                                ["q--------kpB----p-N--K--P--p-------P-------P--------------------", ((5, 2), (6, 1))],
                                ["--q------p-k---rp-----p-----p-P---N-----P---P--p-P-----P--KB--R-", ((3, 7), (6, 4))],
                                ["rnbq-rk--p-n-pbpp--pp-p-P--N----------Q--B--PN---P-B-PPP--R--RK-", ((2, 7), (2, 0))]
                                ])
        self.chesspos = puzzle[0]
        self.answer = puzzle[1]
        self.coords_from_piece = {"k": (0, 0), "q": (50, 0), "b": (100, 0), "n": (150, 0), "r": (200, 0), "p": (250, 0)}
        for i in range(8):
            for j in range(8):
                col = [BOARD_WHITE, BOARD_BLACK][(i+j) % 2]
                pygame.draw.rect(self.image, col, pygame.Rect(50*i, 50*j, 50, 50))
                piece = self.chesspos[8 * j + i]
                if piece != "-":
                    coords = self.coords_from_piece[piece.lower()]
                    piecex = coords[0]
                    piecey = coords[1] + 50 * (piece == piece.lower())
                    self.image.blit(self.pieces, (50 * i, 50 * j), (piecex, piecey, 50, 50))
        self.timer = Timer(x, y + 385, 10, 0, self)

    def response(self, mouse):
        mousecoords = (mouse[0] // 50 - 8, mouse[1] // 50 - 8)
        if not (0 <= mousecoords[0] <= 15 and 0 <= mousecoords[1] <= 15):
            return None
        self.image.fill((200, 200, 200))
        if self.selected is None:
            self.selected = mousecoords
        else:
            safe = 0
            clickedsquare = self.chesspos[mousecoords[1] * 8 + mousecoords[0]]
            if self.chesspos[self.selected[1] * 8 + self.selected[0]] == "-":
                self.selected = None
                safe = 1
            elif clickedsquare.upper() == clickedsquare and clickedsquare != "-":
                self.selected = mousecoords
                safe = 1
            global score
            if (self.selected, mousecoords) == self.answer:
                TextFade(self.x + 200, self.y + 200, "+15")
                score += 15
            if not safe:
                self.kill()
                self.timer.kill()
                return None
        for i in range(8):
            for j in range(8):
                col = [BOARD_WHITE, BOARD_BLACK][(i+j) % 2]
                if (i, j) == self.selected:
                    col = (180, 180, 0)
                pygame.draw.rect(self.image, col, pygame.Rect(50*i, 50*j, 50, 50))
                piece = self.chesspos[8 * j + i]
                if piece != "-":
                    coords = self.coords_from_piece[piece.lower()]
                    piecex = coords[0]
                    piecey = coords[1] + 50 * (piece == piece.lower())
                    self.image.blit(self.pieces, (50 * i, 50 * j), (piecex, piecey, 50, 50))


class TextFade(pygame.sprite.Sprite):
    def __init__(self, x, y, txt, col=(0, 150, 0)):
        self._layer = 5
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([50, 50], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        write(txt, (25, 25), col, 40, self.image)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = x - 25
        self.rect.y = y - 25
        self.stime = time.time()

    def update(self):
        current = time.time()
        self.image.set_alpha(max(0, 250 - ((current - self.stime) * 250)))
        if time.time() - self.stime >= 1:
            self.kill()


class FlappyGame(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 1
        self.groups = all_sprites, flapgames
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([400, 400])
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = x
        self.rect.y = y
        self.lastpipe = time.time() - 2
        self.bird = Bird(self._layer + 1, x + 100, y + 200, self)

    def update(self):
        self.image.fill((200, 200, 200))
        if not pipes and time.time() - self.lastpipe > 5:
            self.lastpipe = time.time()
            between_pipes = 100 if gamemode == 0 else 125
            opening = random.randint(1, 399 - between_pipes)
            Pipe(self._layer + 1, self.x + 400, 0, self, opening, 1)
            Pipe(self._layer + 1, self.x + 400, opening + between_pipes, self, 400 - between_pipes - opening, 0)
        if self.bird.shields > 0:
            write(self.bird.shields, (20, 380), (0, 0, 0), 50, self.image)


def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))


running = True
score = 0
game_running = 1
clock = pygame.time.Clock()


all_sprites = pygame.sprite.LayeredUpdates()
birds = pygame.sprite.Group()
pipes = pygame.sprite.Group()
mathgames = pygame.sprite.Group()
memgames = pygame.sprite.Group()
flapgames = pygame.sprite.Group()
reactgames = pygame.sprite.Group()
chessgames = pygame.sprite.Group()
fades = pygame.sprite.Group()
timers = pygame.sprite.Group()
reset_interval = 15
reset_points = 0
shield_points = 0
next_mini = None
# Mode 0 = Normal, 1 = Easy
gamemode = 0
FlappyGame(0, 0)


BOARD_WHITE = (235, 236, 208)
BOARD_BLACK = (115, 149, 82)
my_image = pygame.image.load("800px-Chess_Pieces_Sprite.svg.png")
drawings = pygame.transform.smoothscale(my_image, (300, 100.125))
# ChessGame(400, 400, drawings)


async def main():
    global running, score, game_running, clock, reset_interval, reset_points, shield_points, next_mini, gamemode
    while running:
        screen.fill((0, 0, 0))
        if game_running:
            all_sprites.update()
            if score >= 2 and not mathgames:
                MathGame(400, 0)
            elif score >= 10 and not memgames:
                MemGame(0, 400)
                next_mini = time.time() + 10
            if next_mini is not None and next_mini < time.time():
                next_mini = time.time() + random.randint(15, 25)
                randnum = random.randint(1, 2)
                if randnum == 1:
                    ReactGame(400, 400)
                else:
                    ChessGame(400, 400, drawings)
            if score // reset_interval > reset_points:
                for timer in timers:
                    timer.stime = time.time()
                reset_points = score // reset_interval
                if score >= 60 and reset_interval == 15:
                    reset_interval = 30
                    reset_points = 0
            if score // 40 > shield_points:
                for flapgame in flapgames:
                    flapgame.bird.shields += 1
                shield_points = score // 40
        else:
            fades.update()
        if not game_running and not fades:
            Fade()
        all_sprites.draw(screen)
        pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(300, 0, 200, 50))
        write(score, (400, 25), (0, 0, 0), 50, screen)
        if gamemode == 1:
            write("(E)", (475, 25), (0, 0, 0), 40, screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_SPACE, pygame.K_UP]:
                    for bird in birds:
                        bird.y_speed = -5
                elif event.unicode != "":
                    if event.unicode in "123":
                        for mathgame in mathgames:
                            mathgame.response(event.unicode)
                    elif event.unicode in "rtfg":
                        for memgame in memgames:
                            memgame.response(event.unicode.upper())
                    elif event.unicode in "456789":
                        for reactgame in reactgames:
                            reactgame.response(event.unicode)
                    elif event.unicode == "|":
                        score = 150
                    elif event.unicode == "M":
                        gamemode = 1 - gamemode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                print(mouse)
                mc = (mouse[0] // 400, mouse[1] // 400)
                if mc == (0, 0):
                    for bird in birds:
                        bird.y_speed = -5
                elif mc == (1, 0):
                    y = mouse[1]
                    clicked = (y - 225) // 50 + 1
                    if 1 <= clicked <= 3:
                        for mathgame in mathgames:
                            mathgame.response(clicked)
                elif mc == (0, 1):
                    x = mouse[0]
                    y = mouse[1]
                    clicked = ((y - 540) // 120) * 2 + (x - 82) // 121
                    if 0 <= clicked <= 3:
                        for memgame in memgames:
                            memgame.response("RTFG"[clicked].upper())
                elif mc == (1, 1):
                    for chessgame in chessgames:
                        chessgame.response(mouse)
        clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())
