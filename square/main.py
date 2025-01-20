import pygame
import sys
import math
import time
import scene_library as sl
import asyncio

pygame.init()

screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("The Little Square")


FPS = 60
TILESIZE = 40
PLAYER_SPEED = 4
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
        if mode == 0:
            self.image.fill(GROUND_COL)
        else:
            self.image.fill(BACKGROUND_COL)
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
                self.pull += 1
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
            return hits[0].rect.left - orr if steps > 0 else hits[0].rect.right - orl
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
                    Clone(player.rect.x + offset_x, player.rect.y + offset_y)


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, scenesprites, solid, doors, specialblocks
        self._layer = BLOCKLAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill((100, 0, 0))
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
        self.image.fill((255, 100, 0))
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

    def all_pressed(self):
        # print("checking")
        for plate in plates:
            if not plate.is_pressed:
                return False
        return True

    def update(self):
        hits = pygame.sprite.spritecollide(self, playergroup, False) or pygame.sprite.spritecollide(self, solid, False) or pygame.sprite.spritecollide(self, clones, False) or pygame.sprite.spritecollide(self, skidders, False)
        if hits:
            self.image.fill((0, 200, 0))
            self.is_pressed = 1
        else:
            self.image.fill((200, 0, 0))
            self.is_pressed = 0
        if self.all_pressed():
            for plate in plates:
                plate.kill()
            for door in doors:
                door.kill()
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
        elif self.rect.x < 0 or self.rect.x > 800 or self.rect.y < 0 or self.rect.y > 800:
            self.kill()


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
        self.image.fill((200, 200, 0))
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
        self.image.fill((100, 100, 100))
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
        self.image.fill((150, 0, 150))
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


class Text(pygame.sprite.Sprite):
    def __init__(self, txt, col):
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
                self.isreal = 0
                self.pull = -15
        else:
            self.rect.y += self.pull
            self.pull += 1
        if not (0 < self.rect.centerx < 800 and 0 < self.rect.centery < 800):
            self.kill()


class RisingLava(pygame.sprite.Sprite):
    def __init__(self, x, y, s):
        self.groups = all_sprites, scenesprites, lavas, risinglavas
        self._layer = PLATELAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        if len(risinglavas) > 1:
            self.kill()
            return None
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 2
        if s in [10203]:
            self.speed = 1.25
        elif s in [10204, 204, 10209, 10800]:
            self.speed = 1.5
        elif s in [10208]:
            self.speed = 1
        elif s in [10310, 10697]:
            self.speed = 3
        elif s in [10309]:
            self.speed = 4
        elif s in [304]:
            self.speed = 4.25
        elif s in [10599]:
            self.speed = 5
        elif s in [10698]:
            self.speed = 0.1
        self.dubspeed = self.speed * 2
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
                    reset()
                self.transitioning = 1
                self.mobile = 0
        hits = pygame.sprite.spritecollide(self, keygroup, False)
        if hits and not self.transitioning:
            for key in keygroup:
                key.kill()
            for lock in locks:
                lock.kill()
            unlocked.append(scenenum)
        hits = pygame.sprite.spritecollide(self, risers, False)
        if hits:
            hits[0].kill()
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
            self.pull = -14
        hits = pygame.sprite.spritecollide(self, clonepads, False)
        if hits:
            hits[0].activate()

    def update(self):
        global scenenum
        if pygame.sprite.spritecollide(self, solid, False):
            if not self.transitioning:
                reset()
            self.mobile = 0
            self.transitioning = 1
        self.falling = 1
        original_pos = (self.rect.x, self.rect.y)
        self.hittingwater = bool(pygame.sprite.spritecollide(self, water, False))
        wfs = 3
        self.speed = PLAYER_SPEED
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
                self.pull += 0.5
            # print(self.pull)
            self.y_change += self.pull

        self.rect.x += self.x_change
        #print(self.x_change)
        self.wall_collision("x")
        self.rect.y += self.y_change
        self.wall_collision("y")
        #print(self.falling)

        # for spr in all_sprites:
        #     spr.rect.x -= self.x_change

        if self.rect.centerx > 800:
            self.rect.centerx = 0
            scenenum += 1
            initialize_scene()
        elif self.rect.centerx < 0:
            self.rect.centerx = 800
            if scenenum == 199:
                scenenum = 600
            else:
                scenenum -= 1
            initialize_scene()
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

class EndFade(pygame.sprite.Sprite):
    def __init__(self, deaths):
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
        if elapsed < 5:
            self.image.set_alpha((elapsed - 3) * 128)
        elif 6 < elapsed:
            self.image.set_alpha(255)
            write("The End", (400, 400), (255, 255, 255), 70, self.image)
        if 7 < elapsed:
            # print(elapsed, int(elapsed - 5 * 100))
            self.death_amount = max([0, min([int((elapsed - 8) * self.change_rate), self.deaths])])
            write(f"Deaths: {self.death_amount}", (400, 600), (255, 255, 255), 40, self.image)
        if 12 < elapsed < 14:
            if not self.has_changed:
                menu()
                self.has_changed = 1
            self.image.set_alpha(250 - (elapsed - 12) * 125)
        if 14 < elapsed:
            self.kill()


class Fade(pygame.sprite.Sprite):
    def __init__(self):
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
            self.image.set_alpha(250 - (time_passed - 1) * 250)
        else:
            self.kill()


class Helpbox(pygame.sprite.Sprite):
    def __init__(self, name, desc):
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
        write(self.label, (TILESIZE / 2, TILESIZE / 2), (0, 0, 0), self.tsize, self.image)
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
        elif self.hitting:
            self.hitting = 0
            if self.colliderpos(self.lasthitter) != self.objentrance:
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
            self.kill()
            return None
        # print(self)
        global solid
        if self.issolid:
            if counter.total == self.target:
                self.issolid = 0
                self.image.set_alpha(125)
                solid.remove(self)
        else:
            if counter.total != self.target:
                self.issolid = 1
                self.image.set_alpha(255)
                solid.add(self)


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
in_game = 0
controls = 0


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
    global deaths
    deaths += 1
    Fade()
    # global scenenum
    # scenenum = checkpoint[0]
    # player.rect.x = checkpoint[1] * TILESIZE
    # player.rect.y = checkpoint[2] * TILESIZE
    # initialize_scene()


def numscene(s):
    for t in s:
        if isinstance(t, sl.ModTile):
            return True
    return False


def initialize_scene():
    global scene, counter
    # for groundblock in ground:
    #     groundblock.kill()
    # for block in blocks:
    #     block.kill()
    if counter is not None:
        counter.kill()
    for sprite in scenesprites:
        sprite.kill()
    scene = sl.scenes[scenenum]
    if numscene(scene):
        counter = Counter()
    for i in range(20):
        for j in range(20):
            Ground(j, i)
            element = i * 20 + j
            tile = scene[element]
            if isinstance(tile, sl.ModTile):
                Modtile(j, i, tile.label, tile.oper, tile.desc)
            elif isinstance(tile, sl.BlockTile):
                Numblock(j, i, tile.target)
            elif tile == "1":
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


def draw_board():
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
    else:
        if controls == 0:
            mouse = pygame.mouse.get_pos()
            write("The Little Square", (400, 180), (0, 0, 0), 70, screen)
            pygame.draw.rect(screen, (100, 100, 100) if 275 < mouse[0] < 525 and 320 < mouse[1] < 400 else (120, 120, 120), pygame.Rect(275, 320, 250, 80))
            write("PLAY", (400, 360), (0, 0, 0), 40, screen)
            pygame.draw.rect(screen, (100, 100, 100) if 275 < mouse[0] < 525 and 440 < mouse[1] < 520 else (120, 120, 120), pygame.Rect(275, 440, 250, 80))
            write("CONTROLS", (400, 480), (0, 0, 0), 40, screen)
            write(f"Checkpoint code: {checkpoint_code}", (400, 650), (0, 0, 0), 40, screen)
        else:
            write("WASD / Arrow Keys  -  Move Player", (400, 100), (0, 0, 0), 45, screen)
            write("Click / Scroll  -  Shoot Arrow", (400, 200), (0, 0, 0), 45, screen)
            write("Shift + Click  -  Block Information", (400, 300), (0, 0, 0), 45, screen)
            write("R  -  Reset From Checkpoint (Lose All Unlocks)", (400, 400), (0, 0, 0), 45, screen)
            write("Q  -  Get Checkpoint Code", (400, 500), (0, 0, 0), 45, screen)
            write("SPACE  -  Enter Portal / Kill Clones", (400, 600), (0, 0, 0), 45, screen)
            write("ESC  -  Main Menu (Lose Unsaved Progress)", (400, 700), (0, 0, 0), 45, screen)
    fades.draw(screen)


def interpret(code):
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
    return [int(split[i]) for i in range(4)]


def encode(code):
    if code == (0, 9.5, 12.5, 0):
        return "0"
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
    global deaths, checkpoint, checkpoint_code, controls, in_game, unlocked, opened, mode, scenenum
    while running:
        # print(fades)
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
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        spr = get_clicked(mouse[0], mouse[1])
                        if spr is not None:
                            Helpbox(spr.name, spr.desc)
                    else:
                        Arrow(player.rect.x, player.rect.y, mouse)
                else:
                    if controls == 0:
                        if 630 < mouse[1] < 670:
                            checkpoint_code = ""
                        elif 320 < mouse[1] < 400:
                            checkpoint = interpret(checkpoint_code)
                            scenenum = checkpoint[0]
                            deaths = checkpoint[3] - 1
                            initialize_scene()
                            reset()
                        elif 440 < mouse[1] < 520:
                            controls = 1
                    else:
                        controls = 0
            elif event.type == pygame.KEYDOWN:
                if in_game:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and mode == 1 and player.mobile and not player.hittingwater:
                        # player.pull = -JUMP_HEIGHT
                        if (not player.falling):
                            player.pull = -JUMP_HEIGHT
                        elif (pygame.sprite.spritecollide(player, orbs, False)):
                            player.pull = -13
                    elif event.key == pygame.K_q:
                        checkstr = encode(checkpoint)
                        Text(checkstr, (255, 255, 255))
                    elif event.key == pygame.K_SPACE:
                        for clone in clones:
                            clone.kill()
                        hits = pygame.sprite.spritecollide(player, portals, False)
                        if hits:
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
                        unlocked = []
                        opened = []
                        reset()
                    elif event.key == pygame.K_ESCAPE:
                        menu()
                else:
                    if event.unicode in "1234567890." and event.unicode != "":
                        if checkpoint_code == "0":
                            checkpoint_code = ""
                        checkpoint_code += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        if len(checkpoint_code) > 0:
                            checkpoint_code = checkpoint_code[:-1]
        clock.tick(FPS)
        await asyncio.sleep(0)

asyncio.run(main())
