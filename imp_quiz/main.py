import pygame
import sys
import time, random
import asyncio

pygame.init()

screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("The (Almost) Impossible Quiz")

symbols = pygame.transform.smoothscale(pygame.image.load("manasymbols.png"), (300, 60))
#symbols = pygame.transform.smoothscale(pygame.image.load("imp_quiz/manasymbols.png"), (300, 60))
offset = 2

mananum = random.randint(0, 4)
manaprompt = ["It's a Shock you got this far.", "Go to Sleep, you'll never beat this quiz.", "Give up already! I need some Solitude.", "This quiz will Obliterate your patience.", "Stop trying to persevere and Get Lost."][mananum]
manacost = [[0, "R"], [2, "BB"], [3, "WW"], [6, "RR"], [1, "W"]][mananum]
manarecipe = [0, ""]

ops = ["",
       "Barely, No (almost), Yes, Not even close",
       "1, 8, 4, 6",
       "Bottom right, Bottom left, Bottom left, Top right",
       "",
       "Elevator, Eel, Styler, Time Machine",
       "",
       "2042556264, 2405256264, 2042256246, 2405226462",
       "",
       "True, False, , ",
       "5, 7, 1, 2",
       "1, 2, 3, 42",
       "7, 11, 0, 12",
       "13, 14, 42, 10",
       "Risk it!, Continue, , ",
       "Work, Heaven, School, Another Place",
       "90, 1, 3628800, 10",
       "Cooperate, Defect, , ",
       "True, False, , ",
       "",
       "Darwin, Hamilton, Shakespear, None of these",
       "Science, This Quiz, God 2.0, Infinity",
       "+1, -, -, -",
       "Brown, Purple, Black, Green",
       "+2 Lives, +1 Skip, See the future, Continue",
       "1, 2, 3, 4",
       "1001, 101, 1111, 100",
       "x, +, +, +",
       "",
       "0-2, 3-5, 6-8, 9+",
       "True, False, , ",
       "Aww, That's mean., I disagree, Help!!"]

prompts = ["",
           "1) Is this quiz possible?",
           "2) Solve: 8 / 2 (4)",
           "3) The right answer is at the top left",
           "",
           "5) Choose the best word",
           "",
           "7) I hope you remembered.",
           "8) What's the current seconds?",
           "9) If you get this question wrong, you definitely won't lose your progress.",
           "10) Activate all the buttons.",
           "11) Choose a number.",
           "12) Choose another.",
           "13) Now add them!",
           "14) You may gain life... or lose it...",
           "15) There's no place like ___",
           "16) If x = 10, f(x) =",
           "17) Get at least 25 points",
           "All True / False questions in this quiz are False",
           "",
           "20) Who wrote Hamlet?",
           "21) What's greater than God and more evil than the Devil?",
           manaprompt,
           "23) What color is the screen?",
           "24) You've done well. Choose a reward.",
           "25) Click the green button!",
           "26) 110 + 11 = ?",
           "27) Make The rectangle the color Rose",
           "",
           "29) How many times have you lost life so far?",
           "If you get this wrong, you immediately lose.",
           "You got the last question wrong lolol"]

message = random.choice(["Well done, traveler.", "But you died like fifty times.", "Now try it bindfolded.", "Somewhat impressive, actually."])

BLUE = (0, 0, 100)
PINK = (200, 120, 120)
DGRAY = (50, 50, 50)
LGRAY = (200, 200, 200)
ORANGE = (200, 120, 0)
BROWN = (80, 40, 0)
PURPLE = (100, 0, 150)
# colcycle = [BLUE, PINK, DGRAY, LGRAY, ORANGE, BROWN, PURPLE, BLUE, PINK, DGRAY, LGRAY, BROWN, PURPLE, BLUE, PINK, DGRAY, LGRAY, BROWN, PURPLE]

answers = "1-0---2-1--------1-3--2--0----4"


deaths = 0
running = True
clock = pygame.time.Clock()
question = 1
lives = 3
skips = 2
stage = 0
clicks = 0
stime = None
chosen = 0
dial = 10
code = [0, 0, 0]
gb = 0
# opening = 0
conv = [3, 2, 0, 1]
# loop = 0
twodig = ""
mouse = pygame.mouse.get_pos()
mousedown = 0
lastclicked = [0, 0, 0, 0]
times = [5, 7, 1, 2]
activated = [0, 0, 0, 0]
a = 0
b = 0
counter = 0
points = [0, 0]
mem = []
opp = 2
ctime = None
current = random.randint(0, 3)
rgbcolor = [0, 0, 0]
targetcolor = [255, 0, 127.5]
chesspositions = ["-kr--R-rppp--pp--n--pq-----p---p-Q-N--b-------B-------P-R-----K-",
                  "-kr--R-rp-p--pp--np-pq-----p---p-Q----b-------B-------P-R-----K-",
                  "--r--R-rpkB--pp--np-pq-----p---p-Q----b---------------P-R-----K-",
                  "--r--R-rk-B--pp--np-pq-----p---p-Q----b---------------P-------K-",
                  "k-r--R-r--B--pp--Qp-pq-----p---p------b---------------P-------K-"]
chesspos = chesspositions[0]
chessmoves = [(35, 18), (46, 10), (56, 8), (33, 17), (17, 25)]
selected = None
totalloss = 0
previewing = 0


# def tocmy(rgb):
#     r, g, b = rgb
#     c = 1 - (r / 255)
#     m = 1 - (g / 255)
#     y = 1 - (b / 255)
#     return (c, m, y)


# def torgb(cmy):
#     c, m, y = cmy
#     print(cmy)
#     r = 255 * (1 - c)
#     g = 255 * (1 - m)
#     b = 255 * (1 - y)
#     print(r, g, b)
#     return (r, g, b)


# def mix(colors):
#     cmycols = [tocmy(col) for col in colors]
#     print(cmycols)
#     l = len(cmycols)
#     mc = sum(col[0] for col in cmycols)/l
#     mm = sum(col[1] for col in cmycols)/l
#     my = sum(col[2] for col in cmycols)/l
#     return torgb([mc, mm, my])


# print(mix([(255, 0, 0), (0, 0, 255)]))


def same_col(a, b):
    for val in range(3):
        if abs(a[val] - b[val]) > 15:
            return False
    return True


def strat(memory):
    length = len(memory)
    #print(memory)
    if length == 0:
        return 0
    if length > 7:
        return 0
    if length == 1:
        return memory[-1]
    return 1 - (0 in memory[-2:])


def write(txt, pos, col, size):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    screen.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))


def draw_options(custops=[], custprompt=None):
    global activated, question
    prompt = prompts[question] if custprompt is None else custprompt
    write(prompt, (400, 180), (0, 0, 0), 50 if question not in (9, 21) else 30)
    options = ops[question].split(", ")
    if custops != []:
        options = list(custops)
    tcol = (0, 0, 0)
    if question == 10:
        activated = [0, 0, 0, 0]
    for j in range(2):
        for i in range(2):
            boxcol = (150, 150, 150)
            if (100 + i * 310) < mouse[0] < (390 + i * 310) and (350 + j * 120) < mouse[1] < (450 + j * 120) and not previewing:
                boxcol = (120, 120, 120)
            if question == 10:
                t = time.time()
                if times[2 * j + i] < t - lastclicked[2 * j + i] < times[2 * j + i] + 0.5:
                    boxcol = (0, 100, 0)
                    activated[2 * j + i] = 1
            elif question == 25 and 2 * j + i == current:
                boxcol = (0, 100, 0)
            elif question == 27:
                boxcol = [(250, 250, 250), (250, 0, 0), (0, 250, 0), (0, 0, 250)][2 * j + i]
            if str(options[2 * j + i]) not in " ":
                pygame.draw.rect(screen, boxcol, pygame.Rect(100 + i * 310, 350 + j * 120, 290, 100))
                write(options[2 * j + i], (245 + i * 310, 400 + j * 120), tcol, 50)
    if activated == [1, 1, 1, 1]:
        activated = [0, 0, 0, 0]
        question += 1


def loselife(life=1):
    global lives, totalloss
    lives -= life
    totalloss += 1
    # print(totalloss)


def run_click():
    global question, lives, clicks, stime, bgcol, twodig, chosen, gb, lastclicked, a, b, counter, mem, points, opp, manarecipe, skips, current, rgbcolor, targetcolor, selected, chessmoves, chesspos, chesspositions, previewing
    #print(question)
    if question == 23:
        625, 25, 150, 100
        if 625 < mouse[0] < 775 and 25 < mouse[1] < 125:
            #print("ans")
            counter = 1 - counter
    if question == 4:
        if time.time() - stime >= 2:
            question += 1
            stime = None
        else:
            loselife()
    elif question == 6:
        if 600 < mouse[1] < 640:
            code.pop(0)
            code.append(dial)
            #print(code)
        if code == [12, 5, 18]:
            question += 1
    elif question == 19:
        #print(ctime, stime, counter)
        if ctime is None:
            counter += 1
            if stime is None:
                stime = time.time()
            if counter >= 80:
                stime = None
                counter = 0
                question += 1
    elif question == 21:
        passed = 1
        for j in range(2):
            for i in range(2):
                if (100 + i * 310) < mouse[0] < (390 + i * 310) and (350 + j * 120) < mouse[1] < (450 + j * 120):
                    passed = 0
        if passed:
            question += 1
        else:
            loselife()
    elif question == 28:
        square = (mouse[0]//100, mouse[1]//100)
        squarenum = square[1] * 8 + square[0]
        target = chesspos[squarenum]
        if selected is None and target != "-" and target == target.upper():
            selected = square
        elif selected is not None:
            selectednum = selected[1] * 8 + selected[0]
            if selectednum == squarenum:
                selected = None
            elif chesspos[squarenum] == chesspos[squarenum].upper() and chesspos[squarenum] != "-":
                selected = square
            else:
                move = (selectednum, squarenum)
                if chessmoves[counter] == move:
                    selected = None
                    counter += 1
                    if counter >= 5:
                        question += 1
                    else:
                        chesspos = chesspositions[counter]
                else:
                    loselife()
                    selected = None
    else:
        for j in range(2):
            for i in range(2):
                if (100 + i * 310) < mouse[0] < (390 + i * 310) and (350 + j * 120) < mouse[1] < (450 + j * 120):
                    # print(2*j+i)
                    clicked = 2 * j + i
                    if question == 2:
                        if twodig == "":
                            twodig += "1846"[2*j+i]
                        else:
                            twodig += "1846"[2*j+i]
                            if twodig == "16":
                                twodig = ""
                                question += 1
                            else:
                                loselife()
                                twodig = ""
                    elif question == 5:
                        chosen = 2 * j + i
                        question += 1
                    elif question == 8:
                        #print(stime + [2, -3, 27, 42][2*j+i], time.localtime().tm_sec)
                        if ((stime + [2, -3, 27, 42][2*j+i])%60 - time.localtime().tm_sec + offset)**2 <= 1:
                            question += 1
                            stime = None
                        else:
                            loselife()
                    elif question == 10:
                        lastclicked[2 * j + i] = time.time()
                    elif question == 11:
                        a = [1, 2, 3, 42][2 * j + i]
                        question += 1
                    elif question == 12:
                        b = [7, 11, 0, 12][2 * j + i]
                        question += 1
                    elif question == 13:
                        if a + b == [13, 14, 42, 10][2 * j + i]:
                            question += 1
                        else:
                            loselife(2)
                            question += 1
                    elif question == 14:
                        if 2 * j + i == 0:
                            if counter == 0:
                                lives += 1
                                if lives >= 4:
                                    counter = 1
                            else:
                                lifechanges = [0, -1, -2, 4, -1, -1, -1, 4, -6]
                                change = lifechanges[counter]
                                if change > 0:
                                    lives += change
                                else:
                                    loselife(-change)
                                counter += 1
                        else:
                            question += 1
                            counter = 0
                    elif question == 15:
                        loselife()
                    elif question == 16:
                        if 2 * j + i == conv[chosen]:
                            question += 1
                        else:
                            loselife()
                    elif question == 17:
                        comp = strat(mem)
                        if 2 * j + i == 0:
                            mem.append(1)
                            if comp == 0:
                                points[1] += 5
                            else:
                                points[0] += 3
                                points[1] += 3
                        else:
                            mem.append(0)
                            if comp == 1:
                                points[0] += 5
                            else:
                                points[0] += 1
                                points[1] += 1
                        opp = comp
                        counter += 1
                        if counter >= 10:
                            counter = 0
                            if points[0] >= 25:
                                question += 1
                            else:
                                loselife()
                                points = [0, 0]
                                mem = []
                                opp = 2
                    elif question == 22:
                        if 2 * j + i == 0:
                            manarecipe[0] += 1
                            if manarecipe[0] > manacost[0]:
                                loselife()
                                manarecipe = [0, ""]
                        else:
                            manarecipe[1] += "-WRB"[2 * j + i]
                            if manarecipe[1] not in manacost[1]:
                                loselife()
                                manarecipe = [0, ""]
                        if manarecipe == manacost:
                            question += 1
                    elif question == 24:
                        if clicked == 0:
                            lives += 2
                        elif clicked == 1:
                            skips += 1
                        elif clicked == 2:
                            previewing = 1
                            question = 29
                        question += 1
                    elif question == 25:
                        if clicked == current:
                            if stime is None:
                                stime = time.time()
                            counter += 1
                            oc = current
                            while current == oc:
                                current = random.randint(0, 3)
                            if counter >= 20:
                                counter = 0
                                question += 1
                                stime = None
                        else:
                            loselife()
                    elif question == 27:
                        if clicked == 0:
                            rgbcolor = [0, 0, 0]
                        else:
                            selectedcol = [(255, 0, 0), (0, 255, 0), (0, 0, 255)][clicked - 1]
                            for i in range(3):
                                rgbcolor[i] += selectedcol[i]
                            scale = 255 / max(rgbcolor)
                            for i in range(3):
                                rgbcolor[i] *= scale
                            #print(rgbcolor)
                            if same_col(rgbcolor, targetcolor):
                                #print("goal reached")
                                counter += 1
                                if counter >= 4:
                                    question += 1
                                    counter = 0
                                else:
                                    targetcolor = [[255, 0, 127.5], [255, 63.75, 0], [0, 63.75, 255], [127.5, 255, 0]][counter]
                    elif question == 29:
                        tl = totalloss
                        if [tl<3, 2<tl<6, 5<tl<9, tl>8][clicked]:
                            question += 1
                        else:
                            loselife()
                    elif question == 30:
                        if previewing:
                            previewing = 0
                            question = 25
                        else:
                            if clicked == 0:
                                if lives == 1:
                                    question += 2
                                else:
                                    loselife()
                                    question += 1
                            elif clicked == 1:
                                loselife()
                                question += 1
                    else:
                        if 2 * j + i == int(answers[question-1]):
                            if question == 9:
                                question = 1
                                gb = 1
                            elif question == 3 and gb:
                                question = 10
                            elif question == 23 and counter == 1:
                                loselife()
                            else:
                                question += 1
                                draw_board()
                        else:
                            loselife()


def draw_board():
    global stime, clicks, bgcol, question, stage, dial, counter, ctime, targetcolor, deaths
    bgcol = (200, 200, 200)
    if question == 19 and counter > 0:
        redness = min(255, 100 * (time.time() - stime))
        bgcol = (255, 255 - redness, 255 - redness)
        if redness > 250:
            stime = None
            loselife()
            counter = 0
            ctime = time.time()
    screen.fill(bgcol)
    if lives <= 0 and stage != 2:
        question = 0
        stage = 2
        deaths += 1
        #print(deaths)
    elif question == 32:
        question = 0
        stage = 3
    if stage == 0:
        write("The (Almost) Impossible Quiz", (400, 200), (0, 0, 0), 60)
        boxcol = (150, 150, 150)
        if 260 < mouse[0] < 260 + 280 and 350 < mouse[1] < 450:
            boxcol = (120, 120, 120)
        pygame.draw.rect(screen, boxcol, pygame.Rect(260, 350, 280, 100))
        write("PLAY", (400, 400), (0, 0, 0), 60)
    elif stage == 2:
        write("GAME OVER", (400, 400), (0, 0, 0), 60)
    elif stage == 3:
        write("You won!", (400, 400), (0, 0, 0), 60)
        write(message, (400, 600), (0, 0, 0), 40)
        write(f"Deaths: {deaths}", (400, 700), (0, 0, 0), 40)
    else:
        write("Lives:", (150, 700), (0, 0, 0), 35)
        lcolor = [(150, 0, 0), (200, 150, 0), (0, 150, 0), (0, 0, 150), (0, 0, 250), (150, 0, 150), (150, 0, 150), (150, 0, 150)][lives-1]
        write(lives, (200, 700), lcolor, 35)
        write(f"Skips: {skips}", (650, 700), (0, 0, 0), 35)
        if question in (1, 2, 3, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 21, 24, 26, 29, 30, 31):
            draw_options()
            if previewing and question == 30:
                write("Coming up soon...", (400, 600), (0, 0, 0), 50)
        elif question == 4:
            write("Patience is key in life...", (400, 180), (0, 0, 0), 50)
            if stime is None:
                stime = time.time()
        elif question == 6:
            write("12 - 5 - 18", (400, 180), (0, 0, 0), 50)
            # pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(190 + 0 * 20, 380, 40, 40))
            pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(210, 390, 380, 20))
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(190 + dial * 20, 380, 40, 40))
            write("Submit", (400, 620), (0, 0, 0), 50)
        elif question == 8:
            if stime is None:
                stime = time.localtime().tm_sec
            draw_options([(stime + 5 - offset)%60, (stime - offset)%60, (stime + 30 - offset)%60, (stime + 45 - offset)%60])
        elif question == 17:
            draw_options()
            write(f"You: {points[0]}", (250, 525), (0, 0, 0), 50)
            pygame.draw.rect(screen, [(150, 0, 0), (0, 150, 0)][mem[-1]] if mem != [] else (150, 150, 150), pygame.Rect(200, 575, 100, 20))
            write(f"Computer: {points[1]}", (550, 525), (0, 0, 0), 50)
            pygame.draw.rect(screen, [(150, 0, 0), (0, 150, 0), (150, 150, 150)][opp], pygame.Rect(500, 575, 100, 20))
            write(f"{counter + 1} / 10", (400, 80), (0, 0, 0), 50)
        elif question == 19:
            write("Click 80 times before the room turns red!", (400, 180), (0, 0, 0), 50)
            pygame.draw.rect(screen, (0, 150, 0), pygame.Rect(225, 350, 350, 100))
            if ctime is None or time.time() - ctime > 2:
                write(counter, (400, 400), (0, 0, 0), 50)
                ctime = None
            if counter > 0 and redness > 175:
                #print(45)
                write("(Scroll!)", (750, 50), (250, 0, 0), 30)
        elif question == 22:
            draw_options()
            dig = "" if manarecipe[0] == 0 else str(manarecipe[0])
            write(dig + manarecipe[1], (400, 275), (0, 0, 0), 50)
            screen.blit(symbols, (527, 370), (0, 0, 55, 60))
            screen.blit(symbols, (527, 490), (55, 0, 60, 60))
            screen.blit(symbols, (217, 490), (170, 0, 60, 60))
        elif question == 23:
            draw_options()
            if counter == 0:
                pygame.draw.rect(screen, (0, 150, 0), pygame.Rect(625, 25, 150, 100))
                write("ON", (700, 75), (0, 0, 0), 40)
            else:
                pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(625, 25, 150, 100))
                write("OFF", (700, 75), (0, 0, 0), 40)
            if counter == 0:
                ws = 3
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, mouse[1] - ws))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, mouse[1] + ws, 800, 800 - mouse[1] - ws))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, mouse[0] - ws, 800))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(mouse[0] + ws, 0, 800 - mouse[0] - ws, 800))
        elif question == 25:
            draw_options()
            if stime is not None:
                if time.time() - stime > 10:
                    loselife()
                    stime = None
                    counter = 0
                else:
                    write(round(10 - time.time() + stime, 1), (750, 50), (0, 0, 0), 50)
        elif question == 27:
            draw_options([], "Make the rectangle the color " + ["rose", "vermillion", "cerulean", "chartreuse"][counter])
            pygame.draw.rect(screen, targetcolor, pygame.Rect(295, 235, 210, 70))
            pygame.draw.rect(screen, rgbcolor, pygame.Rect(300, 240, 200, 60))
        elif question == 28:
            for i in range(8):
                for j in range(8):
                    tilecol = [(235, 236, 208), (115, 149, 82)][(i+j) % 2]
                    if (i, j) == selected:
                        tilecol = (180, 180, 0)
                    pygame.draw.rect(screen, tilecol, pygame.Rect(100*i, 100*j, 100, 100))
            draw_pieces(chesspos)
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(250, 650, 300, 100))
            write("White To Move", (400, 685), (0, 0, 0), 50)
            write("Lives:", (140, 750), (0, 0, 0), 35)
            lcolor = [(150, 0, 0), (200, 150, 0), (0, 150, 0), (0, 0, 150), (0, 0, 250), (150, 0, 150), (150, 0, 150), (150, 0, 150)][lives-1]
            write(lives, (190, 750), lcolor, 35)
            if counter >= 4:
                write("Find the move best for Black", (400, 725), (0, 0, 0), 25)
            else:
                write("Find the move best for White", (400, 725), (0, 0, 0), 25)


my_image = pygame.image.load("800px-Chess_Pieces_Sprite.svg.png")
# my_image = pygame.image.load("imp_quiz/800px-Chess_Pieces_Sprite.svg.png")
drawings = pygame.transform.smoothscale(my_image, (600, 200.25))


def knight(x, y, size, color):
    screen.blit(drawings, (x-50, y-50), (300, 100*color, 100, 100))


def king(x, y, size, color):
    screen.blit(drawings, (x-50, y-50), (0, 100*color, 100, 100))


def queen(x, y, size, color):
    screen.blit(drawings, (x-50, y-50), (100, 100*color, 100, 100))


def bishop(x, y, size, color):
    screen.blit(drawings, (x-50, y-50), (200, 100*color, 100, 100))


def rook(x, y, size, color):
    screen.blit(drawings, (x-50, y-50), (400, 100*color, 100, 100))


def pawn(x, y, size, color):
    screen.blit(drawings, (x-50, y-50), (500, 100*color, 100, 100))


def draw_pieces(code):
    for i in range(64):
        if code[i].upper() == "P":
            pawn((i%8)*100+50, (i//8)*100+50, 100, code[i]==code[i].lower())
        elif code[i].upper() == "R":
            rook((i%8)*100+50, (i//8)*100+50, 100, code[i]==code[i].lower())
        elif code[i].upper() == "B":
            bishop((i%8)*100+50, (i//8)*100+50, 100, code[i]==code[i].lower())
        elif code[i].upper() == "Q":
            queen((i%8)*100+50, (i//8)*100+50, 100, code[i]==code[i].lower())
        elif code[i].upper() == "K":
            king((i%8)*100+50, (i//8)*100+50, 100, code[i]==code[i].lower())
        elif code[i].upper() == "N":
            knight((i%8)*100+50, (i//8)*100+50, 100, code[i]==code[i].lower())


async def main():
    global stime, skips, question, stage, mouse, lives, clicks, running, mousedown, dial, mananum, manaprompt, manacost, manarecipe, prompts, chosen, code, gb, twodig, lastclicked, times, activated, a, b, mem, opp, points, ctime, current, rgbcolor, targetcolor, chesspos, chesspositions, selected, totalloss, counter
    while running:
        draw_board()
        # if question == 19 and counter > 0:
            # print(100 * (time.time() - stime))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse = pygame.mouse.get_pos()
                if question == 6 and mousedown and 350 < mouse[1] < 450:
                    dial = (mouse[0] - 195) // 20
                    dial = max(1, dial)
                    dial = min(19, dial)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    mousedown = 1
                    if stage == 0 and 260 < mouse[0] < 260 + 280 and 350 < mouse[1] < 450:
                        stage = 1
                    elif stage == 1:
                        run_click()
                    elif stage == 2:
                        question = 1
                        lives = 3
                        skips = 2
                        stage = 0
                        clicks = 0
                        stime = None
                        mananum = random.randint(0, 4)
                        manaprompt = ["It's a Shock you got this far.", "Go to Sleep, you'll never beat this quiz.", "Give up already! I need some Solitude.", "This quiz will Obliterate your patience.", "Stop trying to persevere and Get Lost."][mananum]
                        manacost = [[0, "R"], [2, "BB"], [3, "WW"], [6, "RR"], [1, "W"]][mananum]
                        manarecipe = [0, ""]
                        prompts[22] = manaprompt
                        chosen = 0
                        dial = 10
                        code = [0, 0, 0]
                        gb = 0
                        twodig = ""
                        lastclicked = [0, 0, 0, 0]
                        times = [5, 7, 1, 2]
                        activated = [0, 0, 0, 0]
                        a = 0
                        b = 0
                        counter = 0
                        points = [0, 0]
                        mem = []
                        opp = 2
                        ctime = None
                        current = random.randint(0, 3)
                        rgbcolor = [0, 0, 0]
                        targetcolor = [255, 0, 127.5]
                        chesspos = chesspositions[0]
                        selected = None
                        totalloss = 0
                elif event.button == 5:
                    #print("sd")
                    if question == 19 and counter > 0:
                        ct = time.time()
                        if ct - stime < 0.1:
                            stime = ct
                        else:
                            stime += 0.1
            elif event.type == pygame.MOUSEBUTTONUP:
                mousedown = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and skips > 0:
                    skips -= 1
                    question += 1
                    counter = 0
                    stime = None
                    ctime = None
                elif event.key == pygame.K_6 and question == 8:
                    question += 1
                    stime = None
                elif event.key == pygame.K_HOME and question == 15:
                    question += 1
        clock.tick(30)
        await asyncio.sleep(0)


asyncio.run(main())
