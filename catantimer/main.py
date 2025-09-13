import pygame, sys, time, asyncio

pygame.init()

screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("Game Title")

DARK_COLS = [(140, 0, 0), (0, 120, 150), (150, 100, 0), (150, 150, 150)]
COLS = [(180, 40, 20), (0, 150, 200), (200, 150, 0), (225, 225, 225)]

SECS_PER_TURN = 120
BUTTON_SIZE = 90
BUTTON_GAP = 8

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, wid, height, game):
        self.groups = all_sprites, buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pygame.Surface([wid, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

class Start(Button):
    def __init__(self, x, y, game):
        super().__init__(x, y, 300, 150, game)
        self.image.fill((200, 200, 200))
        write("START", (150, 75), (0, 0, 0), 60, self.image)
    def use(self):
        if self.game.order:
            self.game.start()

class TurnButton(Button):
    def __init__(self, x, y, dcol, col, id, game):
        super().__init__(x, y, 100, 100, game)
        self.image.fill(dcol)
        pygame.draw.rect(self.image, col, pygame.Rect(10, 10, 80, 80))
        self.active = 0
        self.dcol = dcol
        self.col = col
        self.index = None
        self.id = id
    def use(self):
        if not self.active:
            self.active = 1
            self.index = len(self.game.order) + 1
            self.game.order.append(self.id)
            self.image.fill((0, 0, 0))
            pygame.draw.rect(self.image, self.col, pygame.Rect(10, 10, 80, 80))
            write(self.index, (50, 50), (0, 0, 0), 50, self.image)
        elif self.index == len(self.game.order):
            self.game.order.pop()
            self.active = 0
            self.image.fill(self.dcol)
            pygame.draw.rect(self.image, self.col, pygame.Rect(10, 10, 80, 80))

class Pause(Button):
    def __init__(self, x, y, dcol, col, game):
        super().__init__(x, y, BUTTON_SIZE, BUTTON_SIZE, game)
        self.image.fill(dcol)
        pygame.draw.rect(self.image, col, pygame.Rect(BUTTON_GAP, BUTTON_GAP, (BUTTON_SIZE - BUTTON_GAP * 2), (BUTTON_SIZE - BUTTON_GAP * 2)))
        write("P/R", (BUTTON_SIZE / 2, BUTTON_SIZE / 2), dcol, 40, self.image)
    def use(self):
        self.game.paused = 1 - self.game.paused

class Extension(Button):
    def __init__(self, x, y, amt, dcol, col, game):
        super().__init__(x, y, BUTTON_SIZE, BUTTON_SIZE, game)
        self.image.fill(dcol)
        pygame.draw.rect(self.image, col, pygame.Rect(BUTTON_GAP, BUTTON_GAP, (BUTTON_SIZE - BUTTON_GAP * 2), (BUTTON_SIZE - BUTTON_GAP * 2)))
        self.amt = amt
        write(f"+{amt}", (BUTTON_SIZE / 2, BUTTON_SIZE / 2), dcol, 50, self.image)
        self.alpha = 255
        self.fading = 0
    def use(self):
        if not self.fading:
            self.fading = 1
            self.game.extensions[self.game.turn].remove(self.amt)
            self.game.stime += self.amt * 60
            self.game.shade = 255
    def update(self):
        if self.fading:
            self.alpha -= 30
            if self.alpha <= 0:
                self.kill()
            else:
                self.image.set_alpha(self.alpha)

class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.order = []
        self.game_stage = 2
        for i in range(4):
            TurnButton(150 * i + 125, 350, DARK_COLS[i], COLS[i], i, self)
        Start(250, 550, self)
    def start(self):
        self.turn_index = -1
        self.stage = 1
        self.extensions = [[1, 1, 3] for _ in range(4)]
        self.shade = 0
        self.game_stage = 0
        self.place_order = self.order + self.order[::-1]
        self.paused = 0
        self.next_turn()
    async def run(self):
        while self.running:
            all_sprites.update()
            self.draw_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.shade = 0
                    mouse = pygame.mouse.get_pos()
                    actioned = 0
                    for spr in all_sprites:
                        if spr.rect.collidepoint(mouse):
                            actioned = 1
                            spr.use()
                            break
                    if not actioned and self.game_stage < 2:
                        if mouse[1] > 70 + BUTTON_SIZE:
                            if self.stage == 0:
                                self.stage = 1
                                self.stime = time.perf_counter()
                                self.paused = 0
                                for i, amt in enumerate(self.extensions[self.turn]):
                                    Extension(50 + (BUTTON_SIZE + 25) * i, 50, amt, DARK_COLS[self.turn], COLS[self.turn], self)
                                Pause(800 - 50 - BUTTON_SIZE, 50, DARK_COLS[self.turn], COLS[self.turn], self)
                            else:
                                self.next_turn()
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)
    def next_turn(self):
        for spr in all_sprites:
            spr.kill()
        if self.game_stage == 0:
            self.turn_index += 1
            if self.turn_index >= len(self.place_order):
                self.stage = 0
                self.game_stage = 1
                self.turn_index = 0
                return
            self.stime = time.perf_counter()
            self.turn = self.order[self.turn_index] if self.game_stage == 1 else self.place_order[self.turn_index]
            Pause(800 - 50 - BUTTON_SIZE, 50, DARK_COLS[self.turn], COLS[self.turn], self)
        else:
            self.stage = 0
            self.turn_index = (self.turn_index + 1) % len(self.order)
            self.turn = self.order[self.turn_index] if self.game_stage == 1 else self.place_order[self.turn_index]
    def draw_screen(self, screen):
        if self.game_stage < 2:
            screen.fill(DARK_COLS[self.turn])
            pygame.draw.rect(screen, COLS[self.turn], pygame.Rect(25, 25, 750, 750), border_radius=20)
            if self.stage == 0:
                write("Roll & Distribute", (400, 400), (0, 0, 0), 70, screen)
            else:
                if self.paused:
                    self.stime = time.perf_counter() - self.elapsed
                else:
                    self.elapsed = time.perf_counter() - self.stime
                if self.elapsed <= SECS_PER_TURN:
                    if self.game_stage == 0:
                        write(f"Place Structure {1 if self.turn_index < len(self.order) else 2}", (400, 300), (0, 0, 0), 60, screen)
                    remaining = SECS_PER_TURN - self.elapsed
                    mins = int(remaining // 60)
                    secs = int(remaining % 60)
                    if secs < 10:
                        secs =  f"0{secs}"
                    if self.shade > 0:
                        self.shade -= 5
                        self.shade = max(0, self.shade)
                    if self.paused:
                        self.shade = 75
                    write(f"{mins}:{secs}", (400, 400), [self.shade for _ in range(3)], 90, screen)
                else:
                    self.next_turn()
        else:
            screen.fill((200, 200, 200))
            write("Catan Timer", (400, 200), (0, 0, 0), 75, screen)
        all_sprites.draw(screen)

all_sprites = pygame.sprite.LayeredUpdates()
buttons = pygame.sprite.Group()

def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))

def main():
    asyncio.run(Game().run())

main()
