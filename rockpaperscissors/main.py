import pygame, sys, random, asyncio

pygame.init()

screen = pygame.display.set_mode([800, 1000])
pygame.display.set_caption("Rock Paper Scissors Simulator")

PLAYERSIZE = 40
COLORS = {"rock": (100, 100, 100), "paper": (150, 150, 150), "scissors": (200, 150, 0)}

def draw_screen(screen, population, speed, updated, percents, cpop):
    screen.fill((200, 200, 200))
    all_sprites.draw(screen)
    write(f"Population: {population}", (200, 950), (0, 0, 0) if updated else (150, 150, 150), 50, screen)
    write(f"Speed: {speed}", (600, 950), (0, 0, 0) if updated else (150, 150, 150), 50, screen)
    current_pop = cpop
    rock = int(percents["rock"] / current_pop * 800)
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, 800, rock, 100))
    paper = int(percents["paper"] / current_pop * 800)
    pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(rock, 800, paper, 100))
    pygame.draw.rect(screen, (200, 150, 0), pygame.Rect(rock + paper, 800, 800 - rock - paper, 100))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        global totals
        self.groups = all_sprites, players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([PLAYERSIZE, PLAYERSIZE])
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = random.random() * 2 - 1
        self.dy = (1 - self.dx ** 2) ** 0.5
        self.speed = speed
        self.type = random.choice(["rock", "paper", "scissors"])
        totals[self.type] += 1
        self.image.fill(COLORS[self.type])

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.x, self.rect.y = self.x, self.y
        if not 0 <= self.rect.x <= 800 - PLAYERSIZE:
            self.dx *= -1
        if not 0 <= self.rect.y <= 800 - PLAYERSIZE:
            self.dy *= -1
        for hit in pygame.sprite.spritecollide(self, players, False):
            if (self.type, hit.type) in [("paper", "scissors"), ("scissors", "rock"), ("rock", "paper")]:
                totals[self.type] -= 1
                self.type = hit.type
                totals[self.type] += 1
                self.image.fill(COLORS[self.type])

all_sprites = pygame.sprite.LayeredUpdates()
players = pygame.sprite.Group()

def init_sim(population, speed):
    global totals
    totals = {"rock": 0, "paper": 0, "scissors": 0}
    for player in players:
        player.kill()
    for _ in range(population):
        Player(random.randint(0, 800 - PLAYERSIZE), random.randint(0, 800 - PLAYERSIZE), speed)

def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))

async def main():
    global totals
    totals = {"rock": 0, "paper": 0, "scissors": 0}
    percents = {"rock": 0, "paper": 0, "scissors": 0}
    running = True
    playing = True
    population = 50
    speed = 5
    clock = pygame.time.Clock()
    updated = 1
    current_pop = 50
    epsilon = 0.001
    init_sim(population, speed)
    while running:
        # print(totals, percents, sum(percents.values()))
        if playing:
            all_sprites.update()
        draw_screen(screen, population, speed, updated, percents, current_pop)
        keys = pygame.key.get_pressed()
        shifting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if shifting:
                        population = 50
                        speed = 5
                    playing = False
                    updated = 1
                    init_sim(population, speed)
                    current_pop = population
                elif event.key == pygame.K_SPACE:
                    playing = not playing
                elif event.key == pygame.K_LEFT:
                    updated = 0
                    if shifting:
                        population = max(0, population - 10)
                    else:
                        population = max(0, population - 1)
                elif event.key == pygame.K_RIGHT:
                    updated = 0
                    if shifting:
                        population = min(200, population + 10)
                    else:
                        population = min(200, population + 1)
                elif event.key == pygame.K_UP:
                    updated = 0
                    speed += 1
                elif event.key == pygame.K_DOWN:
                    updated = 0
                    speed = max(0, speed - 1)
        for key in percents.keys():
            disc = totals[key] - percents[key]
            if totals[key] == 0 and abs(disc) < epsilon:
                # print("resetting", disc, totals[key], percents[key])
                percents[key] = totals[key]
            elif totals[key] == current_pop and abs(disc) < epsilon:
                percents[key] = totals[key]
            else:
                percents[key] += (disc) / 10
            # if totals[key] == 0:
            #     percents[key] = 0
            # elif totals[key] == sum(totals.values()):
            #     percents[key] = totals[key]
            # else:
            #     disc = totals[key] - percents[key]
            #     percents[key] += (disc) / 10
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
