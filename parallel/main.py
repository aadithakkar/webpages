import pygame
import sys
import math
import time
import scene_library as sl
import asyncio

pygame.init()

screen = pygame.display.set_mode([800, 900])
pygame.display.set_caption("Parallel")


FPS = 60
TILESIZE = 40
PLAYER_SPEED = 5
GROUND_COL = (180, 230, 150)
BACKGROUND_COL = (100, 70, 40)
JUMP_HEIGHT = 10

GROUNDLAYER = 1
PLATELAYER = 2
BOULDERLAYER = 3
BLOCKLAYER = 4
ARROWLAYER = 5
TEXTLAYER = 6


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, ground, scenesprites
        self._layer = GROUNDLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill(BACKGROUND_COL if not (level == 15 and mode == 0) else GROUND_COL)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, scenesprites, specialblocks, water
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((0, 200, 200))
        self.rect = self.image.get_rect()
        self.image.set_alpha(125)
        self.rect.x = self.x
        self.rect.y = self.y
        self.name = "Water"
        self.desc = "Dihydrogen Monoxide."



class Boulder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, scenesprites, specialblocks, solid
        self._layer = BOULDERLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.pull = 0
        self.name = "Boulder"
        self.desc = "A solid block you can push around."

    def update(self):
        hittingwater = bool(pygame.sprite.spritecollide(self, water, False))
        if mode == 1:
            if not hittingwater:
                self.pull += 1 if gravity == 0 else -1
            else:
                self.pull = 2
            self.y_change += self.pull
            # pass
            # self.move()
            # self.rect.x += self.x_change
            # self.wall_collision("x")
            # self.rect.y += self.y_change
            # self.wall_collision("y")
        if self.canmove("y", self.y_change):
            self.rect.y += self.y_change
        elif hittingwater and self.canmove("y", 1):
            self.rect.y += 1
        else:
            self.pull = 0
        self.x_change = 0
        self.y_change = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] + keys[pygame.K_d] + keys[pygame.K_s] + keys[pygame.K_w]) == 1:
            if keys[pygame.K_a]:
                self.x_change -= PLAYER_SPEED
            if keys[pygame.K_d]:
                self.x_change += PLAYER_SPEED
            if keys[pygame.K_w]:
                self.y_change -= PLAYER_SPEED
            if keys[pygame.K_s]:
                self.y_change += PLAYER_SPEED

    def canmove(self, dir, steps):
        if paused:
            return 0
        if dir == "x":
            orr = self.rect.right
            orl = self.rect.left
            self.rect.x += steps
            hits = pygame.sprite.spritecollide(self, solid, False)
            hits += pygame.sprite.spritecollide(self, playergroup, False)
            self.rect.x -= steps
            if len(hits) <= 1:
                return steps
            hits.remove(self)
            #print(hits[0])
            overlap = self.rect.right - hits[0].rect.left if steps > 0 else hits[0].rect.right - self.rect.left
            return hits[0].rect.left - orr if steps > 0 else hits[0].rect.right - orl
            return steps - overlap if steps > 0 else steps + overlap
        elif dir == "y":
            self.rect.y += steps
            hits = pygame.sprite.spritecollide(self, solid, False)
            hits += pygame.sprite.spritecollide(self, playergroup, False)
            self.rect.y -= steps
            return len(hits) <= 1


class Clonepad(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specialblocks, scenesprites, clonepads
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((150, 250, 250))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.name = "Clone Pad"
        self.desc = "Stepping on these will create a Clone of you."

    def activate(self):
        if not clones:
            for pad in clonepads:
                if pad != self:
                    offset_x = pad.x - self.x
                    offset_y = pad.y - self.y
                    #print(offset_x, offset_y)
                    #print(player.rect.x + offset_x, player.rect.y + offset_y)
                    Clone(player.rect.x + offset_x, player.rect.y + offset_y)


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        if level == 5:
            self.groups = all_sprites, scenesprites, doors, specialblocks
        else:
            self.groups = all_sprites, scenesprites, solid, doors, specialblocks
        self._layer = BLOCKLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((100, 0, 0) if level != 14 else (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.name = "Locked Gate"
        self.desc = "Press all Pressure Plates to unlock this gate."


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specialblocks, scenesprites, lavas
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((255, 100, 0) if level != 14 else (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.name = "Lava"
        self.desc = "You and your clones die by touching this."


class Orb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specialblocks, scenesprites, orbs
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((0, 250, 250))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.name = "Jump Orb"
        self.desc = "Press 'W' while touching an Orb to jump midair."


class Nummod(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pass


class Plate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specialblocks, scenesprites, plates
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.is_pressed = 0
        self.name = "Pressure Plate"
        self.desc = "These activate if you (or Boulders) step on them."
        self.beenpressed = 0

    def all_pressed(self):
        # print("checking")
        for plate in plates:
            if not plate.is_pressed:
                return False
        return True

    def update(self):
        global lavas
        hits = pygame.sprite.spritecollide(self, playergroup, False) or pygame.sprite.spritecollide(self, solid, False) or pygame.sprite.spritecollide(self, clones, False) or pygame.sprite.spritecollide(self, skidders, False)
        if level != 12:
            if hits:
                self.image.fill((0, 200, 0))
                self.is_pressed = 1
            else:
                self.image.fill((200, 0, 0))
                self.is_pressed = 0
        else:
            if hits:
                self.beenpressed = min(self.beenpressed + 0.125, 40)
            else:
                self.beenpressed = max(self.beenpressed - 0.4, 0)
            if self.beenpressed > 0:
                self.is_pressed = 1
            else:
                self.is_pressed = 0
            self.image.fill((200, 0, 0))
            pygame.draw.rect(self.image, (0, 200, 0), pygame.Rect(0, 0, self.beenpressed, 40))
        if self.all_pressed():
            for plate in plates:
                #print("all clcikd!")
                plate.kill()
            for door in doors:
                door.kill()
            for risl in risinglavas:
                risl.speed = -6
                lavas.remove(risl)
            if scenenum not in opened:
                opened.append(scenenum)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, dest):
        self.groups = all_sprites, scenesprites, arrows
        self._layer = ARROWLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.dest = dest
        self.x = x + TILESIZE/2
        self.y = y + TILESIZE/2
        self.image = pygame.Surface([TILESIZE / 4, TILESIZE / 4])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        if dest[0] == self.x:
            self.angle = None
            self.delta_x = 0
            self.delta_y = 1
        else:
            self.angle = math.atan(abs(dest[1] - self.y) / abs(dest[0] - self.x))
            self.delta_x = math.cos(self.angle)
            self.delta_y = math.sin(self.angle)
        if dest[0] - self.x < 0:
            self.delta_x *= -1
        if dest[1] - self.y < 0:
            self.delta_y *= -1
        #print(self.angle, self.delta_x, self.delta_y)

    def update(self):
        self.x_change += self.delta_x
        self.y_change += self.delta_y
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        hits = pygame.sprite.spritecollide(self, solid, False)
        if hits:
            if type(hits[0]) == Wall:
                hits[0].health -= 1
            self.kill()
            #print(all_sprites)
        elif self.rect.x < 0 or self.rect.x > 800 or self.rect.y < 0 or self.rect.y > 800:
            self.kill()
            #print('died')


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specialblocks, scenesprites, solid
        self._layer = BLOCKLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((180, 180, 180))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.health = 4
        self.name = "Vulnerable Wall"
        self.desc = "Click/Scroll with your mouse on a Wall to damage/break it."

    def update(self):
        col = min([250 - self.health * 10, 255])
        self.image.fill((col, col, col))
        if self.health <= 0:
            self.kill()


class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specialblocks, scenesprites, keygroup
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((200, 200, 0) if level != 14 else(255, 100, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.name = "Key"
        self.desc = "This opens Locked Doors."


class Lock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specialblocks, scenesprites, solid, locks
        self._layer = BLOCKLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((100, 100, 100) if level != 14 else (100, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.name = "Locked Door"
        self.desc = "Get the Key to unlock this."


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, blocks, scenesprites, solid
        self._layer = BLOCKLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, scenesprites, portals, specialblocks
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((250, 0, 250))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.name = "Portal"
        self.desc = "Press [SPACE] while touching to enter/exit The Underground."


class Trampoline(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, scenesprites, trampolines, specialblocks
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((150, 0, 150) if level != 14 else (255, 100, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.name = "Trampoline"
        self.desc = "Touching these will shoot you upwards."


class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, scenesprites, checkpoints, specialblocks
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((0, 250, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.reached = 0
        self.name = "Checkpoint"
        self.desc = "When you die or reset, you reappear at your last checkpoint."

    def reach(self):
        global checkpoint, deaths
        self.reached = 1
        self.image.fill((0, 150, 0))
        checkpoint = (scenenum, self.x / TILESIZE, self.y / TILESIZE, deaths)
        #print(checkpoint)


class Text(pygame.sprite.Sprite):
    def __init__(self, txt, col):
        #print("tc")
        self.groups = all_sprites
        self._layer = TEXTLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font(None, 70)
        self.stime = time.time()
        self.image = self.font.render(txt, True, col)
        self.image.set_alpha(125)
        isize = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = 400 - isize[0] / 2
        self.rect.y = 700 - isize[1] / 2
        self.alpha = 255

    def update(self):
        time_passed = time.time() - self.stime
        if time_passed < 2:
            self.image.set_alpha(time_passed * 125)
        elif 4 < time_passed < 6:
            self.image.set_alpha(255 - (time_passed - 4) * 125)
        elif time_passed > 6:
            #print("endig")
            self.kill()


class Riser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specialblocks, scenesprites, risers
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((200, 250, 200))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.name = "Lava Trap"
        self.desc = "This activates a rising lava trap when touched."


class Faller(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specialblocks, scenesprites, fallers
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((250, 200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.name = "Lava Drainer"
        self.desc = "This drains the rising lava trap."


class Clone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #print(x, y, "i")
        self._layer = ARROWLAYER
        self.groups = all_sprites, clones, scenesprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((120, 120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.first = 1

    def move(self, xc, yc):
        if self.first:
            self.first = 0
        else:
            hits = pygame.sprite.spritecollide(self, solid, False)
            if hits:
                return False
            self.rect.x += xc
            hits = pygame.sprite.spritecollide(self, solid, False)
            if hits:
                moveable = 1
                for sprite in hits:
                    if type(sprite) == Boulder:
                        if sprite.canmove('x', xc):
                            sprite.rect.x += xc
                        else:
                            moveable = 0
                    else:
                        moveable = 0
                if not moveable:
                    self.rect.x -= xc
            self.rect.y += yc
            hits = pygame.sprite.spritecollide(self, solid, False)
            if hits:
                moveable = 1
                for sprite in hits:
                    if type(sprite) == Boulder:
                        if sprite.canmove('y', yc):
                            sprite.rect.y += yc
                        else:
                            top = sprite.rect.top
                            bottom = sprite.rect.bottom
                            moveable = 0
                    else:
                        top = sprite.rect.top
                        bottom = sprite.rect.bottom
                        moveable = 0
                if not moveable:
                    if yc > 0:
                        self.rect.y = top - TILESIZE
                    else:
                        self.rect.y = bottom
        hits = pygame.sprite.spritecollide(self, lavas, False)
        if hits or (not 0 < self.rect.centerx < 800) or (not 0 < self.rect.centery < 800):
            self.kill()


class Skidder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = BOULDERLAYER
        self.groups = all_sprites, skidders, scenesprites, lavas, specialblocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((125, 0, 250))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.pull = 0
        self.dir = 1
        self.speed = 5
        self.name = "Skidder"
        self.desc = "Bouncing creatures that kill you if they hit you."
        self.isreal = 1

    def update(self):
        if self.isreal:
            self.rect.x += self.dir * self.speed
            hits = pygame.sprite.spritecollide(self, solid, False)
            if hits:
                if self.dir == 1:
                    self.rect.x = hits[0].rect.left - TILESIZE
                else:
                    self.rect.x = hits[0].rect.right
                self.dir *= -1
            hits = pygame.sprite.spritecollide(self, solid, False)
            if hits:
                # self.kill()
                #print("dh")
                self.isreal = 0
                self.pull = -15
        else:
            self.rect.y += self.pull
            self.pull += 1
        if not (0 < self.rect.centerx < 800 and 0 < self.rect.centery < 800):
            #print('deids')
            self.kill()


class RisingLava(pygame.sprite.Sprite):
    def __init__(self, x, y, s):
        #print("iexist")
        self.groups = all_sprites, scenesprites, lavas, risinglavas
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        if len(risinglavas) > 1:
            self.kill()
            #print("nm")
            return None
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 2.25
        self.image = pygame.Surface([800, 800])
        self.image.fill((255, 100, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.skip = 0
        self.ypos = self.rect.y
        self.stime = time.time()

    def update(self):
        elapsed = time.time() - self.stime
        self.image.fill((250, 225 - abs((elapsed % 2) - 1) * 100 , 0))
        self.ypos -= self.speed
        self.rect.y = self.ypos
        if self.rect.y > 800:
            self.kill()
            #print("diedl")
        # self.skip = 1 - self.skip


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, playergroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0
        self.pull = 0
        self.mobile = 1
        self.falling = 1
        self.transitioning = 0
        self.l9 = 0
        self.positions = []
        self.revi = -1
        self.rewind_start = 0
        self.wpw = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x_change -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x_change += self.speed
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (mode == 0 or self.hittingwater):
            if self.hittingwater:
                self.pull -= 0.75
                if self.pull < -4:
                    self.pull = -4
            else:
                self.y_change -= self.speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and mode == 0 and self.rect.bottom > 0:
            self.y_change += self.speed

    def wall_collision(self, dir):
        hits = pygame.sprite.spritecollide(self, solid, False)
        for sprite in hits:
            if dir == "x":
                if type(sprite) == Boulder:
                    # if self.x_change < 0:
                    #     self.rect.left = sprite.rect.right - 2
                    # else:
                    #     self.rect.right = sprite.rect.left + 2
                    steps = self.rect.left - sprite.rect.right if self.x_change < 0 else self.rect.right - sprite.rect.left
                    can_move = sprite.canmove(dir, steps)
                    if can_move:
                        sprite.rect.x += can_move
                        if self.x_change > 0:
                            self.rect.right = sprite.rect.left
                        elif self.x_change < 0:
                            self.rect.left = sprite.rect.right
                    else:
                        if self.x_change > 0:
                            self.rect.right = sprite.rect.left
                        elif self.x_change < 0:
                            self.rect.left = sprite.rect.right
                else:
                    if self.x_change > 0:
                        self.rect.x = sprite.rect.left - self.rect.width
                    elif self.x_change < 0:
                        self.rect.x = sprite.rect.right
            elif dir == "y":
                if mode == 1:
                    self.pull = 0
                    self.falling = 0
                if type(sprite) == Boulder:
                    steps = self.rect.top - sprite.rect.bottom if self.y_change < 0 else self.rect.bottom - sprite.rect.top
                    can_move = sprite.canmove(dir, steps)
                    if can_move:
                        sprite.rect.y += steps
                    else:
                        if self.y_change > 0:
                            self.rect.bottom = sprite.rect.top
                        elif self.y_change < 0:
                            self.rect.top = sprite.rect.bottom
                else:
                    if self.y_change > 0:
                        self.rect.y = sprite.rect.top - self.rect.height
                    elif self.y_change < 0:
                        self.rect.y = sprite.rect.bottom
        hits = pygame.sprite.spritecollide(self, lavas, False)
        if hits:
            if not (type(hits[0]) == Skidder and not hits[0].isreal):
                if not self.transitioning:
                    #print("rst")
                    reset()
        hits = pygame.sprite.spritecollide(self, keygroup, False)
        if hits and not self.transitioning:
            for key in keygroup:
                key.kill()
            for lock in locks:
                lock.kill()
            unlocked.append(scenenum)
            #print(unlocked)
        hits = pygame.sprite.spritecollide(self, risers, False)
        if hits:
            hits[0].kill()
            #print("RISSERS")
            RisingLava(0, 20, scenenum)
        hits = pygame.sprite.spritecollide(self, fallers, False)
        if hits:
            hits[0].kill()
            for risinglava in risinglavas:
                risinglava.speed = -6
                risinglava.dubspeed = -12
        hits = pygame.sprite.spritecollide(self, checkpoints, False)
        if hits:
            if not hits[0].reached:
                hits[0].reach()
        hits = pygame.sprite.spritecollide(self, trampolines, False)
        if hits and mode:
            #print("tramp")
            self.pull = -14 if level != 14 else -18
        hits = pygame.sprite.spritecollide(self, clonepads, False)
        if hits:
            hits[0].activate()

    def update(self):
        global scenenum, level, opened, gamestart, total_time, gravity
        if self.l9:
            alpha = max(0, 250 - 125 * (time.time() - self.l9))
            self.image.set_alpha(alpha)
        hits = pygame.sprite.spritecollide(self, solid, False)
        if hits:
            #print("EPR")
            if level == 16:
                hits[0].kill()
            else:
                self.mobile = 0
                if not self.transitioning:
                    reset()
        self.falling = 1
        original_pos = (self.rect.x, self.rect.y)
        self.hittingwater = bool(pygame.sprite.spritecollide(self, water, False))
        wfs = 3
        self.speed = PLAYER_SPEED if level != 17 else 12
        if self.mobile:
            if self.hittingwater:
                self.speed = 3
            self.move()
        if mode == 1:
            if self.hittingwater:
                if self.pull >= wfs:
                    self.pull -= 0.5
                    if self.pull < wfs:
                        self.pull = wfs
                elif self.pull < -wfs:
                    self.pull += 0.6
                    if self.pull > -wfs:
                        self.pull = -wfs
                else:
                    self.pull += 0.25
            else:
                self.pull += 0.5 if gravity == 0 else -0.5
            # print(self.pull)
            self.y_change += self.pull
            if pygame.key.get_pressed()[pygame.K_w]:
                pass
                #print("pw")
                #self.pull = 5
            #print(self.pull)
        kp = 0
        keys = pygame.key.get_pressed()
        if level == 19 and (keys[pygame.K_DELETE] or keys[pygame.K_BACKSPACE]):
            kp = 1
            if len(self.positions) >= 1:
                if not self.rewind_start:
                    self.rewind_start = time.time()
                lastpos = self.positions[-1]
                self.x_change = lastpos[0] - self.rect.x
                self.y_change = lastpos[1] - self.rect.y
                self.positions = self.positions[:-1]
                self.pull = 0
            else:
                if self.rewind_start:
                    gamestart = time.time() - ((player.rewind_start - gamestart) - (time.time() - player.rewind_start))
                    #print(gamestart, time.time())
                    self.rewind_start = 0
        else:
            if self.rewind_start:
                gamestart = time.time() - ((player.rewind_start - gamestart) - (time.time() - player.rewind_start))
                self.rewind_start = 0
        if level == 20:
            mouse = pygame.mouse.get_pos()
            totalx = mouse[0] - self.rect.centerx
            totaly = mouse[1] - self.rect.centery
            dist = (totalx ** 2 + totaly ** 2) ** 0.5
            if dist <= 30:
                self.x_change = totalx
                self.y_change = totaly
            else:
                scale = 30 / (totalx ** 2 + totaly ** 2) ** 0.5
                self.x_change = scale * totalx
                self.y_change = scale * totaly
        self.rect.x += self.x_change
        #print(self.x_change)
        self.wall_collision("x")
        self.rect.y += self.y_change
        self.wall_collision("y")
        
        #print(self.falling)
        if level == 19:
            if not kp:
                if len(self.positions) > 500:
                    self.positions = self.positions[1:] + [(self.rect.x, self.rect.y)]
                else:
                    self.positions.append((self.rect.x, self.rect.y))
            # print(self.positions)

        # for spr in all_sprites:
        #     spr.rect.x -= self.x_change
        if level == 20 and self.rect.centerx >= 795:
            level = 21
            self.mobile = False
            total_time = time.time() - gamestart
            EndFade(1)
            #print('9')
        if self.rect.centerx > 800:
            self.rect.centerx = 0
            level += 1
            opened = []
            initialize_scene()
        elif self.rect.centerx < 0:
            if level == 11:
                self.rect.centerx = 800
            else:
                self.rect.centerx = 0
            # self.rect.centerx = 800
            # if scenenum == 199:
            #     scenenum = 600
            # else:
            #     scenenum -= 1
            # initialize_scene()
        elif self.rect.centery > 800:
            self.rect.centery = 0
            scenenum -= 100
            initialize_scene()
        elif self.rect.centery < 0 and scenenum != 900:
            self.rect.centery = 800
            scenenum += 100
            initialize_scene()

        for clone in clones:
            clone.move(self.rect.x - original_pos[0], self.rect.y - original_pos[1])

        self.x_change = 0
        self.y_change = 0
        if self.rect.bottom < 0 and self.mobile:
            self.mobile = 0
            EndFade(deaths)
        # keys = pygame.key.get_pressed()
        # print(keys[pygame.K_w] or keys[pygame.K_UP], mode == 1, self.mobile, not self.hittingwater)
        # iwpw = self.wpw
        # self.wpw = 0
        # if (keys[pygame.K_w] or keys[pygame.K_UP]) and mode == 1 and self.mobile and not self.hittingwater:
        #     if not iwpw:
        #         if level != 2:
        #             # player.pull = -JUMP_HEIGHT
        #             #print("a")
        #             if (not self.falling) or level == 3:
        #                 #print("b")
        #                 self.pull = -JUMP_HEIGHT
        #             elif (pygame.sprite.spritecollide(self, orbs, False)):
        #                 self.pull = -13
        #         else:
        #             gravity = 1 - gravity
        #     self.wpw = 1
        # elif False:
        #     self.wpw = 0


class EndFade(pygame.sprite.Sprite):
    def __init__(self, deaths):
        #print("efc")
        self.groups = fades
        self._layer = TEXTLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.stime = time.time()
        self.image = pygame.Surface((800, 800))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.deaths = deaths
        self.death_amount = 0
        self.change_rate = max(8, int(deaths / 3))
        self.has_changed = 0
    
    def update(self):
        self.image.fill((0, 0, 0))
        elapsed = time.time() - self.stime
        if elapsed < 2:
            self.image.set_alpha((elapsed) * 128)
        elif 3 < elapsed:
            self.image.set_alpha(255)
            write("The End", (400, 400), (255, 255, 255), 70, self.image)
        if 4 < elapsed:
            # print(elapsed, int(elapsed - 5 * 100))
            if skips == 1:
                write("By the way, you could've pressed '6' for a free skip :)", (400, 600), (255, 255, 255), 40, self.image)
        if 9 < elapsed < 11:
            if not self.has_changed:
                menu()
                self.has_changed = 1
            self.image.set_alpha(250 - (elapsed - 9) * 125)
        if 11 < elapsed:
            #print("dddd", all_sprites)
            self.kill()


class Fade(pygame.sprite.Sprite):
    def __init__(self):
        #print("tc")
        self.groups = fades
        self._layer = TEXTLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.stime = time.time()
        self.image = pygame.Surface((800, 800))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.has_changed = 0

    def update(self):
        global in_game
        time_passed = time.time() - self.stime
        if time_passed < 1:
            self.image.set_alpha(time_passed * 250)
        elif not self.has_changed:
            global scenenum, mode
            #print("updating!!")
            scenenum = checkpoint[0]
            if scenenum >= 9800:
                mode = 1
            else:
                mode = 0
            player.rect.x = checkpoint[1] * TILESIZE
            player.rect.y = checkpoint[2] * TILESIZE
            player.transitioning = 0
            player.mobile = 1
            in_game = 1
            initialize_scene()
            self.has_changed = 1
        elif time_passed < 2:
            #print("i")
            self.image.set_alpha(250 - (time_passed - 1) * 250)
        else:
            #print("endigg")
            self.kill()


class Helpbox(pygame.sprite.Sprite):
    def __init__(self, name, desc):
        #print("hc")
        self.groups = helpboxes
        self._layer = TEXTLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.stime = time.time()
        self.image = pygame.Surface((600, 150))
        self.image.fill((100, 100, 100))
        self.image.set_alpha(230)
        write(name, (300, 30), (255, 255, 255), 50, self.image)
        write(desc, (300, 100), (255, 255, 255), 30, self.image)
        # self.font = pygame.font.Font(None, 70)
        # self.stime = time.time()
        # self.image = self.font.render(name, True, col)
        # self.image.set_alpha(125)
        # isize = self.image.get_size()
        # self.rect = self.image.get_rect()
        # self.rect.x = 400 - isize[0] / 2
        # self.rect.y = 700 - isize[1] / 2
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 550

    def update(self):
        if time.time() - self.stime > 3:
            self.kill()


class Counter(pygame.sprite.Sprite):
    def __init__(self):
        self.total = 0
        #print("COUNTERMADE")
        self.groups = all_sprites, countergroup
        self._layer = TEXTLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE * 2, TILESIZE * 2))
        self.image.fill((75, 75, 75))
        pygame.draw.rect(self.image, (100, 100, 100), pygame.Rect(8, 8, TILESIZE * 2 - 16, TILESIZE * 2 - 16))
        write(self.total, (TILESIZE, TILESIZE), (0, 0, 0), 50, self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def alterto(self, newtotal):
        if not abs(newtotal - round(newtotal)) < 0.01:
            return None
        newtotal = int(round(newtotal))
        if not 0 <= newtotal <= 999:
            return None
        self.total = newtotal
        self.image.fill((75, 75, 75))
        pygame.draw.rect(self.image, (100, 100, 100), pygame.Rect(8, 8, TILESIZE * 2 - 16, TILESIZE * 2 - 16))
        write(self.total, (TILESIZE, TILESIZE), (0, 0, 0), 50, self.image)


class Modtile(pygame.sprite.Sprite):
    def __init__(self, x, y, label, oper, desc):
        self.total = 0
        #print("MO")
        self.groups = all_sprites, scenesprites, specialblocks, modtiles
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.label = label
        self.oper = oper
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((250, 250, 200))
        self.tsize = 40 if len(self.label) < 4 else 30
        if self.label == "+%3":
            self.tsize = 30
        #write(self.label, (TILESIZE / 2, TILESIZE / 2), (0, 0, 0), self.tsize, self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.objentrance = (0, 0)
        self.hitting = 0
        self.lasthitter = None
        self.name = f"Number Laser ({label})"
        self.desc = desc
        self.brightness = 250

    def update(self):
        hits = pygame.sprite.spritecollide(self, playergroup, False) + pygame.sprite.spritecollide(self, skidders, False)
        if hits:
            if not self.hitting:
                self.hitting = 1
                self.lasthitter = hits[0]
                self.objentrance = self.colliderpos(hits[0])
                #print(self.objentrance)
        elif self.hitting:
            self.hitting = 0
            if self.colliderpos(self.lasthitter) != self.objentrance:
                #print("OPERATION!")
                global counter
                counter.alterto(self.oper(counter.total))
                self.brightness = 200
            self.lasthitter = None
        if self.brightness < 250:
            # print("rstii")
            b = self.brightness
            self.image.fill((b, b, b - 50))
            write(self.label, (TILESIZE / 2, TILESIZE / 2), (0, 0, 0), self.tsize, self.image)
            self.brightness += 1

    def colliderpos(self, hit):
        if hit.rect.x > self.rect.x:
            return (1, 0)
        if hit.rect.x < self.rect.x:
            return (-1, 0)
        if hit.rect.y > self.rect.y:
            return (0, 1)
        if hit.rect.y < self.rect.y:
            return (0, -1)


class Numblock(pygame.sprite.Sprite):
    def __init__(self, x, y, targ):
        #print("MO")
        self.groups = all_sprites, scenesprites, specialblocks, numblocks, solid
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = targ
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((200, 200, 100))
        pygame.draw.rect(self.image, (250, 250, 150), pygame.Rect(3, 3, TILESIZE - 6, TILESIZE - 6))
        write(self.target, (TILESIZE / 2, TILESIZE / 2), (0, 0, 0), 40 if targ < 100 else 35, self.image)
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.name = f"Number Block ({self.target})"
        self.desc = f"Block that's solid unless your number total is {self.target}."
        self.brightness = 250
        self.issolid = 1
        self.s = scenenum

    def update(self):
        if self.s != scenenum:
            #print("retis")
            self.kill()
            return None
        # print(self)
        global solid
        if self.issolid:
            if counter.total == self.target:
                self.issolid = 0
                self.image.set_alpha(125)
                solid.remove(self)
                #print("ch", solid)
        else:
            if counter.total != self.target:
                self.issolid = 1
                self.image.set_alpha(255)
                solid.add(self)
                #print('b', solid)


running = True
clock = pygame.time.Clock()
mode = 1
scene = ""
checkpoint = (0, 9.5, 12.5)
checkpoint = (10399, 5, 10)
checkpoint = (0, 2, 17)
checkpoint = (10800, 11, 16)
checkpoint = (800, 1, 2, 4)
checkpoint_code = "0"
# 10399
scenenum = 10596
scenenum = 10307
deaths = checkpoint[3]
unlocked = []
opened = []
messaged = []
numreached = 0
skips = 1
all_sprites = pygame.sprite.LayeredUpdates()
blocks = pygame.sprite.Group()
water = pygame.sprite.Group()
skidders = pygame.sprite.Group()
risinglavas = pygame.sprite.Group()
risers = pygame.sprite.Group()
fallers = pygame.sprite.Group()
helpboxes = pygame.sprite.Group()
clones = pygame.sprite.Group()
clonepads = pygame.sprite.Group()
lavas = pygame.sprite.Group()
ground = pygame.sprite.Group()
playergroup = pygame.sprite.Group()
scenesprites = pygame.sprite.Group()
specialblocks = pygame.sprite.Group()
solid = pygame.sprite.Group()
locks = pygame.sprite.Group()
keygroup = pygame.sprite.Group()
plates = pygame.sprite.Group()
doors = pygame.sprite.Group()
arrows = pygame.sprite.Group()
portals = pygame.sprite.Group()
fades = pygame.sprite.Group()
checkpoints = pygame.sprite.Group()
trampolines = pygame.sprite.Group()
orbs = pygame.sprite.Group()
countergroup = pygame.sprite.Group()
modtiles = pygame.sprite.Group()
numblocks = pygame.sprite.Group()
player = Player(10, 10)
total_time = 0
in_game = 0
controls = 0
level = 1
l10 = 0
paused = 0
begun = 0
hints = [
    "",
    "The First Level",
    "Gravity Falls",
    "Flappy Bird?",
    "Before You Leap",
    "The Grand Illusion",
    "Danger Zone",
    "Through the Portal",
    "Timeless",
    "Curse of Vanishing",
    "Curse of Everything Vanishing",
    "Back and There Again",
    "Recharged",
    "A Vulnerable World",
    "Disguised",
    "A New World",
    "Creative Mode",
    "Think Fast",
    "All Under Control",
    "kcabyalP",
    "Leader and Follower",
    "The End"
]
gravity = 0
blockplaced = 0


def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))


counter = None
numreached = 1


def write_text():
    global numreached, counter
    if scenenum in messaged:
        return False
    messaged.append(scenenum)
    if scenenum == 10397:
        Text("The Underground", (255, 255, 255))
    elif scenenum == 99:
        Text("The Forgotten Plains", (255, 255, 255))
    elif scenenum == 101:
        Text("The Fractal Field", (255, 255, 255))
    elif scenenum == 201:
        Text("Danger Zone", (100, 100, 100))
    elif scenenum == 199:
        Text("Numberland", (255, 255, 255))
        if not numreached:
            counter = Counter()
            numreached = 1
    elif scenenum == 10596:
        Text("The Abandoned Reefs", (255, 255, 255))
    elif scenenum == 10698:
        Text("The Trial of Intellect", (200, 150, 0))
    elif scenenum == 10800:
        Text("The Penultimate Tomb", (255, 255, 255))
    else:
        messaged.remove(scenenum)


def reset():
    global in_game, scenenum, opened, unlocked
    # deaths += 1
    # print(deaths)
    # Fade()
    player.positions = []
    opened = []
    unlocked = []
    scenenum = checkpoint[0]
    player.rect.x = checkpoint[1] * TILESIZE
    player.rect.y = checkpoint[2] * TILESIZE
    player.transitioning = 0
    player.mobile = 1
    #print(player.mobile)
    in_game = 1
    initialize_scene()
    # global scenenum
    # scenenum = checkpoint[0]
    # player.rect.x = checkpoint[1] * TILESIZE
    # player.rect.y = checkpoint[2] * TILESIZE
    # initialize_scene()


def initialize_scene():
    global scene, counter, gravity, scenenum, blockplaced, opened, mode, paused, gamestart, l10
    blockplaced = 0
    opened = []
    # for groundblock in ground:
    #     groundblock.kill()
    # for block in blocks:
    #     block.kill()
    if scenenum != 15:
        scenenum = 10000
        if 10000 + level in sl.scenes.keys():
            scenenum = 10000 + level
        mode = 1
    if level == 7:
        mode = 0
    if level == 9:
        player.l9 = time.time()
        if paused:
            gamestart = time.time() - paused
            paused = 0
    if level == 10:
        player.l9 = 0
        player.image.set_alpha(255)
        l10 = time.time()
    if level == 11:
        l10 = 0
    if level == 17:
        player.speed = 10
    gravity = 0
    if counter is not None:
        counter.kill()
    for sprite in scenesprites:
        sprite.kill()
    if level == 6 and not risinglavas:
        #print("l6")
        RisingLava(0, 20, level)
    #print(numblocks)
    scene = sl.scenes[scenenum]
    for i in range(20):
        for j in range(20):
            Ground(j, i)
            element = i * 20 + j
            tile = scene[element]
            if tile == "1":
                Block(j, i)
            elif tile == "2":
                if scenenum not in opened:
                    Plate(j, i)
            elif tile == "3":
                Checkpoint(j, i)
            elif tile == "4":
                Wall(j, i)
            elif tile == "5":
                Boulder(j, i)
            elif tile == "6":
                if scenenum not in unlocked:
                    Lock(j, i)
            elif tile == "7":
                if scenenum not in unlocked:
                    Key(j, i)
            elif tile == "8":
                Portal(j, i)
            elif tile == "9":
                Trampoline(j, i)
            elif tile == "C":
                if scenenum not in opened:
                    Door(j, i)
            elif tile == "A":
                Lava(j, i)
            elif tile == "B":
                Orb(j, i)
            elif tile == "D":
                Clonepad(j, i)
            elif tile == "E":
                Riser(j, i)
            elif tile == "F":
                Faller(j, i)
            elif tile == "G":
                Skidder(j, i)
            elif tile == "J":
                Water(j, i)
    write_text()
    #print(numblocks)
    #print(all_sprites)
    #print("s", solid)


def draw_board():
    global wasjumping
    screen.fill((200, 200, 200))
    # ground.draw(screen)
    # blocks.draw(screen)
    # specialblocks.draw(screen)
    # playergroup.draw(screen)
    # print(all_sprites)
    if in_game:
        all_sprites.draw(screen)
        playergroup.draw(screen)
        helpboxes.draw(screen)
        pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(0, 800, 800, 100))
        if level <= 20:
            write(f"Level {level}", (400, 830), (0, 0, 0), 50, screen)
            write(hints[level], (400, 870), (0, 0, 0), 30, screen)
        if paused:
            timeplaying = paused
        else:
            if player.rewind_start:
                timeplaying = (player.rewind_start - gamestart) - (time.time() - player.rewind_start)
            else:
                if level == 21:
                    timeplaying = total_time
                else:
                    timeplaying = time.time() - gamestart
        mins = timeplaying // 60
        secs = int(((timeplaying % 60) // 1))
        centis = int((timeplaying % 1) // 0.01)
        if centis < 10:
            centis = f"0{centis}"
        if secs < 10:
            secs = f"0{secs}"
        write(f"{int(mins)}:{secs}:{centis}", (600, 850) if level <= 20 else (400, 850), (0, 0, 0) if not player.rewind_start else (0, 150, 250), 40, screen)
        if level == 8:
            if paused:
                write("RESUME (P)", (600, 875), (0, 0, 0), 30, screen)
            else:
                write("PAUSE (P)", (600, 875), (0, 0, 0), 30, screen)
        keys = pygame.key.get_pressed()
        if level == 19 and not (keys[pygame.K_DELETE] or keys[pygame.K_BACKSPACE]):
            write("REWIND (DEL)", (600, 875), (0, 0, 0), 30, screen)
    else:
        if controls == 0:
            mouse = pygame.mouse.get_pos()
            write("Parallel", (400, 180), (0, 0, 0), 70, screen)
            pygame.draw.rect(screen, (100, 100, 100) if 275 < mouse[0] < 525 and 320 < mouse[1] < 400 else (120, 120, 120), pygame.Rect(275, 320, 250, 80))
            write("PLAY", (400, 360), (0, 0, 0), 40, screen)
            pygame.draw.rect(screen, (100, 100, 100) if 275 < mouse[0] < 525 and 440 < mouse[1] < 520 else (120, 120, 120), pygame.Rect(275, 440, 250, 80))
            write("CONTROLS", (400, 480), (0, 0, 0), 40, screen)
            # write(f"Checkpoint code: {checkpoint_code}", (400, 650), (0, 0, 0), 40, screen)
        else:
            write("WASD / Arrow Keys  -  Move Player", (400, 100), (0, 0, 0), 45, screen)
            write("Click / Scroll  -  Shoot Arrow", (400, 200), (0, 0, 0), 45, screen)
            write("SHIFT + Click  -  Block Information", (400, 300), (0, 0, 0), 45, screen)
            write("R  -  Reset From Checkpoint (Lose All Unlocks)", (400, 400), (0, 0, 0), 45, screen)
            if level == 18:
                write("I  -  Skip Level 18", (400, 500), (0, 0, 0), 45, screen)
            else:
                write("CTRL + SHIFT + R - Reset Game", (400, 500), (0, 0, 0), 45, screen)
            write("SPACE  -  Enter Portal", (400, 600), (0, 0, 0), 45, screen)
            write("ESC  -  Main Menu", (400, 700), (0, 0, 0), 45, screen)
    fades.draw(screen)
    if jumping:
        # pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(50, 0, 100, 50))
        if not wasjumping and not player.falling and not player.hittingwater and not level == 2:
            player.pull = -JUMP_HEIGHT
    if jumping:
        wasjumping = True
    else:
        wasjumping = False


def interpret(code):
    #print(all_sprites)
    if code == "0":
        return (0, 9.5, 12.5, 0)
    split = code.split(".")
    if len(split) != 4:
        return (0, 9.5, 12.5, 0)
    scenekey = int(split[0])
    pixel = int(split[2]) * 20 + int(split[1])
    if not (scenekey in sl.scenes.keys() and 0 <= pixel <= 399):
        return (0, 9.5, 12.5, 0)
    if sl.scenes[scenekey][pixel] != "3":
        return (0, 9.5, 12.5, 0)
    #print([int(split[i]) for i in range(4)])
    return [int(split[i]) for i in range(4)]


def encode(code):
    if code == (0, 9.5, 12.5, 0):
        return "0"
    #print(checkpoint)
    return f"{checkpoint[0]}.{int(checkpoint[1])}.{int(checkpoint[2])}.{checkpoint[3]}"


def get_clicked(mx, my):
    for sprite in specialblocks:
        if sprite.rect.left < mx < sprite.rect.right and sprite.rect.top < my < sprite.rect.bottom:
            return sprite
    return None


def menu():
    global unlocked, opened, checkpoint_code, in_game
    for sprite in all_sprites:
        if not isinstance(sprite, Player):
            sprite.kill()
    unlocked = []
    opened = []
    checkpoint_code = encode(checkpoint)
    in_game = 0


# initialize_scene()
# GAME LOOP
async def main():
    global deaths, checkpoint, checkpoint_code, controls, in_game, unlocked, opened, mode, scenenum, begun, paused, level, gravity, skips, gamestart, blockplaced, jumping, wasjumping, total_time, l10
    jumping = False
    wasjumping = False
    while running:
        keys = pygame.key.get_pressed()
        if jumping == False and (keys[pygame.K_w] or keys[pygame.K_UP]):
            jumping = True
            if level != 2:
                if (not player.falling) or level == 3:
                    player.pull = -JUMP_HEIGHT
                elif (pygame.sprite.spritecollide(player, orbs, False)):
                    player.pull = -13
            else:
                gravity = 1 - gravity
        elif not (keys[pygame.K_w] or keys[pygame.K_UP]):
            jumping = False
        if in_game:
            all_sprites.update()
            helpboxes.update()
        fades.update()
        draw_board()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if in_game:
                    if mouse[1] > 800:
                        if level == 8:
                            if not paused:
                                paused = time.time() - gamestart
                            else:
                                gamestart = time.time() - paused
                                paused = 0
                    else:
                        pressed = pygame.key.get_pressed()
                        if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                            spr = get_clicked(mouse[0], mouse[1])
                            if spr is not None:
                                Helpbox(spr.name, spr.desc)
                        else:
                            if level == 16:
                                valid = 1
                                targetx = mouse[0] // TILESIZE
                                targety = mouse[1] // TILESIZE
                                for py in (player.rect.bottom, player.rect.top):
                                    for px in (player.rect.left, player.rect.right):
                                        pdx = px // TILESIZE
                                        pdy = py // TILESIZE
                                        #print(pdx, pdy)
                                        if (targetx, targety) == (pdx, pdy):
                                            valid = 0
                                if True or valid == 1:
                                    targetnum = targety * 20 + targetx
                                    if scene[targetnum] == "0":
                                        #print("Placing!")
                                        Block(targetx, targety)
                            else:
                                Arrow(player.rect.x, player.rect.y, mouse)
                            #print(13)
                else:
                    if controls == 0:
                        if 630 < mouse[1] < 670:
                            checkpoint_code = ""
                        elif 320 < mouse[1] < 400:
                            checkpoint = interpret(checkpoint_code)
                            checkpoint = (10000, 1, 15, 0)
                            scenenum = checkpoint[0]
                            deaths = checkpoint[3] - 1
                            initialize_scene()
                            reset()
                            if not begun:
                                gamestart = time.time()
                                begun = 1
                        elif 440 < mouse[1] < 520:
                            controls = 1
                    else:
                        controls = 0
            elif event.type == pygame.KEYDOWN:
                if in_game:
                    if False and (event.key == pygame.K_w or event.key == pygame.K_UP) and mode == 1 and player.mobile and not player.hittingwater:
                        if level != 2:
                            # player.pull = -JUMP_HEIGHT
                            #print("a")
                            if (not player.falling) or level == 3:
                                #print("b")
                                player.pull = -JUMP_HEIGHT
                            elif (pygame.sprite.spritecollide(player, orbs, False)):
                                player.pull = -13
                        else:
                            gravity = 1 - gravity
                    elif event.key == pygame.K_q:
                        checkstr = encode(checkpoint)
                        Text(checkstr, (255, 255, 255))
                    elif event.key == pygame.K_SPACE:
                        for clone in clones:
                            clone.kill()
                        hits = pygame.sprite.spritecollide(player, portals, False)
                        if hits and not player.transitioning:
                            #print("changing")
                            player.pull = 0
                            if mode == 0:
                                mode = 1
                                if scenenum == 300:
                                    scenenum = 10800
                                else:
                                    scenenum += 10000
                            elif mode == 1:
                                mode = 0
                                if scenenum == 10895:
                                    scenenum = 300
                                else:
                                    scenenum -= 10000
                            initialize_scene()
                    elif event.key == pygame.K_r:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL]:
                            level = 1
                            gamestart = time.time()
                            skips = 1
                            l10 = 0
                            paused = 0
                            total_time = 0
                            player.l9 = 0
                            player.image.set_alpha(255)
                            gravity = 0
                            blockplaced = 0
                            player.positions = []
                            player.revi = -1
                            player.rewind_start = 0
                            player.wpw = 0
                        unlocked = []
                        opened = []
                        reset()
                    elif event.key == pygame.K_6 and skips > 0 and level != 20:
                        level += 1
                        unlocked = []
                        opened = []
                        skips -= 1
                        reset()
                    elif event.key == pygame.K_ESCAPE:
                        menu()
                    elif event.key == pygame.K_p:
                        if level == 8:
                            if not paused:
                                paused = time.time() - gamestart
                            else:
                                gamestart = time.time() - paused
                                paused = 0
                    elif event.key == pygame.K_i and level == 18:
                        level += 1
                        opened = []
                        initialize_scene()
                        reset()
                else:
                    if event.unicode in "1234567890." and event.unicode != "":
                        if checkpoint_code == "0":
                            checkpoint_code = ""
                        checkpoint_code += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        if len(checkpoint_code) > 0:
                            checkpoint_code = checkpoint_code[:-1]
        if in_game and level == 4 and blockplaced == 0 and player.rect.centerx > 300:
            #print("PLACING")
            #print(all_sprites)
            newblock = Block(10, 12)
            blockplaced = time.time()
        if in_game and level == 4 and blockplaced > 0 and time.time() - blockplaced > 3:
            #print("KILLINGBLOCK")
            newblock.kill()
            blockplaced = -1
        if l10:
            alpha = max(0, 250 - 250 * (time.time() - l10))
            for spr in scenesprites:
                if not isinstance(spr, Ground) and not isinstance(spr, Plate):
                    spr.image.set_alpha(alpha)
        clock.tick(FPS)
        await asyncio.sleep(0)

asyncio.run(main())
