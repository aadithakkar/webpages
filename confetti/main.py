import pygame
import sys
import random
import time
import asyncio


pygame.init()
screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("Confetti Game")
clock = pygame.time.Clock()
score = 0
timer = time.time()


START_SQUARES = 35
WAIT_TIME = 3
mt = 30


def write(txt, pos, col, size):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    screen.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))


def add_sq():
    global squares
    squares.add(Square((random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)), random.randint(25, 575), random.randint(50, 575)))


def outfunc():
    global score
    score += 50
    add_sq()


class Square(pygame.sprite.Sprite):
    def __init__(self, c, x, y):
        self.spos = (x, y)
        self.stime = time.time()
        self.acc = -15
        self.inmotion = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(c)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        if self.inmotion:
            self.acc += 1
            self.rect.move_ip(0, self.acc)
            if self.rect.centery > 600:
                self.kill()

    def fall(self, mouse):
        if not self.inmotion and self.rect.centerx - 25 < mouse[0] < self.rect.centerx + 25 and self.rect.centery - 25 < mouse[1] < self.rect.centery + 25:
            outfunc()
            self.inmotion = 1


john = Square((100, 0, 0), 300, 300)
running = True
mode = 0
highest = 0


squares = pygame.sprite.Group()
for _ in range(START_SQUARES):
    add_sq()


async def main():
    global score, mt, timer, squares, mode, highest
    while True:
        screen.fill((255, 255, 255))
        if mode == 0:
            write(score, (300, 25), (0, 0, 0), 50)
            write(mt - round(time.time() - timer), (50, 25), (0, 0, 0), 50)
            squares.update()
            squares.draw(screen)
        else:
            write(score, (300, 300), (0, 0, 0), 70)
            write(f"High score: {highest}", (300, 450), (0, 0, 0), 40)
            write(WAIT_TIME - round(time.time() - timer), (50, 25), (0, 0, 0), 50)
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for sq in squares:
                    sq.fall(mouse)
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    mode = 0
                    for square in squares:
                        square.kill()
                    for _ in range(START_SQUARES):
                        add_sq()
                    score = 0
                    timer = time.time()
        if mode == 0:
            if time.time() - timer > mt:
                mode = 1
                for square in squares:
                    square.kill()
                timer = time.time()
                if score > highest:
                    highest = score
        else:
            if time.time() - timer > WAIT_TIME:
                mode = 0
                score = 0
                for _ in range(START_SQUARES):
                    add_sq()
                timer = time.time()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
