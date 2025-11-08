import pygame, sys, random, math, time, asyncio
import chess_min as chess

pygame.init()

screen = pygame.display.set_mode([720, 810])
pygame.display.set_caption("Escape Room")

def element_at(x, y):
    periodic_table = {
        (1, 1): "H",   (18, 1): "He",
        (1, 2): "Li",  (2, 2): "Be",  (13, 2): "B",   (14, 2): "C",   (15, 2): "N",
        (16, 2): "O",  (17, 2): "F",  (18, 2): "Ne",
        (1, 3): "Na",  (2, 3): "Mg",  (13, 3): "Al",  (14, 3): "Si",  (15, 3): "P",
        (16, 3): "S",  (17, 3): "Cl", (18, 3): "Ar",
        (1, 4): "K",   (2, 4): "Ca",  (3, 4): "Sc",  (4, 4): "Ti",  (5, 4): "V",
        (6, 4): "Cr",  (7, 4): "Mn",  (8, 4): "Fe",  (9, 4): "Co",  (10, 4): "Ni",
        (11, 4): "Cu", (12, 4): "Zn", (13, 4): "Ga", (14, 4): "Ge", (15, 4): "As",
        (16, 4): "Se", (17, 4): "Br", (18, 4): "Kr",
        (1, 5): "Rb",  (2, 5): "Sr",  (3, 5): "Y",   (4, 5): "Zr",  (5, 5): "Nb",
        (6, 5): "Mo",  (7, 5): "Tc",  (8, 5): "Ru",  (9, 5): "Rh",  (10, 5): "Pd",
        (11, 5): "Ag", (12, 5): "Cd", (13, 5): "In", (14, 5): "Sn", (15, 5): "Sb",
        (16, 5): "Te", (17, 5): "I",  (18, 5): "Xe",
        (1, 6): "Cs",  (2, 6): "Ba",  (3, 6): "La",  (4, 6): "Hf",  (5, 6): "Ta",
        (6, 6): "W",   (7, 6): "Re",  (8, 6): "Os",  (9, 6): "Ir",  (10, 6): "Pt",
        (11, 6): "Au", (12, 6): "Hg", (13, 6): "Tl", (14, 6): "Pb", (15, 6): "Bi",
        (16, 6): "Po", (17, 6): "At", (18, 6): "Rn",
        (1, 7): "Fr",  (2, 7): "Ra",  (3, 7): "Ac",  (4, 7): "Rf",  (5, 7): "Db",
        (6, 7): "Sg",  (7, 7): "Bh",  (8, 7): "Hs",  (9, 7): "Mt",  (10, 7): "Ds",
        (11, 7): "Rg", (12, 7): "Cn", (13, 7): "Nh", (14, 7): "Fl", (15, 7): "Mc",
        (16, 7): "Lv", (17, 7): "Ts", (18, 7): "Og"
    }

    return periodic_table.get((x, y), None)

def extended_element_at(x, y):
    lanthanides = [
        "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb",
        "Dy", "Ho", "Er", "Tm", "Yb", "Lu"
    ]

    actinides = [
        "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk",
        "Cf", "Es", "Fm", "Md", "No", "Lr"
    ]

    if y == 1 and 1 <= x <= 15:
        return lanthanides[x - 1]
    elif y == 2 and 1 <= x <= 15:
        return actinides[x - 1]
    else:
        return None

def atomic_number(symbol):
    periodic_order = [
        "H", "He",
        "Li", "Be", "B", "C", "N", "O", "F", "Ne",
        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
        "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "Ga", "Ge", "As", "Se", "Br", "Kr",
        "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
        "In", "Sn", "Sb", "Te", "I", "Xe",
        "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb",
        "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
        "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
        "Tl", "Pb", "Bi", "Po", "At", "Rn",
        "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm",
        "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
        "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn",
        "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
    ]
    return periodic_order.index(symbol) + 1

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, img, game, children, bg=0, desc=None):
        self.groups = all_sprites, game_objs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        isize = img.get_size()
        self.image = img
        self.visible = 1
        self.game = game
        self.children = children
        self.rect = self.image.get_rect()
        self.rect.x = x - isize[0] / 2
        self.rect.y = y - isize[1] / 2
        self.parent = None
        self.is_bg = bg
        self.desc = desc
        self.existent = 1
        self.is_room = 0
        # #print(isize)
        if self.desc in ("parrot_eye", "paper_pin", "top_firefly", "buttons", "clue_placer"):
            self.image.set_alpha(0)
    def draw(self):
        if self.visible:
            if self.desc in ("sky", "zsky"):
                t = self.game.time
                # self.game.time = (self.game.time + 0.25) % 24
                prop = (12 - (abs(t - 12))) / 12
                col1 = (11, 48, 65)
                col2 = (131, 203, 235)
                col = [((col2[i] - col1[i]) * prop + col1[i]) for i in range(3)]
                # #print(col)
                self.image.fill(col)
            screen.blit(self.image, (self.rect.x, self.rect.y))
    def gen_id(self, prev, index):
        return
        if len(prev) > 1:
            self.visible = 0
        self.id = list(prev) + [index]
        #print(self.id)
        for i, child in enumerate(self.children):
            child.gen_id(self.id, i)
    def onclick(self):
        if len(self.children) > 0:
            if self.desc == "end":
                self.game.game_over = 1
                Fade(self.zoom, 1, 2, 810)
            else:
                Fade(self.zoom)
            # self.zoom()
        else:
            self.click_actions(pygame.mouse.get_pos())
    def zoom(self):
        self.parent = self.game.lens
        self.game.lens = self
        for spr in specials:
            spr.kill()
        for sprite in all_sprites:
            sprite.visible = 0
        for child in self.children:
            child.appear()
            # #print(child, child.id)
        self.on_entry()
    def click_actions(self, mouse):
        if self.desc == "paper_pin":
            FallingPaper(460, 345, self.game.croppedpaper)
            paper = self.game.lens.children[2]
            # paper.visible = 0
            # paper.existent = 0
            paper.kill()
            # self.visible = 0
            # self.existent = 0
            self.kill()
            new_obj = Object(200, 620, pygame.transform.smoothscale(self.game.pic(15), (75, 62)), self.game, [], 0, "paper_item")
            new_obj.visible = 0
            self.game.root.children.append(new_obj)
            self.game.collect(InventoryItem("pin", pygame.transform.smoothscale(self.game.pic(24), (40, 40))))
            self.game.progress.add("pin_collected")
            #print(all_sprites)
        elif self.desc == "paper_item":
            self.game.collect(InventoryItem("paper", self.image))
            self.kill()
        elif self.desc == "buttons":
            y = (mouse[1] - self.rect.y) // ((self.rect.height + 15) / 5)
            x = (mouse[0] - self.rect.x) // (self.rect.width / 2)
            num = (y * 2 + x + 1) % 10
            #print(num)
            for scrn in tv_screens:
                scrn.button(num)
        elif self.desc == "clue_placer":
            holding = self.game.holding()
            if holding and holding.name == "clue":
                if "pin_collected" not in self.game.progress:
                    self.game.make_txt("not enough space on board")
                    return
                #print("creating obj")
                WinFade()
                #print(holding.name, holding.id)
                index = int(holding.id[-1]) - 1
                self.game.lens.children.append(Object(300, 220 + 90 * index, self.game.clue_imgs[index], self, [], 1))
                self.game.lose_item()
        # elif self.desc == "watch":
        #     holding = self.game.holding()
        #     if holding and holding.name == "pin":
        #         WinFade()
        #         self.image = self.game.altwatch
        #         self.rect.y -= 5
        #         self.game.lose_item()
        elif self.desc == "egg":
            if self.game.egg_frame == 4:
                holding = self.game.holding()
                if holding and holding.name == "eyedrops":
                    self.game.lose_item()
                else:
                    return
            elif self.game.egg_frame >= 6:
                return
            elif self.game.egg_frame == 0:
                holding = self.game.holding()
                if holding and holding.name == "ash":
                    self.game.lose_item()
                else:
                    return
            self.game.egg_frame += 1
            self.image = self.game.eggs[self.game.egg_frame]
            match self.game.egg_frame:
                case 1:
                    WinFade()
                    self.rect.y -= 12
                case 3:
                    WinFade()
                    self.rect.x = 350 - self.image.get_size()[0] / 2
                    self.rect.y = 210
                case 4:
                    WinFade()
                    self.rect.x = 350 - self.image.get_size()[0] / 2
                    self.rect.y = 115
                case 6:
                    self.game.collect(InventoryItem("water", self.game.pic(60, (80, 80))))
        elif self.desc == "flag":
            holding = self.game.holding()
            if holding:
                if holding.name == "water":
                    WinFade()
                    self.game.lose_item()
                    self.image = pygame.transform.smoothscale(self.game.kiribati2, (700, 350))
                    self.game.flag_prev.image = pygame.transform.smoothscale(self.game.kiribati2, (180, 90))
                    self.game.progress.add("water_added")
                elif holding.name == "sun":
                    if "water_added" in self.game.progress:
                        WinFade()
                        self.game.lose_item()
                        self.image = pygame.transform.smoothscale(self.game.kiribati3, (700, 350))
                        self.game.flag_prev.image = pygame.transform.smoothscale(self.game.kiribati3, (180, 90))
                        self.game.progress.add("sun_added")
                    else:
                        self.game.make_txt("wrong order")
                elif holding.name == "bird":
                    if "sun_added" in self.game.progress:
                        WinFade()
                        self.game.lose_item()
                        self.image = pygame.transform.smoothscale(self.game.kiribati4, (700, 350))
                        self.game.flag_prev.image = pygame.transform.smoothscale(self.game.kiribati4, (180, 90))
                        self.game.progress.add("flag_complete")
                        self.game.next_swipe = random.choice([-1, 1])
                    else:
                        self.game.make_txt("wrong order")
        elif self.desc == "owl":
            if "owl_dial1" not in self.game.progress:
                WinFade((200, 0, 0))
                self.image = self.game.front_owl
                self.rect.x -= 20
                self.rect.y -= 5
                self.game.make_txt("Do not be fooled. They're listening.")
                self.game.progress.add("owl_dial1")
            elif "owl_dial2" not in self.game.progress:
                self.game.make_txt("The birds are more than they seem.")
                self.game.progress.add("owl_dial2")
            else:
                WinFade()
                self.image = pygame.Surface((0, 0))
                self.rect = pygame.Rect(0, 0, 0, 0)
                Item(360, 360, self.game.scroll, "clue", "clue4", self.game, 1)
    def reset(self):
        if self.desc == "owl":
            if "owl_dial1" in self.game.progress:
                self.game.progress.remove('owl_dial1')
                self.game.progress.remove('owl_dial2')
                self.image = self.game.right_owl
                self.rect = self.image.get_rect()
                isize = self.image.get_size()
                self.rect.x, self.rect.y = 360 - isize[0] / 2, 360 - isize[1] / 2
        self.game.game_over = 0
    def on_entry(self):
        if self.desc is not None and self.desc not in self.game.progress:
            match self.desc:
                case "orangebird":
                    random.seed(3)
                    for y in range(4):
                        for x in range(4):
                            PicTile(x * 92, y * 92, self.game.small_orange_bird, random.randint(0, 3), self.game)
                case "jar":
                    Firefly(300, 420, self.game.firefly, 0)
                    Firefly(390, 320, self.game.firefly, 2)
                    Firefly(425, 400, self.game.firefly, 4)
                case "top_firefly":
                    Firefly(360, 360, self.game.big_firefly, 0)
                case "mathvault":
                    #print("mg")
                    self.game.num_arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                    x_pos = (220, 340, 490)
                    y_pos = (225, 335, 445)
                    for i, y in enumerate(y_pos):
                        for j, x in enumerate(x_pos):
                            MathSlot(x, y, i, j)
                    for i, y in enumerate(y_pos):
                        for j, x in enumerate(x_pos):
                            MathTile(x, y, i * 3 + j + 1, i, j, self.game)
                case "vase_shelf":
                    Vase(360, 310, self.game.vase)
                case "tv_shelf":
                    TVScreen(290, 305, self.game.tv_imgs, self.game, self.game.tv_level)
                case "periodic":
                    Periodic(0, 60, self.game.periodic, self.game)
                case "codevault":
                    for x in range(4):
                        CodeNum(204 + 56 * x, 175, self.game.digits, x)
                # case "sky":
                #     ZoomedSky(360, 330)
                #     #print(all_sprites)
                case "sky":
                    t = self.game.time
                    if 9 <= t <= 15:
                        if "sun" not in self.game.progress:
                            Item(480, 215, self.game.sun, "sun", "sun", self.game, 1, self.game.small_sun)
                    elif 5 <= t <= 19:
                        pass
                    else:
                        Moon(480, 215, self.game.moon)
                        #print(all_sprites)
                case "table":
                    if "fixed_watch" in self.game.progress:
                        ClockHands(222, 332, self.game, self.children[2])
                    else:
                        ClockHands(208, 335, self.game, self.children[2])
                # case "end":
                #     self.game.game_over = 1
    def appear(self):
        if self.existent:
            self.visible = 1

class ClockHands(pygame.sprite.Sprite):
    def __init__(self, x, y, game, watch):
        self.groups = all_sprites, specials, hands
        super().__init__(self.groups)
        self.image = pygame.Surface((220, 220)).convert_alpha()
        self.rect = self.image.get_rect()
        # 207, 335
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2
        self.game = game
        self.watch = watch
        self.mousedown = 0
    def onclick(self):
        if "fixed_watch" in self.game.progress:
            self.mousedown = 1
        else:
            holding = self.game.holding()
            if holding and holding.name == "pin":
                WinFade()
                self.watch.image = self.game.altwatch
                self.watch.rect.y -= 5
                self.game.lose_item()
                # self.kill()
                self.rect.x += 14
                self.rect.y -= 3
                self.game.progress.add("fixed_watch")
    def update(self):
        self.image.fill((0, 0, 0, 0))
        if self.mousedown:
            self.game.time = (self.game.time + 0.03) % 24
        t = self.game.time
        for i, prop in enumerate((((t % 12) / 12), t - int(t))):
            theta = prop * math.pi * 2
            scalar = [85, 110][i]
            dx = scalar * math.sin(theta)
            dy = -(scalar * math.cos(theta))
            pygame.draw.line(self.image, (147, 84, 18), (110, 110), (110 + dx, 110 + dy), 7)


class Moon(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.groups = all_sprites, specials
        super().__init__(self.groups)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2

class Owl(pygame.sprite.Sprite):
    def __init__(self, pic, x):
        self.groups = all_sprites, specials
        super().__init__(self.groups)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 510

class Gloom(pygame.sprite.Sprite):
    def __init__(self, alpha):
        self.groups = all_sprites, specials
        super().__init__(self.groups)
        self.image = pygame.Surface((720, 720))
        self.rect = self.image.get_rect()
        self.image.set_alpha(alpha)

class Frigate(pygame.sprite.Sprite):
    def __init__(self, pic, dir):
        self.groups = all_sprites, specials
        super().__init__(self.groups)
        self.image = pic
        self.rect = self.image.get_rect()
        if dir == 1:
            self.rect.x = -150
        else:
            self.rect.x = 750
        self.dx = 3 * dir
        self.y_shift = random.randint(100, 400)
        self.stime = time.time()
    def update(self):
        t = time.time()
        if t - self.stime > 2:
            #print(self.rect.x)
            self.rect.x += self.dx
            self.rect.y = 25 * math.sin(time.time()) + self.y_shift
            if self.rect.x > 750 or self.rect.x < -150:
                self.kill()

class Label(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites, specials
        super().__init__(self.groups)
        self.image = pygame.Surface((720, 60)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.col = (25, 0, 50, 0)
        self.image.fill(self.col)
    def disp(self, text):
        self.image.fill(self.col)
        write(text, (360, 30), (250, 250, 250), 50, self.image)

class Periodic(pygame.sprite.Sprite):
    def __init__(self, x, y, img, game):
        self.groups = all_sprites, specials, periodics
        super().__init__(self.groups)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.clickpoint = None
        self.name_label = Label(0, 0)
        self.num_label = Label(0, 660)
        self.clicking = 0
        self.name = ""
        self.num = ""
        self.game = game
        #print(all_sprites)
        if "per_open" not in game.progress:
            game.progress.add("per_open")
            game.make_txt("some objects you can drag")
        if "per" not in game.progress:
            self.name = game.per_name
            self.num = game.per_num
            self.name_label.disp(self.name)
            self.num_label.disp(self.num)
    def update(self):
        if self.clickpoint:
            mx, my = pygame.mouse.get_pos()
            cx, cy = self.clickpoint
            if (mx - cx, my - cy) != (self.rect.x, self.rect.y):
                self.clicking = 0
            self.rect.x = mx - cx
            self.rect.y = my - cy
    def onclick(self):
        mx, my = pygame.mouse.get_pos()
        self.clickpoint = (mx - self.rect.x, my - self.rect.y)
        self.clicking = 1
        #print(self.clickpoint)
    def release(self):
        if self.clicking:
            cx, cy = self.clickpoint
            ex = (cx - 70) // 76
            ey = (cy - 125) // 76
            #print(ex, ey)
            if ey < 8:
                el = element_at(ex + 1, ey + 1)
            else:
                #print(ex, ey)
                el = extended_element_at(ex - 2, ey - 7)
            if el is not None:
                self.name += el
                self.num += str(atomic_number(el))
                self.name_label.disp(self.name)
                self.num_label.disp(self.num)
                ans = "PoTaSSiUMtIn"
                length = len(self.name)
                if "per" not in self.game.progress and ans[:length] == self.name and (length >= 12 or ans[length] == ans[length].upper()):
                    self.game.per_name, self.game.per_num = self.name, self.num
                    if length == 12:
                        WinFade()
                        self.game.progress.add("per")
                        self.name = ""
                        self.num = ""
            #print()
        self.clicking = 0
        self.clickpoint = None


class Firefly(pygame.sprite.Sprite):
    def __init__(self, x, y, img, offset):
        self.groups = all_sprites, specials
        super().__init__(self.groups)
        self.image = img
        self.rect = self.image.get_rect()
        isize = self.image.get_size()
        self.y = y - isize[1] / 2
        self.rect.x = x - isize[0] / 2
        self.rect.y =  self.y
        self.stime = time.time() - offset
    def update(self):
        self.rect.y = self.y + 10 * math.sin(time.time() - self.stime)

# class ZoomedSky(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         self.groups = all_sprites, specials
#         super().__init__(self.groups)
#         self.image = pygame.Surface((400, 360))
#         self.rect = self.image.get_rect()
#         self.rect.x = x - self.rect.width / 2
#         self.rect.y = y - self.rect.height / 2

class FallingPaper(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.groups = all_sprites, specials
        super().__init__(self.groups)
        self.image = img
        self.rect = self.image.get_rect()
        isize = self.image.get_size()
        self.x = x - isize[0] / 2
        self.rect.x = self.x
        self.rect.y = y - isize[1] / 2
        self.stime = time.time()
    def update(self):
        self.rect.y += 2
        self.rect.x = self.x + 50 * math.sin(time.time() - self.stime)
        if self.rect.y > 720:
            self.kill()
    def onclick(self):
        pass

class Text(pygame.sprite.Sprite):
    def __init__(self, txt, font):
        self.groups = all_sprites, texts
        super().__init__(self.groups)
        textimg = font.render(txt, True, (255, 255, 255))
        wid, height = textimg.get_size()
        self.image = pygame.Surface((wid + 20, height + 20))
        self.image.blit(textimg, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = 710 - self.rect.width
        self.rect.y = 10
        self.stime = time.time()
    def update(self):
        self.alpha = min(255, 450 - 125 * (time.time() - self.stime))
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)

class InventoryItem:
    def __init__(self, name, img, id=None):
        self.name = name
        self.img = img
        self.size = self.img.get_size()
        self.id = id if id is not None else name
    def draw(self, x, y):
        screen.blit(self.img, (x - self.size[0] / 2, y - self.size[1] / 2))

class WinFade(pygame.sprite.Sprite):
    def __init__(self, col=(255, 255, 255)):
        self.groups = all_sprites, winfades
        super().__init__(self.groups)
        self.image = pygame.Surface((720, 720))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.image.fill(col)
        self.alpha = 240
        self.image.set_alpha(self.alpha)
    def update(self):
        self.alpha -= 10
        if self.alpha <= 0:
            self.kill()
            return
        self.image.set_alpha(self.alpha)

class Fade(pygame.sprite.Sprite):
    def __init__(self, process, upspeed=30, downspeed=30, height=720):
        if fades:
            return
        self.groups = all_sprites, fades
        super().__init__(self.groups)
        self.proc = process
        self.image = pygame.Surface((720, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.image.fill((0, 0, 0))
        self.alpha = 0
        self.image.set_alpha(self.alpha)
        self.phase = 0
        self.upspeed = upspeed
        self.downspeed = downspeed
    def update(self):
        # #print('i exist')
        self.image.set_alpha(self.alpha)
        if self.phase == 0:
            self.alpha += self.upspeed
            if self.alpha >= 255:
                self.phase = 1
                self.alpha = 255
                self.proc()
        else:
            self.alpha -= self.downspeed
            if self.alpha <= 0:
                self.kill()

class PicTile(pygame.sprite.Sprite):
    def __init__(self, x, y, img, rot, game):
        self.groups = all_sprites, specials, pictiles
        super().__init__(self.groups)
        self.image = pygame.Surface((92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = x + 360 - 92 * 2
        self.rect.y = y + 360 - 92 * 2 - 5
        #print(x, y)
        self.image.blit(img, (0, 0), (x, y, 92, 92))
        self.game = game
        for _ in range(rot):
            self.image = pygame.transform.rotate(self.image, 90)
        self.rot = rot
    def onclick(self):
        if self.all_correct():
            for tile in pictiles:
                tile.kill()
            self.game.progress.add('orangebird')
            # self.game.root.children[2].kill()
            self.game.orange_prev.kill()
            self.game.collect(InventoryItem("bird", pygame.transform.smoothscale(self.game.pic(26), (60, 25))))
            return
        self.image = pygame.transform.rotate(self.image, 90)
        self.rot = (self.rot + 1) % 4
    def all_correct(self):
        for tile in pictiles:
            if tile.rot != 0:
                return False
        return True

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, img, name, id, game, c=0, altimg=None):
        self.groups = all_sprites, specials
        super().__init__(self.groups)
        self.image = img
        self.rect = self.image.get_rect()
        if c:
            isize = img.get_size()
            self.rect.x = x - isize[0] / 2
            self.rect.y = y - isize[1] / 2
        else:
            self.rect.x = x
            self.rect.y = y
        self.id = id
        self.game = game
        self.alpha = None
        self.name = name
        self.altimg = altimg
        self.taken = 0
    def onclick(self):
        self.taken = 1
        self.game.progress.add(self.id)
        if self.altimg:
            self.image = self.altimg
        self.game.collect(InventoryItem(self.name, self.image, self.id))
        self.kill()
        if self.id == "clue4":
            Fade(self.leave_room, 250, 2)
    def leave_room(self):
        self.game.room = 1
        self.game.lens = self.game.rooms[1]
        self.game.transition()
    def update(self):
        if self.alpha is not None:
            self.alpha -= 20
            if self.alpha <= 0:
                self.kill()
                return
            self.image.set_alpha(self.alpha)

class MathTile(pygame.sprite.Sprite):
    def __init__(self, x, y, num, i, j, game):
        self.groups = all_sprites, specials, mathtiles
        super().__init__(self.groups)
        wid = 70
        self.image = pygame.Surface((wid, wid), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (160, 150, 140), pygame.Rect(0, 0, wid, wid), border_radius=10)
        pygame.draw.rect(self.image, (180, 170, 160), pygame.Rect(5, 5, wid - 10, wid - 10), border_radius=8)
        write(num, (35, 35), (0, 0, 0), 50, self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x - wid / 2, y - wid / 2
        self.dragging = 0
        self.i = i
        self.j = j
        self.game = game
        self.num = num
        #print(all_sprites)
        #print(self)
    def onclick(self):
        self.dragging = 1
        if self.i is not None:
            self.game.num_arr[self.i][self.j] = None
        #print(self.game.num_arr)
    def update(self):
        if self.dragging:
            mx, my = pygame.mouse.get_pos()
            self.rect.centerx = mx
            self.rect.centery = my
    def release(self):
        if self.dragging:
            self.dragging = 0
            point = (self.rect.centerx, self.rect.centery)
            for slot in mathslots:
                if slot.rect.collidepoint(point):
                    self.rect.x, self.rect.y = slot.rect.x, slot.rect.y
                    self.i, self.j = slot.i, slot.j
                    self.game.num_arr[self.i][self.j] = self.num
                    self.eval_done()
                    #print(self.game.num_arr)
                    return
            self.i = None
            #print(self.game.num_arr)
    def eval_done(self):
        arr = self.game.num_arr
        for row in arr:
            if None in row:
                return
        if arr[0][0] + arr[0][1] != arr[0][2]:
            return 
        if arr[1][0] - arr[1][1] != arr[1][2]:
            return
        if arr[2][0] * arr[2][1] != arr[2][2]:
            return
        if "wohoo" not in self.game.progress:
            self.game.progress.add("wohoo")

class MathSlot(pygame.sprite.Sprite):
    def __init__(self, x, y, i, j):
        self.groups = all_sprites, specials, mathslots
        super().__init__(self.groups)
        wid = 70
        self.image = pygame.Surface((wid, wid), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (160, 160, 160), pygame.Rect(0, 0, wid, wid), border_radius=10)
        # pygame.draw.rect(self.image, (200, 200, 200), pygame.Rect(3, 3, wid - 6, wid - 6), border_radius=8)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x - wid / 2, y - wid / 2
        self.i = i
        self.j = j
        #print(all_sprites)
        #print(self)

# class MathVault(Object):
#     def __init__(self, x, y, img, game, children):
#         super().__init__(x, y, img, game, children)
#     def on_entry(self):
#         MathSlot(360, 360)

class Book(Object):
    def __init__(self, x, y, images, game, children):
        self.img_index = 0
        self.images = images
        self.img = self.images[self.img_index]
        super().__init__(x, y, self.img, game, children)
    def click_actions(self, mouse):
        x = mouse[0]
        if self.img_index == 2 and x > 360:
            return
        if self.img_index == 0 or mouse[0] > 360:
            self.img_index = (self.img_index + 1) % len(self.images)
        else:
            self.img_index = (self.img_index - 1) % len(self.images)
        self.image = self.images[self.img_index]
        isize = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = self.x - isize[0] / 2
        self.rect.y = self.y - isize[1] / 2

class Furnace(Object):
    def __init__(self, x, y, img, altimg, game, children):
        self.img = img
        self.img_index = 0
        self.altimg = altimg
        self.inv_item = None
        self.item = None
        super().__init__(x, y, img, game, children)
    def click_actions(self, mouse):
        if self.img_index == 1 and 220 < mouse[0] < 480 and 230 < mouse[1] < 420 and not self.inv_item:
            holding = self.game.holding()
            if holding:
                #print(holding)
                self.inv_item = holding
                self.game.lose_item()
                self.item = Item(335, 325, self.inv_item.img, self.inv_item.name, self.inv_item.id, self.game, 1)
                return
        self.img_index = 1 - self.img_index
        self.image = self.altimg if self.img_index == 1 else self.img
        if self.img_index == 1 and self.inv_item:
            if self.inv_item.name == "paper":
                self.item = Item(335, 345, self.game.ash, "ash", "ash", self.game, 1)
            else:
                self.item = Item(335, 325, self.inv_item.img, self.inv_item.name, self.inv_item.id, self.game, 1)
        elif self.img_index == 0:
            if self.item and self.item.alive():
                self.item.kill()
                #print('kli')
            else:
                self.inv_item = None
                self.item = None
        # if self.img_index == 1 and self.item is None and "eyedrops" not in self.game.progress:
        #     self.item = Item(350, 350, self.item_img, "eyedrops", "eyedrops", self.game)
        # elif self.item is not None:
        #     self.item.kill()
        #     self.item = None
    def reset(self):
        self.img_index = 0
        self.image = self.img
        if self.inv_item:
            if self.item.taken:
                self.inv_item = None
            self.item.kill()
        else:
            self.inv_item = None
            self.item = None

class Cabinet(Object):
    def __init__(self, x, y, img, altimg, game, children):
        self.img = img
        self.img_index = 0
        self.altimg = altimg
        self.item_img = pygame.image.load("Pictures/Picture5.png").convert_alpha()
        self.item = None
        super().__init__(x, y, img, game, children)
    def click_actions(self, mouse):
        self.img_index = 1 - self.img_index
        self.image = self.altimg if self.img_index == 1 else self.img
        if self.img_index == 1 and self.item is None and "eyedrops" not in self.game.progress:
            self.item = Item(350, 350, self.item_img, "eyedrops", "eyedrops", self.game)
        elif self.item is not None:
            self.item.kill()
            self.item = None
    def reset(self):
        self.img_index = 0
        self.image = self.img
        self.item = None

class Vase(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.groups = all_sprites, specials, vases
        super().__init__(self.groups)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2
        self.mousedown = None
    def update(self):
        if self.mousedown is not None:
            self.rect.centerx = pygame.mouse.get_pos()[0] - self.mousedown
    def onclick(self):
        self.mousedown = pygame.mouse.get_pos()[0] - self.rect.centerx

class Vault(Object):
    def __init__(self, x, y, img, altimg, game, children):
        self.img = img
        self.img_index = 0
        self.altimg = altimg
        self.item_img = game.scroll
        self.item = None
        super().__init__(x, y, img, game, children)
    def click_actions(self, mouse):
        if not self.img_index and "wohoo" in self.game.progress:
            for tile in mathtiles:
                tile.kill()
            for slot in mathslots:
                slot.kill()
            self.img_index = 1
            self.rect.x += 20
            self.image = self.altimg
            if self.img_index == 1 and self.item is None and "clue1" not in self.game.progress:
                self.item = Item(330, 330, self.item_img, "clue", "clue1", self.game, 1)
    def reset(self):
        self.img_index = 0
        self.image = self.img
        self.item = None
        self.rect.centerx = 360

class CodeNum(pygame.sprite.Sprite):
    def __init__(self, x, y, digits, id):
        self.groups = all_sprites, specials, codenums
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pygame.Surface([35, 35]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill((255, 255, 255, 0))
        self.offset = 12
        self.image.blit(digits, (0, 0), (12, 12, 35, 35))
        self.digits = digits
        self.num = 0
        self.current = self.offset
        self.shift = 3
        self.id = id
    def onclick(self):
        #print(self.num)
        if self.num < 10 or self.current == self.offset:
            self.offset += 34.6
            self.num += 1
            # if self.num > 10:
            #     self.num = 0
            #     self.offset = 12
    def update(self):
        if self.current > self.offset:
            self.current = self.offset
        elif self.current < self.offset - 1:
            self.current += (self.offset - self.current) / 5
        else:
            self.current = self.offset
            if self.num >= 10:
                self.num = 0
                self.offset = 12
        self.image.fill((255, 255, 255, 0))
        s = self.shift
        self.image.blit(self.digits, (s, s), (12 + s, self.current + s, 35 - 2 * s, 35 - 2 * s))

class CodeVault(Object):
    def __init__(self, x, y, img, altimg, game, children):
        self.img = img
        self.img_index = 0
        self.altimg = altimg
        self.item_img = game.scroll
        self.item = None
        self.ans = [3, 3, 5, 1]
        super().__init__(x, y, img, game, children)
    def click_actions(self, mouse):
        for codenum in codenums:
            if self.ans[codenum.id] != codenum.num:
                return
        if not self.img_index:
            for codenum in codenums:
                codenum.kill()
            self.img_index = 1
            self.rect.x += 20
            self.image = self.altimg
            if self.img_index == 1 and self.item is None and "clue3" not in self.game.progress:
                self.item = Item(330, 330, self.item_img, "clue", "clue3", self.game, 1)
    def reset(self):
        self.img_index = 0
        self.image = self.img
        self.item = None
        self.rect.centerx = 360

class ChessBoard(Object):
    def __init__(self, x, y, img, game, children):
        self.img = img
        self.item_img = pygame.image.load("Pictures/Picture5.png").convert_alpha()
        super().__init__(x, y, img, game, children)
        # self.board = chess.Board('8/6R1/1N6/5B2/5P2/2K5/8/8')
        self.board = chess.Board('8/8/5q2/1n6/3b1k2/1R6/8/8')
        self.pieces = self.game.chess_pieces
        # #print(self.board)
        self.piece_order = "KQBNRP"
        self.selected = None
        self.puzzle = 0
        self.puzzles = [
            "8/8/5q2/1n6/3b1k2/1R6/8/8",
            "8/8/4q3/1b6/6k1/2N5/4r3/8 ",
            "8/8/5b2/4p3/3qR1n1/3k4/8/8",
            "8/8/2npk3/2pprb2/2ppnn2/2pppQ2/8/8"
        ]
        self.paint()
    def paint(self):
        self.img.fill((0, 0, 0))
        for y in range(8):
            for x in range(8):
                index = (7 - y) * 8 + x
                if index != self.selected:
                    col = [(230, 210, 170), (110, 75, 30)][(x + y) % 2]
                else:
                    col = (200, 200, 0)
                pygame.draw.rect(self.img, col, pygame.Rect(80 * x, 80 * y, 80, 80))
                piece = self.board.piece_at(index)
                if piece is not None:
                    #print(str(piece).upper())
                    self.img.blit(self.pieces, (x * 80, y * 80), (self.piece_order.index(str(piece).upper()) * 80, 80 * (piece.color == chess.BLACK), 80, 80))
        for y in range(8):
            write(8 - y, (12, y * 80 + 20), [(210, 190, 150), (90, 55, 10)][y % 2], 30, self.image)
        for x in range(8):
            write("abcdefgh"[x], (x * 80 + 65, 628), [(210, 190, 150), (90, 55, 10)][1 - x % 2], 30, self.image)
    def click_actions(self, mouse):
        mx, my = mouse
        my -= 40
        mx -= 40
        clicked = (7 - my // 80) * 8 + mx // 80
        clicked_piece = self.board.piece_at(clicked)
        if self.selected == clicked:
            self.selected = None
        elif clicked_piece is not None and clicked_piece.color == chess.WHITE:
            self.selected = clicked
        elif self.selected is not None:
            move = chess.Move(self.selected, clicked)
            #print(f'attempting move: {move}')
            if self.puzzle < len(self.puzzles):
                if clicked_piece is not None:
                    #print("clicked piece is not None.")
                    #print(self.board.legal_moves())
                    if move in self.board.legal_moves():
                        #print("move is legal")
                        self.board.push(move)
                        #print(clicked_piece.piece_type)
                        self.board.set_piece_at(clicked, chess.Piece(clicked_piece.piece_type, chess.WHITE))
                        # self.board.set_piece_at(clicked).piece_type = clicked_piece.piece_type
                        self.board.turn = chess.WHITE
                        self.selected = None
                        if sum(1 if sq != "." else 0 for sq in self.board.board) == 1:
                            self.puzzle += 1
                            if self.puzzle < len(self.puzzles):
                                self.board.set_fen(self.puzzles[self.puzzle])
                            else:
                                WinFade()
                                self.board.set_fen('8/6R1/1N6/5B2/5P2/2K5/8/8')
            else:
                if clicked > 55 and self.board.piece_at(self.selected).piece_type == chess.PAWN:    
                    move.promotion = chess.QUEEN
                if move in self.board.legal_moves():
                    #print('lgl')
                    self.board.push(move)
                    self.board.turn = chess.WHITE
                    self.selected = None
        self.paint()
        if not "chess_board" in self.game.progress:
            p = self.board.piece_at(chess.square(1, 6))
            if p and p.piece_type == chess.KNIGHT:
                p = self.board.piece_at(chess.square(3, 3))
                if p and p.piece_type == chess.ROOK:
                    p = self.board.piece_at(chess.square(6, 1))
                    if p and p.piece_type == chess.QUEEN:
                        p = self.board.piece_at(chess.square(5, 5))
                        if p and p.piece_type == chess.KING:
                            self.game.progress.add("chess_board")
                            #print("ALL CORRECT!")
                            Ghost(self.game.front_owl)
                            self.game.make_txt("The illusion is broken.")
                            for obj in (self.game.orange_prev, self.game.parrot_prev, self.game.rook_prev):
                                obj.image = pygame.Surface((32, 33))
                                obj.rect.y -= 1
                            self.game.root.children.append(self.game.space_clicker)
        #print('tih')
    def reset(self):
        self.selected = None
        if self.puzzle < len(self.puzzles):
            self.board.set_fen(self.puzzles[self.puzzle])
        self.paint()

class Ghost(pygame.sprite.Sprite):
    def __init__(self, pic):
        self.groups = all_sprites, specials
        super().__init__(self.groups)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.centerx = 360
        self.rect.centery = 360
        self.alpha = 255
    def update(self):
        self.alpha -= 4
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)

class TVScreen(pygame.sprite.Sprite):
    def __init__(self, x, y, imgs, game, lvl):
        self.groups = all_sprites, specials, tv_screens
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.imgs = imgs
        # self.image = self.imgs[0].copy()
        # self.rect = self.image.get_rect()
        # self.rect.x = x - self.rect.width / 2
        # self.rect.y = y - self.rect.height / 2
        self.x = x
        self.y = y
        self.answers = [0, 2, 9, 5, 4, 6, 8, 9]
        self.typed = ""
        self.game = game
        self.level = lvl
        self.init_level()
    def button(self, num):
        if self.level == 0:
            self.typed += str(int(num))
            if len(self.typed) >= 4:
                if self.typed == "1950":
                    WinFade()
                    self.level += 1
                else:
                    WinFade((125, 0, 0))
                self.typed = ""
                self.init_level()
            else:
                write(int(num), (-40 + 70 * len(self.typed), 30), (0, 0, 0), 40, self.image)
                #print(self.rect.x, self.rect.y)
        else:
            if num == self.answers[self.level]:
                WinFade()
                self.level += 1
                self.init_level()
            else:
                WinFade((125, 0, 0))
                self.level = 1
                self.init_level()
    def init_level(self):
        if self.level >= 8:
            self.kill()
            if "clue2" not in self.game.progress:
                Item(self.rect.centerx, self.rect.centery, self.game.scroll, "clue", "clue2", self.game, 1)
            return
        self.game.tv_level = self.level
        self.image = self.imgs[self.level] if self.level else self.imgs[self.level].copy()
        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.rect.width / 2
        self.rect.y = self.y - self.rect.height / 2

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
        self.frame_img = pygame.image.load('Pictures/Picture6.png').convert_alpha()
        self.small_frame = pygame.transform.smoothscale(self.frame_img, (60, 60))
        self.orange_bird = pygame.image.load('Pictures/orangebirdimage.jpg')
        self.orange_bird = pygame.transform.smoothscale(self.orange_bird, (490, 368))
        self.small_orange_bird = pygame.Surface((368, 368))
        self.small_orange_bird.blit(self.orange_bird, (0, 0), (61, 0, 368, 368))
        self.parrot = pygame.image.load('Pictures/Picture8.jpg')
        self.small_parrot = pygame.transform.smoothscale(self.parrot, (368, 368))
        self.wallbg = pygame.image.load('Pictures/Screenshot 2025-07-03 143135.png').convert_alpha()
        self.knight = pygame.image.load('Pictures/Picture9.jpg')
        self.rook = pygame.image.load('Pictures/Picture12.jpg')
        self.bulletin = pygame.image.load('Pictures/Picture13.png')
        self.paperimg = pygame.image.load('Pictures/Picture14.png')
        self.croppedpaper = pygame.image.load('Pictures/Picture15.png')
        self.space = pygame.image.load('Pictures/Picture68.jpg')
        self.def_firefly = self.pic(21)
        self.big_firefly = pygame.transform.smoothscale(self.def_firefly, (512, 512))
        self.firefly = pygame.transform.smoothscale(self.def_firefly, (64, 64))
        self.jar_bg = pygame.Surface((720, 720))
        self.jar_bg.fill((209, 222, 224))
        self.queen = pygame.image.load("Pictures/Picture22.jpg")
        self.room_bg =  pygame.image.load('Pictures/Picture4.png')
        self.shelf_bg = pygame.transform.smoothscale(self.pic(20), (720, 125))
        self.inventory = [None for _ in range(9)]
        self.i_sel = None
        self.font = pygame.font.Font(None, 30)
        self.chess_pieces = pygame.transform.smoothscale(pygame.image.load("Pictures/800px-Chess_Pieces_Sprite.svg.png"), (480, 160))
        self.dark_bg = self.pic(30)
        self.shelf = self.pic(16)
        self.kiribati1 = self.pic(39)
        self.kiribati2 = self.pic(38)
        self.kiribati3 = self.pic(62)
        self.kiribati4 = self.pic(63)
        self.num_arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.vase = self.pic(43)
        self.tv_imgs = []
        self.clue_imgs = [pygame.transform.smoothscale_by(self.clue(i + 1), 0.3) for i in range(4)]
        self.tv_level = 0
        self.per_name = ""
        self.per_num = ""
        self.periodic = pygame.image.load("Pictures/periodictable.png")
        self.scroll = self.pic(42)
        self.digits = self.pic(49, (59, 413))
        self.moon = self.pic(55)
        self.sun = self.pic(54)
        self.small_sun = pygame.transform.smoothscale_by(self.sun, 0.75)
        self.altwatch = self.pic(57)
        self.egg_frame = 0
        self.eggs = [self.egg(i) for i in range(1, 7)]
        self.eggs[2] = pygame.transform.smoothscale(self.eggs[2], (439, 659))
        self.eggs[5] = pygame.transform.smoothscale(self.eggs[5], (524, 524))
        self.eggs.append(self.eggs[4])
        self.frigate1 = self.pic(65)
        self.frigate2 = pygame.transform.flip(self.frigate1, True, False)
        self.frigate = None
        self.next_swipe = 1
        self.frigate_num = 0
        self.right_owl = self.pic(66)
        self.front_owl = self.pic(67)
        self.small_owl = pygame.transform.smoothscale_by(self.right_owl, 0.35)
        self.owl1 = self.small_owl
        self.owl2 = pygame.transform.flip(self.owl1, True, False)
        self.door = self.pic(69)
        self.ash = self.pic(70, (80, 80))
        # self.space_frame_prev = pygame.transform.smoothscale(self.space_frame, (32, 32))
        # self.digits = self.pic(49, (30, 240))
        # for x in range(18):
        #     xpos = x * 76 + 70
        #     pygame.draw.circle(self.periodic, (0, 0, 0), (xpos, 400), 5)
        # for y in range(10):
        #     ypos = y * 76 + 125
        #     pygame.draw.circle(self.periodic, (0, 0, 0), (400, ypos), 5)
        end_bg =  pygame.Surface((720, 810))
        write("The End", (360, 405), (250, 250, 250), 90, end_bg)
        for i in range(1, 9):
            img = pygame.image.load(f"Pictures/tv_pics/PictureTV{i}.png")
            img = pygame.transform.smoothscale_by(img, 1/4)
            self.tv_imgs.append(img)
        self.space_clicker = Object(535, 180, pygame.Surface((150, 120)), self, [
            self.wall_bg(),
            Object(360, 360, self.frame_img, self, [
                Object(360, 360, self.space, self, [], 1),
                Object(360, 360, pygame.transform.smoothscale(self.door, (30, 45)), self, [
                    Object(360, 360, self.space, self, [], 1),
                    Object(360, 360, pygame.transform.smoothscale(self.door, (100, 150)), self, [
                        Object(360, 360, self.space, self, [], 1),
                        Object(360, 360, pygame.transform.smoothscale(self.door, (460, 690)), self, [
                            Object(360, 405, end_bg, self, [], 1)
                        ], 0, "end")
                    ])
                ])
            ]),
            Object(360, 355, pygame.transform.smoothscale(self.space.subsurface(pygame.Rect(0, 0, 1995, 1995)), (346, 364)), self, [])
        ], 0, "space_clicker")
        # Root
        self.root = Object(0, 0, pygame.Surface((0, 0)), self, [
            # Background
            Object(360, 360, self.room_bg, self, [], 1),
            #Object(360, 360, self.parrot, self, [], 1),
            # Frames
            # Orange Bird
            Object(540, 210, self.small_frame, self, [
                self.wall_bg(),
                Object(360, 360, self.frame_img, self, [], 1),
                #Object(360, 355, self.small_orange_bird, self, [], 1)
            ], 0, "orangebird"),
            orange_prev := Object(540, 210, pygame.transform.smoothscale(self.small_orange_bird, (32, 32)), self, [], 1),
            # Parrot
            Object(500, 150, self.small_frame, self, [
                self.wall_bg(),
                Object(360, 360, self.frame_img, self, [], 1),
                Object(360, 355, self.parrot, self, [], 1),
                Object(278, 265, pygame.Surface((10, 10)), self, [
                    Object(360, 360, pygame.Surface((720, 720)), self, [], 1),
                    Object(360, 360, self.small_frame, self, [
                        Object(360, 360, pygame.Surface((720, 720)), self, [], 1),
                        Object(360, 360, self.frame_img, self, [], 1),
                        Object(360, 360, self.knight, self, [], 1)
                    ], 0),
                    Object(360, 360, pygame.transform.smoothscale(self.knight, (32, 32)), self, [], 1)
                ], 0, "parrot_eye")
            ]),
            # Rook
            Object(580, 150, self.small_frame, self, [
                self.wall_bg(),
                Object(360, 360, self.frame_img, self, [], 1),
                Object(360, 355, self.rook, self, [], 1)
            ], 0),
            rook_prev := Object(580, 150, pygame.transform.smoothscale(self.rook, (32, 32)), self, [], 1),
            parrot_prev := Object(500, 150, pygame.transform.smoothscale(self.parrot, (32, 32)), self, [], 1),
            # Front Cabinet
            Object(560, 550, pygame.image.load('Pictures/Picture3.png').convert_alpha(), self, [
                # Wall BG
                self.wall_bg(),
                # Cabinet
                Cabinet(360, 360, pygame.image.load('Pictures/Picture1.png').convert_alpha(), pygame.image.load('Pictures/Picture2.png').convert_alpha(), self, [
                ])
            ]),
            # Bulletin
            Object(160, 400, pygame.transform.smoothscale(self.bulletin, (170, 170)), self, [
                self.wall_bg(),
                Object(360, 360, self.bulletin, self, [], 1),
                Object(460, 320, self.paperimg, self, [], 1),
                # Object(300, 200, pygame.transform.smoothscale(self.clue(1), (300, 200)), self, []),
                Object(460, 225, pygame.Surface((30, 30)), self, [], 0, "paper_pin"),
                # Object(460, 345, self.croppedpaper, self, [], 1)
                Object(250, 360, pygame.Surface((220, 400)), self, [], 0, "clue_placer")
            ]),
            # Shelf
            Object(160, 220, self.shelf, self, [], 1),
            Object(160, 197, pygame.image.load("Pictures/Picture17.png"), self, [
                self.wall_bg(),
                Object(360, 540, self.shelf_bg, self, [], 1),
                Object(360, 360, pygame.image.load("Pictures/Picture18.png"), self, [], 1),
                Object(390, 320, pygame.Surface((50, 70)), self, [
                    Object(360, 360, self.jar_bg, self, [], 1),
                    Object(390, 290, pygame.Surface((20, 30)), self, [
                        Object(360, 360, pygame.Surface((720, 720)), self, [], 1),
                        Object(360, 360, self.small_frame, self, [
                            Object(360, 360, pygame.Surface((720, 720)), self, [], 1),
                            Object(360, 360, self.frame_img, self, [], 1),
                            Object(360, 360, self.queen, self, [], 1)
                        ], 0),
                        Object(360, 360, pygame.transform.smoothscale(self.queen, (32, 32)), self, [], 1)
                    ], 0)
                ], 0, "top_firefly")
            ], 0, "jar"),
            # Table
            Object(360, 550, self.pic(23), self, [
                self.wall_bg(),
                Object(360, 360, self.pic(33), self, [], 1),
                Object(210, 360, self.pic(56), self, [], 0, "watch")
            ], 0, "table")
        ])
        # Room 2
        self.r2 = Object(0, 0, pygame.Surface((0, 0)), self, [
            Object(360, 360, self.room_bg, self, [], 1),
            Object(360, 540, self.pic(27), self, [
                Object(360, 360, self.pic(28), self, [], 1),
                ChessBoard(360, 360, pygame.Surface((640, 640)), self, [])
            ]),
            Object(150, 540, self.pic(29), self, [
                Object(360, 360, self.dark_bg, self, [], 1),
                Object(360, 360, pygame.transform.smoothscale(self.pic(31), (700, 529)), self, [], 1)
            ]),
            Object(140, 200, self.shelf, self, [
                Object(360, 360, self.pic(33), self, [], 1),
                Book(360, 360, [self.pic(34), pygame.transform.smoothscale(self.pic(35), (600, 900)), pygame.transform.smoothscale(self.pic(36), (600, 900))], self, [])
            ]),
            Object(140, 195, self.pic(32), self, [], 1),
            Object(360, 160, pygame.transform.smoothscale(self.pic(37), (140, 56)), self, []),
            flag_prev := Object(360, 220, pygame.transform.scale(self.kiribati1, (180, 90)), self, [
                self.wall_bg(),
                Object(360, 360, pygame.transform.scale(self.kiribati1, (700, 350)), self, [], 0, "flag")
            ]),
            Object(570, 550, pygame.transform.smoothscale(self.pic(40), (150, 150)), self, [
                self.wall_bg(),
                #Object(360, 360, self.mathvault(), self, [])
                Vault(360, 360, self.mathvault(), pygame.transform.smoothscale(self.pic(41), (700, 700)), self, [])
            ], 0, "mathvault"),
            Object(560, 200, self.shelf, self, [
                self.wall_bg(),
                Object(360, 540, self.shelf_bg, self, []),
                Object(360, 350, self.eggs[0], self, [], 0, "egg")
            ]),
            Object(560, 178, pygame.transform.smoothscale(self.egg(1), (40, 60)), self, [], 1)
        ])
        # Room 3
        self.r3 = Object(0, 0, pygame.Surface((0, 0)), self, [
            Object(360, 360, self.room_bg, self, [], 1),
            Object(560, 180, self.shelf, self, [
                self.wall_bg(),
                Object(360, 540, self.shelf_bg, self, []),
                Object(360, 340, pygame.transform.smoothscale(self.pic(44), (350, 350)), self, [])
                # Vase(360, 310, self.pic(43), self, [])
            ], 0, "vase_shelf"),
            Object(560, 150, pygame.transform.smoothscale(self.vase, (70, 70)), self, []),
            Object(140, 180, self.shelf, self, [
                self.wall_bg(),
                Object(360, 540, self.shelf_bg, self, [], 1),
                Object(360, 310, pygame.transform.smoothscale(self.pic(46), (700, 700)), self, [], 1),
                Object(555, 305, pygame.Surface((110, 290)), self, [], 0, "buttons")
            ], 0, "tv_shelf"),
            Object(140, 155, self.pic(45), self, []),
            #Object(360, 360, pygame.transform.smoothscale(self.pic(47), (700, 376)), self, []),
            Object(360, 120, pygame.transform.smoothscale(self.periodic.convert_alpha(), (75, 50)), self, [
                self.wall_bg()
            ], 0, "periodic"),
            Object(570, 550, pygame.transform.smoothscale(self.pic(48), (150, 150)), self, [
                self.wall_bg(),
                CodeVault(360, 360, pygame.transform.smoothscale(self.pic(48), (700, 700)), pygame.transform.smoothscale(self.pic(41), (700, 700)), self, []),
            ], 0, "codevault"),
            sky := Object(360, 315, pygame.Surface((140, 130)), self, [
                self.wall_bg(),
                Object(360, 330, pygame.Surface((400, 360)), self, [], 1, "zsky"),
                Object(360, 365, self.pic(53), self, [], 1),
                Object(360, 360, self.pic(52), self, [], 1),
            ], 0, "sky"),
            Object(360, 330, self.pic(51), self, [], 1),
            Object(360, 330, self.pic(50), self, [], 1),
            Object(150, 550, self.pic(58, (140, 140)), self, [
                self.wall_bg(),
                Furnace(350, 350, self.pic(58), self.pic(64), self, [])
            ])
        ])
        self.owl_room = Object(0, 0, pygame.Surface((0, 0)), self, [
            Object(360, 360, pygame.Surface((720, 720)), self, [], 1),
            Object(360, 600, self.owl1, self, [
                Object(360, 360, pygame.Surface((720, 720)), self, [], 1),
                Object(360, 380, self.right_owl, self, [], 0, "owl")
            ])
        ])
        self.time = 0
        self.sky = sky
        self.orange_prev, self.rook_prev, self.parrot_prev = orange_prev, rook_prev, parrot_prev
        self.flag_prev = flag_prev
        self.rooms = [self.root, self.r2, self.r3]
        self.room = 0
        self.root.gen_id([], 0)
        self.lens = self.root
        # self.progress = set(["wohoo"])
        self.progress = set()
        self.game_over = 0
        self.transition()
        for room in self.rooms:
            room.is_room = 1
        self.owl_room.is_room = 1
        
    def holding(self):
        if self.i_sel is not None:
            return self.inventory[self.i_sel]
        return None
    def lose_item(self):
        self.inventory[self.i_sel] = None
        self.i_sel = None
    def egg(self, num):
        return pygame.image.load(f"Pictures/eggs/PictureE{num}.png")
    def clue(self, num):
        return pygame.image.load(f"Pictures/clues/PictureC{num}.png")
    def mathvault(self):
        surf = pygame.transform.smoothscale(self.pic(40), (700, 700))
        write("+", (270, 215), (150, 150, 150), 50, surf)
        write("-", (270, 325), (150, 150, 150), 50, surf)
        write("x", (270, 435), (150, 150, 150), 40, surf)
        for y in (215, 325, 435):
            write("=", (405, y), (150, 150, 150), 40, surf)
        return surf
    def make_txt(self, txt):
        for text in texts:
            text.kill()
        Text(txt, self.font)
    def collect(self, item):
        for i, it in enumerate(self.inventory):
            if not it:
                self.inventory[i] = item
                break
        # self.inventory.append(item)
        self.make_txt(item.name)
    def pic(self, num, scale=None):
        if scale:
            return pygame.transform.smoothscale(pygame.image.load(f"Pictures/Picture{num}.png"), scale)
        return pygame.image.load(f"Pictures/Picture{num}.png")
    def wall_bg(self):
        return Object(360, 360, self.wallbg, self, [], 1)
    async def run(self):
        while self.running:
            all_sprites.update()
            self.draw_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    #print(mouse)
                    mx, my = mouse
                    if my < 720:
                        in_per = self.lens.desc == "periodic"
                        if not in_per and mx < 60:
                            Fade(lambda: self.switch_room(-1))
                        elif not in_per and mx > 660:
                            Fade(lambda: self.switch_room(1))
                        elif my > 680:
                            if not self.lens.is_room:
                                Fade(self.zoom_out)
                        else:
                            click_found = 0
                            for spr in specials:
                                if spr.rect.collidepoint(mouse):
                                    if hasattr(spr, "onclick"):
                                        spr.onclick()
                                        click_found = 1
                                        break
                            if not click_found:
                                for spr in game_objs:
                                    if spr.visible and not spr.is_bg and spr.rect.collidepoint(mouse):
                                        # #print(spr, spr.id)
                                        spr.onclick()
                                        break
                    else:
                        index = mouse[0] // 90
                        if len(self.inventory) > index:
                            if self.inventory[index]:
                                if self.i_sel == index:
                                    self.i_sel = None
                                else:
                                    self.i_sel = index
                                    self.make_txt(self.inventory[index].name)
                            elif self.i_sel is not None:
                                self.inventory[index] = self.inventory[self.i_sel]
                                self.lose_item()
                elif event.type == pygame.MOUSEBUTTONUP:
                    for periodic in periodics:
                        periodic.release()
                    for mathtile in mathtiles:
                        mathtile.release()
                    for vase in vases:
                        vase.mousedown = None
                    for hand in hands:
                        hand.mousedown = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_DOWN, pygame.K_s):
                        #print('tn')
                        if not self.lens.is_room:
                            Fade(self.zoom_out)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        Fade(lambda: self.switch_room(1))
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        Fade(lambda: self.switch_room(-1))
                    elif event.key == pygame.K_t:
                        self.time += 0.5
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)
    def switch_room(self, offset):
        if  "flag_complete" in self.progress and "clue4" not in self.progress:
            if offset == self.next_swipe:
                self.frigate_num += 1
                self.next_swipe = random.choice([-1, 1])
                #print(self.frigate_num)
            else:
                self.frigate_num = 0
            if self.frigate_num >= 16:
                self.frigate_num = 0
                self.lens = self.owl_room
                self.transition()
                #print(all_sprites)
                return
        self.room = (self.room + offset) % len(self.rooms)
        self.lens = self.rooms[self.room]
        self.transition()
        #print(all_sprites)
        if "flag_complete" in self.progress and "clue4" not in self.progress:
            #print('genbird')
            if self.frigate_num < 5:
                if self.next_swipe == 1:
                    Frigate(self.frigate1, 1)
                elif self.next_swipe == -1:
                    Frigate(self.frigate2, -1)
            else:
                Owl(self.owl1 if self.next_swipe == 1 else self.owl2, [100, 390, 280][self.room])
        if self.frigate_num > 9:
            Gloom((self.frigate_num - 9) * 40)
    def zoom_out(self):
        self.lens = self.lens.parent
        self.transition()
        self.lens.on_entry()
    def transition(self):
        for spr in specials:
            spr.kill()
        for spr in game_objs:
            spr.visible = 0
            spr.reset()
        for spr in self.lens.children:
            spr.appear()
    def draw_screen(self, screen):
        screen.fill((200, 200, 200))
        for spr in game_objs:
            spr.draw()
        specials.draw(screen)
        texts.draw(screen)
        winfades.draw(screen)
        fades.draw(screen)
        if not self.game_over:
            pygame.draw.rect(screen, (0, 25, 0), pygame.Rect(0, 720, 720, 100))
            for i in range(8):
                col = (0, 50, 0) if i != self.i_sel else (0, 75, 0)
                pygame.draw.rect(screen, col, pygame.Rect(i * 90 + 5, 725, 80, 80), border_radius=5)
                if len(self.inventory) > i and self.inventory[i]:
                    self.inventory[i].draw(i * 90 + 45, 765)

all_sprites = pygame.sprite.LayeredUpdates()
specials = pygame.sprite.Group()
game_objs = pygame.sprite.Group()
pictiles = pygame.sprite.Group()
fades = pygame.sprite.Group()
texts = pygame.sprite.Group()
mathtiles = pygame.sprite.Group()
mathslots = pygame.sprite.Group()
vases = pygame.sprite.Group()
winfades = pygame.sprite.Group()
tv_screens = pygame.sprite.Group()
periodics = pygame.sprite.Group()
codenums = pygame.sprite.Group()
hands = pygame.sprite.Group()

def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))

def main():
    asyncio.run(Game().run())

main()
