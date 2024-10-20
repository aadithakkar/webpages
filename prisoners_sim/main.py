import pygame
import sys
import random
import asyncio


pygame.init()
screen = pygame.display.set_mode([600, 800])
pygame.display.set_caption("Prisoner's Dilemma")
clock = pygame.time.Clock()


variability = 0
COLORS = [(200, 0, 0),
          (0, 200, 0),
          (0, 0, 200),
          (180, 180, 0),
          (0, 180, 180),
          (180, 0, 180),
          (100, 100, 100),
          (200, 0, 100),
          (200, 100, 0),
          (0, 100, 200)]


running = True
auto = 0
speed = 1
fps = 30
misc = 1
menu = 1
menu_list_interval = 50
selected = 0


def simpostor(mem):
    if len(mem) < 1:
        return 0
    if mem[0] == 1:
        return 0
    if len(mem) == 1:
        return 1
    if mem[1] == 0:
        return 0
    if len(mem) == 2:
        return 0
    if mem[2] == 0:
        if 0 in mem[3:]:
            return 0
        return 1
    return 0


def ssensor(mem):
    if len(mem) < 3:
        if len(mem) < 1:
            return 1
        return mem[-1]
    f3 = mem[:3]
    if 0 not in f3:
        return mem[-1]
    elif 0 not in mem[1:3]:
        return mem[-1]
    return 0


def srec(mem):
    if len(mem) < 1:
        return 0
    if mem[0] == 1:
        return 0
    if len(mem) == 1:
        return 1
    if mem[0] == 0 and mem[1] == 1 and 0 not in mem[1:]:
        return 1
    return 0


def stwotft(mem):
    if len(mem) < 1:
        return 1
    if mem[-1] == 0:
        return 0
    if len(mem) > 1 and mem[-2] == 0:
        return 0
    return 1


def stf2t(mem):
    if len(mem) < 2:
        return 1
    if mem[-1] == mem[-2] == 0:
        return 0
    return 1


class Strategy:
    def __init__(self, name, func, desc):
        self.name = name
        self.func = func
        self.desc = desc


sucker = Strategy("Sucker", lambda mem: 1, "Always cooperates")
cheat = Strategy("Cheat", lambda mem: 0, "Always defects")
grudger = Strategy("Grudger", lambda mem: 0 if 0 in mem else 1, "Defects only if opponent has ever defected")
tft = Strategy("Tit for Tat", lambda mem: mem[-1] if mem != [] else 1, "Cooperates, then imitates opponent")
sustft = Strategy("Sus TFT", lambda mem: mem[-1] if mem != [] else 0, "Defects, then imitates opponent")
nicealter = Strategy("Alternator", lambda mem: 1 - (len(mem) % 2), "Alternates cooperating and defecting")
tf2t = Strategy("Tit for 2 Tats", lambda mem: stf2t(mem), "Defects for every two opponent defects")
defecttft = Strategy("Defect TFT", lambda mem: 1 if mem == [] else (mem[-1] if len(mem) < 199 else 0), "Tit for Tat, but defects on the last round")
rand = Strategy("Random", lambda mem: random.randint(0, 1), "Randomly cooperates or defects")
provoker = Strategy("Provoker", lambda mem: 0 if random.randint(1, 50) == 1 else 1, "")
twotft = Strategy("2 Tits for Tat", lambda mem: stwotft(mem), "Defects twice for every opponent defect")
didefect = Strategy("Didefect TFT", lambda mem: 1 if mem == [] else (mem[-1] if len(mem) < 198 else 0), "")
recognizer = Strategy("Recognizer", lambda mem: srec(mem), "Defects then cooperates and then cooperates if the opponent plays identically")
dealter = Strategy("De-Alternator", lambda mem: (len(mem) % 2), "Alternates defecting and cooperating")
sensor = Strategy("Sensor", lambda mem: ssensor(mem), "")
impostor = Strategy("Impostor", lambda mem: simpostor(mem), "Defects, cooperates, defects, then cooperates if the opponent plays identically")


# strategies = [cheat, grudger, sucker, sustft, tft, nicealter, defecttft]
# props = [0, 0, 0, 0, 0.5, 0, 0.5]

allstrats = [cheat, sucker, grudger, tft, sustft, nicealter, dealter, tf2t, defecttft, rand, twotft, recognizer, impostor]
allprops = [0 for _ in allstrats]

strategies = [cheat, sucker, grudger]
s_props = [0.1, 0.85, 0.05]


# s_props = [(1/len(strategies)) for _ in strategies]


props = list(s_props)
pts = [0 for _ in range(len(strategies))]
newprops = [0 for _ in range(len(strategies))]


def write(txt, pos, col, size):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    screen.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))


def next_gen():
    global props, pts, newprops
    pts = [0 for _ in range(len(strategies))]
    for i in range(len(strategies)):
        if props[i] > 0.00001:
            for j in range(len(strategies)):
                pts[i] += battle(strategies[i], strategies[j])[0] * props[j]
    for i in range(len(newprops)):
        pts[i] *= props[i]
    for i in range(len(newprops)):
        newprops[i] = pts[i] / sum(pts)
    props = list(newprops)
    # print(strategies)


def draw_board(props, strategies, prof):
    global menu
    screen.fill((200, 200, 200))
    if menu:
        mls = menu_list_interval
        for i in range(len(allstrats)):
            name = allstrats[i].name
            pc = int(round(allprops[i], 2))
            write(name, (150, i * mls + 50), (0, 0, 0), 40)
            write(f"{pc}%", (450, i * mls + 50), (0, 0, 0) if selected != i else (100, 100, 100), 40)
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, 730, 600, 70))
        write(allstrats[selected].desc, (300, 765), (0, 0, 0), 30 if selected < 11 else 20)
        for i in range(10):
            write(i, (60 * i + 30, 710), (0, 0, 0), 40)
        write("SIM", (30, 15), (0, 0, 0), 30)
    else:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(50, 30, 500, 70))
        left = 55
        for i in range(len(props)):
            prop = round(props[i], 3)
            if i == len(props) - 1:
                prop = (545 - left) / 490
            pygame.draw.rect(screen, COLORS[i], pygame.Rect(left, 35, prop * 490, 60))
            left += prop * 490
        for i in range(len(strategies)):
            if i <= 9:
                name = strategies[i].name
                # print(i, props)
                pc = int(round(props[i], 2) * 100)
                write(name, (150, i * 60 + 150), COLORS[i], 50)
                write(f"{pc}%", (400, i * 60 + 150), COLORS[i], 50)
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(580, 5, 15, 15))
        write(f"Average Profit: {round(prof, 1)}", (300, 750), (0, 0, 0), 50)
        write("PR"[auto], (550, 750), (0, 0, 0), 50)
        write(f"{speed}x", (50, 750), (0, 0, 0), 50)
        write(f"{fps}FPS", (50, 780), (0, 0, 0), 25)
        write("MENU", (40, 15), (0, 0, 0), 30)


def battle(s1, s2):
    s1p = 0
    s2p = 0
    s1m = []
    s2m = []
    for _ in range(random.randint(200 - variability, 200 + variability)):
        responses = (s1.func(s1m), s2.func(s2m))
        s1m.append(responses[1] if random.random() < misc else 1 - responses[1])
        s2m.append(responses[0] if random.random() < misc else 1 - responses[0])
        if responses == (0, 0):
            s1p += 1
            s2p += 1
        elif responses == (0, 1):
            s1p += 5
            s2p += 0
        elif responses == (1, 0):
            s1p += 0
            s2p += 5
        elif responses == (1, 1):
            s1p += 3
            s2p += 3
    return (s1p, s2p)


#print(props)


async def main():
    global newprops, allprops, allstrats, props, strategies, selected, auto, menu, pts, speed, fps
    run = True
    while run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu:
                    mouse = pygame.mouse.get_pos()
                    row = (mouse[1] - 25) // 50
                    if 0 <= row < len(allstrats):
                        selected = row
                        allprops[selected] = 0
                    elif row >= len(allstrats):
                        num = (mouse[0] - 15) // 60
                        if 0 <= num <= 9 and allprops[selected] < 100:
                            allprops[selected] = allprops[selected] * 10 + num
                    elif row < 0:
                        if sum(allprops) == 100:
                            strategies = []
                            s_props = []
                            for i in range(len(allstrats)):
                                if allprops[i] > 0:
                                    strategies.append(allstrats[i])
                                    s_props.append(allprops[i] / 100)
                            props = list(s_props)
                            menu = 0
                            pts = [0 for _ in range(len(strategies))]
                            newprops = [0 for _ in range(len(strategies))]
                else:
                    mouse = pygame.mouse.get_pos()
                    if (mouse[1] - 25) // 50 < 0:
                        if mouse[0] < 300:
                            menu = 1
                            auto = 0
                        else:
                            auto = 1 - auto
                    else:
                        next_gen()
                draw_board(props, strategies, sum(pts))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if menu == 1:
                        if sum(allprops) == 100:
                            strategies = []
                            s_props = []
                            for i in range(len(allstrats)):
                                if allprops[i] > 0:
                                    strategies.append(allstrats[i])
                                    s_props.append(allprops[i] / 100)
                            # print(strategies, props)
                            props = list(s_props)
                            menu = 0
                            pts = [0 for _ in range(len(strategies))]
                            newprops = [0 for _ in range(len(strategies))]
                            draw_board(props, strategies, 0)
                    else:
                        menu = 1
                        auto = 0
                        draw_board(props, strategies, 0)
                elif menu == 1:
                    if event.unicode in "1234567890" and event.unicode != "":
                        if allprops[selected] < 100:
                            allprops[selected] = allprops[selected] * 10 + int(event.unicode)
                            draw_board(props, strategies, 0)
                elif event.key == pygame.K_p:
                    auto = 1 - auto
                    draw_board(props, strategies, sum(pts))
                elif event.key == pygame.K_r:
                    props = list(s_props)
                    pts = [0 for _ in range(len(strategies))]
                    newprops = [0 for _ in range(len(strategies))]
                    auto = 0
                    draw_board(props, strategies, 0)
                elif event.key == pygame.K_LEFT:
                    if speed > 1:
                        speed -= 1
                    draw_board(props, strategies, sum(pts))
                elif event.key == pygame.K_RIGHT:
                    if speed < 10:
                        speed += 1
                    draw_board(props, strategies, sum(pts))
                elif event.key == pygame.K_f:
                    fps = 45 - fps
                    draw_board(props, strategies, sum(pts))
        if auto:
            for _ in range(speed):
                next_gen()
            draw_board(props, strategies, sum(pts))
        clock.tick(fps)
        await asyncio.sleep(0)


asyncio.run(main())
