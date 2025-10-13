import pygame, sys, time, math, random, asyncio

from flagnamelist import flagnames

pygame.init()

HALF = 400

screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("Cognition")

# flag_img = pygame.image.load("Collection-national-flags.png")
# flag_img = flag_img.convert_alpha()
# flag_img = pygame.transform.smoothscale(flag_img, (6000, 2600))
# flag_img = pygame.transform.scale()

with open("valid_words.txt") as file:
    valid_words = set(line.strip() for line in file)

with open("wordle_answers.txt") as file:
    valid_answers = [line.strip() for line in file]

# with zipfile.ZipFile("w2560.zip", "r") as zip_file:
#     flag_images = [image for image in zip_file.namelist()]
#     with zip_file.open(random.choice(flag_images)) as ad:
#         flagimg = pygame.image.load(ad).convert_alpha()
#         iwidth, iheight = flagimg.get_size()
#         new_width = 400
#         flagimg = pygame.transform.smoothscale(flagimg, (new_width, iheight * new_width / iwidth))

flag_images = ['ad.png', 'ae.png', 'af.png', 'ag.png', 'al.png', 'am.png', 'ao.png',
'ar.png', 'at.png', 'au.png', 'az.png', 'ba.png', 'bb.png', 'bd.png',
'be.png', 'bf.png', 'bg.png', 'bh.png', 'bi.png', 'bj.png', 'bo.png',
'br.png', 'bs.png', 'bt.png', 'bw.png', 'by.png', 'bz.png', 'ca.png',
'cd.png', 'cf.png', 'cg.png', 'ch.png', 'ci.png', 'cl.png', 'cm.png',
'cn.png', 'co.png', 'cr.png', 'cu.png', 'cv.png', 'cy.png', 'cz.png',
'de.png', 'dj.png', 'dk.png', 'dm.png', 'do.png', 'dz.png', 'ec.png',
'ee.png', 'eg.png', 'er.png', 'es.png', 'et.png', 'fi.png', 'fj.png',
'fr.png', 'ga.png', 'gb.png', 'gd.png', 'ge.png', 'gh.png', 'gm.png',
'gn.png', 'gq.png', 'gr.png', 'gt.png', 'gw.png', 'gy.png', 'hn.png',
'hr.png', 'ht.png', 'hu.png', 'id.png', 'ie.png', 'il.png', 'in.png',
'iq.png', 'ir.png', 'is.png', 'it.png', 'jm.png', 'jo.png', 'jp.png',
'ke.png', 'kg.png', 'kh.png', 'ki.png', 'km.png', 'kn.png', 'kp.png',
'kr.png', 'kw.png', 'kz.png', 'la.png', 'lb.png', 'lc.png', 'li.png',
'lk.png', 'lr.png', 'ls.png', 'lt.png', 'lu.png', 'lv.png', 'ly.png',
'ma.png', 'mc.png', 'md.png', 'me.png', 'mg.png', 'mh.png', 'mk.png',
'ml.png', 'mm.png', 'mn.png', 'mr.png', 'mt.png', 'mu.png', 'mv.png',
'mw.png', 'mx.png', 'my.png', 'mz.png', 'na.png', 'ne.png', 'ng.png',
'ni.png', 'nl.png', 'no.png', 'np.png', 'nr.png', 'nz.png', 'om.png',
'pa.png', 'pe.png', 'pg.png', 'ph.png', 'pk.png', 'pl.png', 'pt.png',
'pw.png', 'py.png', 'qa.png', 'ro.png', 'rs.png', 'ru.png', 'rw.png',
'sa.png', 'sb.png', 'sc.png', 'sd.png', 'se.png', 'sg.png', 'si.png',
'sk.png', 'sl.png', 'sm.png', 'sn.png', 'so.png', 'sr.png', 'ss.png',
'st.png', 'sv.png', 'sy.png', 'sz.png', 'td.png', 'tg.png', 'th.png',
'tj.png', 'tl.png', 'tm.png', 'tn.png', 'to.png', 'tr.png', 'tt.png',
'tv.png', 'tz.png', 'ua.png', 'ug.png', 'us.png', 'uy.png', 'uz.png',
'va.png', 'vc.png', 've.png', 'vn.png', 'vu.png', 'ws.png', 'ye.png',
'za.png', 'zm.png', 'zw.png'
]

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, wid, height, text, col, dcol, func):
        self.groups = buttons, all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pygame.Surface([wid, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.func = func
        self.wid = wid
        self.height = height
        self.txt = text
        self.col = col
        self.dcol = dcol
        self.paint(col)
    def click(self):
        self.func()
    def paint(self, col):
        self.image.fill((18, 18, 18))
        pygame.draw.rect(self.image, col, pygame.Rect(5, 5, self.wid - 10, self.height - 10), border_radius=15)
        pygame.draw.rect(self.image, (18, 18, 18), pygame.Rect(10, 10, self.wid - 20, self.height - 20), border_radius=10)
        write(self.txt(), (self.wid / 2, self.height / 2), col, 50, self.image)
    def hovering(self, mx, my):
        return self.rect.x < mx < self.rect.right and self.rect.y < my < self.rect.bottom
    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.paint(self.col if not self.hovering(mx, my) else self.dcol)

class Fade(pygame.sprite.Sprite):
    def __init__(self, col):
        self.groups = all_sprites
        self._layer = 2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = 0
        self.y = 0
        self.image = pygame.Surface([800, 800])
        self.image.fill(col)
        self.alpha = 150
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.col = col
        self.image.set_alpha(self.alpha)
    def update(self):
        self.alpha -= 5
        if self.alpha > 0:
            self.image.set_alpha(self.alpha)
        else:
            self.kill()

class FinalFade(pygame.sprite.Sprite):
    def __init__(self, col, game):
        self.groups = all_sprites
        self._layer = 2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = 0
        self.y = 0
        self.image = pygame.Surface([800, 800])
        self.image.fill(col)
        self.alpha = 0
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.game = game
        self.stage = 0
        self.image.set_alpha(self.alpha)
    def update(self):
        if self.stage == 0:
            self.alpha += 2
            if self.alpha >= 255:
                self.stage = 1
                # self.game.reset()
                self.game.menu()
        else:
            self.alpha -= 5
            if self.alpha <= 0:
                self.kill()
        self.image.set_alpha(self.alpha)
        print(self)

class Lvl:
    def __init__(self, game):
        self.game = game
        self.max_time = self.max_times[self.game.stage - 1]
    def paint(self):
        self.draw()
        if self.game.active:
            elapsed = time.time() - self.start_time
            if elapsed > self.max_time:
                self.game.progress(0)
                return
            write(self.max_time - math.floor(elapsed), (50, 50), (250, 250, 250), 50, screen)
    def gen(self):
        self.start_time = time.time()

class FlagLvl(Lvl):
    def __init__(self, game):
        self.max_times = [15, 12, 6, 5]
        super().__init__(game)
        self.type = "flag"
        self.typed = ""
        self.ansnum = random.randint(0, len(flag_images) - 1)
        self.ans = flagnames[self.ansnum].lower()
        # with zipfile.ZipFile("w2560.zip", "r") as zip_file:
        #     with zip_file.open(flag_images[self.ansnum]) as ad:
        flagimg = pygame.image.load("flags/" + flag_images[self.ansnum]).convert_alpha()
        iwidth, iheight = flagimg.get_size()
        new_width = 400
        self.width = new_width
        self.height = iheight * new_width / iwidth
        self.image = pygame.transform.smoothscale(flagimg, (new_width, self.height))
    def resp(self, unicode):
        if len(self.typed) < 35:
            self.typed += unicode
        if self.typed == self.ans:
            self.game.progress()
    def draw(self):
        write("What country flag is this?", (400, 180), (250, 250, 250), 40, screen)
        # x, y = self.coords
        # screen.blit(flag_img, (200, 300), (x * 400, y * 200, 400, 200))
        write(self.typed.upper(), (400, 600), (250, 250, 250), 50, screen)
        screen.blit(self.image, (400 - self.width / 2, 400 - self.height / 2))

class MathLvl(Lvl):
    def __init__(self, game):
        self.max_times = [20, 13, 9, 6]
        super().__init__(game)
        self.type = "math"
        a = random.randint(11, 99)
        b = random.randint(2, 9)
        expression = f"{a} x {b}"
        ans = a * b
        self.expression = expression + " = ?"
        self.ans = str(ans)
        self.typed = ""
    def resp(self, unicode):
        if len(self.typed) < 5:
            self.typed += unicode
        if self.typed == self.ans:
            self.game.progress()
    def draw(self):
        write(self.expression, (400, 200), (250, 250, 250), 60, screen)
        write(self.typed, (400, 400), (250, 250, 250), 60, screen)

class MemTile(pygame.sprite.Sprite):
    def __init__(self, x, y, num, tilesize, level):
        self.groups = all_sprites
        super().__init__(self.groups)
        self.image = pygame.Surface((tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.num = num
        self.level = level
        self.tilesize = tilesize
        self.paint()
    def resp(self):
        if self.level.next == self.num:
            self.level.next += 1
            self.kill()
            if self.level.next >= 10:
                self.level.game.progress()
        else:
            self.level.game.progress(0)
    def update(self):
        self.paint()
    def paint(self):
        self.image.fill((18, 18, 18))
        pygame.draw.rect(self.image, (250, 250, 250), pygame.Rect(10, 10, self.tilesize - 20, self.tilesize - 20), border_radius=10)
        pygame.draw.rect(self.image, (18, 18, 18), pygame.Rect(15, 15, self.tilesize - 30, self.tilesize - 30), border_radius=10)
        if self.level.next == 1:
            write(self.num, (self.tilesize / 2, self.tilesize / 2), (250, 250, 250), 70, self.image)

class MemLvl(Lvl):
    def __init__(self, game):
        self.max_times = [20, 13, 10, 6]
        super().__init__(game)
        self.type = "mem"
        self.next = 1
        code = [i for i in range(1, 10)]
        random.shuffle(code)
        tilesize = 150
        for i in range(3):
            for j in range(3):
                MemTile(400 - tilesize * 3 / 2 + tilesize * j, 400 - tilesize * 3 / 2 + tilesize * i, code[i * 3 + j], tilesize, self)
    def resp(self, unicode):
        if len(self.typed) < 5:
            self.typed += unicode
        if self.typed == self.ans:
            self.game.progress()
    def draw(self):
        pass

class Wordle(Lvl):
    def __init__(self, game):
        self.max_times = [30, 24, 18, 12]
        super().__init__(game)
        self.type = "wordle"
        self.word = random.choice(valid_answers)
        self.rows = [["" for _ in range(5)] for _ in range(6)]
        self.cols = [[0 for _ in range(5)] for _ in range(6)]
        self.typing_index = 0
        self.current_row = 0
    def resp(self, unicode):
        if self.current_row < 6 and self.typing_index < 5:
            self.rows[self.current_row][self.typing_index] = unicode
            self.typing_index += 1
    def enter(self):
        if self.current_row > 5:
            return
        if self.rows[self.current_row][-1] != "":
            guess = list(self.rows[self.current_row])
            strguess = "".join(guess)
            if strguess not in valid_words:
                return
            word = list(self.word)
            if guess == word:
                self.game.progress()
                return
            colors = [0 for _ in range(5)]
            for i in range(5):
                if guess[i] == word[i]:
                    colors[i] = 2
                    guess[i] = 0
                    word[i] = ""
            for i in range(5):
                if guess[i] != 0:
                    if guess[i] in word:
                        word[word.index(guess[i])] = ""
                        colors[i] = 1
                    else:
                        colors[i] = -1
            self.cols[self.current_row] = colors
            self.current_row += 1
            self.typing_index = 0
    def draw(self):
        tilesize = 80
        for i, row in enumerate(self.rows):
            for j, letter in enumerate(row):
                x = (tilesize + 10) * j + 400 - (((tilesize + 10) * 5 - 10) / 2)
                y = (tilesize + 10) * i + 400 - (((tilesize + 10) * 6 - 10) / 2)
                colindex = self.cols[i][j]
                col  = [(50, 50, 50), (180, 180, 0), (0, 150, 0), (35, 35, 35)][colindex]
                bordercol = [(50, 50, 50), (160, 160, 0), (0, 130, 0), (45, 45, 45)][colindex]
                pygame.draw.rect(screen, bordercol, pygame.Rect(x, y, tilesize, tilesize), border_radius=10)
                pygame.draw.rect(screen, col, pygame.Rect(x + 4, y + 4, tilesize - 8, tilesize - 8), border_radius=10)
                write(letter.upper(), (x + tilesize / 2, y + tilesize / 2), (250, 250, 250), 50, screen)

class Game:
    def __init__(self):
        random.seed(time.time())
        self.running = True
        self.clock = pygame.time.Clock()
        # self.levels = [
        #     FlagLvl((11, 6), "france", self),
        #     MathLvl("4 * (5 - 2) + 12", 24, self),
        #     Wordle("steam", self),
        #     FlagLvl((7, 4), "greece", self),
        #     MathLvl("24 * 5 / 8", 15, self),
        #     Wordle("denim", self),
        #     FlagLvl((4, 2), "chad", self),
        #     MathLvl("40% of 70", 28, self),
        #     Wordle("batch", self)
        # ]
        self.alpha = "abcdefghijklmnopqrstuvwxyz -"
        self.totalgames = 4
        self.bar_colors = [(0, 150, 0), (170, 160, 0), (200, 150, 0), (100, 0, 150)]
        self.mode = 0
        # self.reset()
        self.diffs = ["EASY", "MEDIUM", "HARD", "IMPOSSIBLE"]
        self.lengths = ["DEFAULT", "LONG", "SHORT"]
        self.diff = 0
        self.length = 0
        self.menu()
        # Button(HALF, HALF + 170, 420, 144, f"DIFFICULTY", (150, 120, 0), (200, 180, 0), None)
    def menu(self):
        for spr in all_sprites:
            if not isinstance(spr, FinalFade):
                spr.kill()
        s = 250
        self.mode = 0
        Button(250, s, 300, 110, lambda: "PLAY", (0, 120, 170), (0, 180, 200), self.reset)
        Button(250, s + 125, 300, 110, lambda: self.diffs[self.diff], (0, 120, 0), (0, 170, 0), self.toggle_diff)
        Button(250, s + 250, 300, 110, lambda: self.lengths[self.length], (150, 120, 0), (200, 180, 0), self.toggle_len)
    def toggle_diff(self):
        self.diff = (self.diff + 1) % len(self.diffs)
    def toggle_len(self):
        self.length = (self.length + 1) % len(self.lengths)
    def reset(self):
        for spr in all_sprites:
            if not isinstance(spr, FinalFade):
                spr.kill()
        self.stage = self.diff + 1
        self.score = 0
        self.points_to_win = [20, 30, 10][self.length]
        self.levelnum = 0
        self.level = FlagLvl(self)
        self.level.gen()
        # self.totalgames = 1
        self.order = [i for i in range(self.totalgames)] * math.ceil(100 / self.totalgames)
        random.shuffle(self.order)
        self.orderindex = 0
        self.backups = 1
        self.backup_scale = 0
        self.backup_colored = 0
        self.backup_req = 20
        self.score_colored = 0
        self.active = 1
        self.mode = 1
    async def run(self):
        while self.running:
            # print(all_sprites)
            all_sprites.update()
            self.draw_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if self.level.type in ("flag", "math"):
                            if len(self.level.typed) > 0:
                                self.level.typed = self.level.typed [:-1]
                        elif self.level.type == "wordle":
                            level = self.level
                            row = level.rows[level.current_row]
                            if row[0] != "":
                                row[level.typing_index - 1] = ""
                                level.typing_index -= 1
                    elif event.key == pygame.K_RETURN:
                        if not self.mode:
                            self.reset()
                        else:
                            if self.level.type == "wordle":
                                self.level.enter()
                    elif event.key == pygame.K_ESCAPE:
                        self.menu()
                    else:
                        unicode = event.unicode.lower()
                        if unicode != "":
                            if unicode in self.alpha:
                                if self.level.type in ("flag", "wordle"):
                                    self.level.resp(unicode)
                            elif unicode in "0123456789":
                                if self.level.type == "math":
                                    self.level.resp(unicode)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    for spr in all_sprites:
                        if spr.rect.collidepoint(mouse):
                            if isinstance(spr, MemTile):
                                spr.resp()
                            elif isinstance(spr, Button):
                                spr.click()
            if self.mode and self.backup_colored < self.backup_scale:
                self.backup_colored += 0.1 * (self.backup_scale - self.backup_colored)
                if self.backup_colored >= self.backup_req:
                    self.backup_colored -= self.backup_req
                    self.backup_scale -= self.backup_req
                    self.backups += 1
                if self.score_colored < self.score:
                    self.score_colored += 0.05 * (self.score - self.score_colored)
                    # print(self.score_colored)
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)
    def draw_screen(self, screen):
        screen.fill((20, 20, 20))
        if self.mode == 1:
            self.level.paint()
            pygame.draw.rect(screen, (80, 80, 80), pygame.Rect(200, 90, 400, 15))
            pygame.draw.rect(screen, self.bar_colors[self.stage - 1], pygame.Rect(200, 90, self.score_colored * (400 / self.points_to_win), 15))
            write(self.score, (400, 70), (250, 250, 250), 50, screen)
            pygame.draw.rect(screen, (80, 80, 80), pygame.Rect(200, 720, 400, 10))
            pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(200, 720, self.backup_colored / self.backup_req * 400, 10))
            write(self.backups, (400, 725), (250, 250, 250), 50, screen)
        else:
            # write("Cognition", (400, 200), (255, 255, 255), 80, screen)
            write("Cognition", (HALF, HALF / 2 - 80), (250, 250, 250), 80, screen)
        all_sprites.draw(screen)
    def progress(self, won=1):
        if not self.active:
            return
        self.score += won
        if self.score >= self.points_to_win:
            self.active = 0
            FinalFade((200, 180, 0), self)
            return
        # if self.score >= 25 * self.stage:
        #     self.score_colored = 0
        #     self.stage += 1
        self.orderindex += 1
        for spr in all_sprites:
            spr.kill()
        if won:
            Fade((0, 250, 0))
            self.backup_scale += self.level.max_time - (time.time() - self.level.start_time)
        else:
            if self.backups > 0:
                Fade((250, 0, 0))
                self.backups -= 1
            else:
                self.active = 0
                FinalFade((0, 0, 0), self)
                return
        # self.levelnum += 1
        # if self.levelnum >= len(self.levels):
        #     self.levels.append(FlagLvl(None, None, self))
        # self.level = self.levels[self.levelnum]
        if self.orderindex >= len(self.order):
            self.order = [i for i in range(self.totalgames)] * math.ceil((100 - self.score) / self.totalgames)
            self.orderindex = 0
        match self.order[self.orderindex] + 1:
            case 1:
                self.level = FlagLvl(self)
            case 2:
                self.level = Wordle(self)
            case 3:
                self.level = MathLvl(self)
            case 4:
                self.level = MemLvl(self)
        self.level.gen()

all_sprites = pygame.sprite.LayeredUpdates()
levels = pygame.sprite.Group()
buttons = pygame.sprite.Group()

def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))

def main():
    asyncio.run(Game().run())

main()
