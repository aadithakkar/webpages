import pygame
import sys
import time
import asyncio

pygame.init()

screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("The (Barely) Possible Quiz")


ops = ["",
       "Idk, 14, 21, 28",
       "'What', What?, I don't know!, ABC123",
       "Hippopotamus, French, Goldsmith, Ware",
       "",
       "7/3 apples, 3 apples, 1 + 2 apples, 2 + 1 apple",
       "True, False, , ",
       "True, False, , ",
       "",
       "1, 4, 9, Unlimited",
       "+1 Life, Continue, , ",
       "Letter, Cell, Inch, Toenail",
       "0, 1, x, All of the above",
       "",
       "..., ..., Pump blood!, ...",
       "Ok, I won't, No thanks, I'm good",
       "h5, a5, Nh6, e6",
       "14, 15, 16, 17",
       "T, A, W, F",
       "",
       "Gray, White, Black, Turquoise",
       "Red, Yellow, Orange, Green",
       "True, False, , ",
       "Yes, No, Dunno, Probably Not",
       "Turret, Guardian Scout, Stalker, Skywatcher",
       "Have mercy!, Oh well, I'll find a way, I don't need to",
       "Yes, No, , ",
       "That's right!, , , ",
       "That can't be, Sounds untrue, Sounds sus, HELP!!",
       "None, 28, 29, 30",
       "True, False, , "]

prompts = ["",
           "What number is 3 times greater than 7?",
           "'What' is the password?",
           "Choose the best word",
           "",
           "1 apple + 6 apples / 3 apples",
           "You will correctly answer False",
           "Okay you can answer False now",
           "",
           "How many lives do you have?",
           "Ok I'll give your lives back...",
           "Which is a unit of life?",
           "Which are numbers?",
           "",
           "Select the option that speaks to your heart",
           "Remember: 2042256246",
           "e4",
            "17) Which question is this?",
            "What is the first letter of the alphabet?",
            "",
            "What color is the background?",
            "What color is the background?",
            "You will answer False on this question",
            "Can you find the odd one out?",
            "Which is hardest to kill?",
            "I bet you can't escape me!",
            "Are you stuck in a time loop?",
            "Wait a minute, you might actually beat this quiz",
            "If you get this question wrong, you will die",
            "There are 30 questions. How many have you done?",
            ""]

BLUE = (0, 0, 100)
PINK = (200, 120, 120)
DGRAY = (50, 50, 50)
LGRAY = (200, 200, 200)
ORANGE = (200, 120, 0)
BROWN = (80, 40, 0)
PURPLE = (100, 0, 150)
colcycle = [BLUE, PINK, DGRAY, LGRAY, ORANGE, BROWN, PURPLE, BLUE, PINK, DGRAY, LGRAY, BROWN, PURPLE, BLUE, PINK, DGRAY, LGRAY, BROWN, PURPLE]

answers = "32--300--113-20331-0--02----11"


running = True
clock = pygame.time.Clock()
question = 1
lives = 3
skips = 2
stage = 0
clicks = 0
stime = None
opening = 0
move = [2, 3, 0, 1]
loop = 0
mouse = pygame.mouse.get_pos()


def write(txt, pos, col, size):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    screen.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))


def draw_options():
    write(prompts[question], (400, 180), (0, 0, 0), 50 if question != 29 else 40)
    options = ops[question].split(", ")
    tcol = (0, 0, 0)
    if question == 14:
        tcol = (149, 149, 149)
    for j in range(2):
        for i in range(2):
            boxcol = (150, 150, 150)
            if (100 + i * 310) < mouse[0] < (390 + i * 310) and (350 + j * 120) < mouse[1] < (450 + j * 120):
                if question != 14:
                    boxcol = (120, 120, 120)
            if options[2 * j + i] not in " ":
                pygame.draw.rect(screen, boxcol, pygame.Rect(100 + i * 310, 350 + j * 120, 290, 100))
                if 2 * j + i == 3 and question == 23:
                    tcol = (50, 50, 50)
                write(options[2 * j + i], (245 + i * 310, 400 + j * 120), tcol, 50)


def run_click():
    global question, lives, clicks, opening, stime, bgcol, loop
    #print(question)
    if question == 4:
        if 100 < mouse[0] < 390:
            if 5 <= clicks <= 8:
                lives -= 1
            else:
                clicks += 1
        elif 410 < mouse[0] < 700:
            if 5 <= clicks <= 8:
                clicks += 1
            else:
                lives -= 1
                clicks = 0
        if clicks >= 10:
            question += 1
    elif question == 8:
        question += 1
    elif question == 13:
        if clicks == 1:
            question += 1
            stime = None
            clicks = 0
        else:
            lives -= 1
    elif question == 19:
        if 100 < mouse[0] < 390:
            clicks += 1
        elif 410 < mouse[0] < 700:
            lives -= 1
        if clicks >= 30:
            question += 1
            clicks = 0
    else:
        for j in range(2):
            for i in range(2):
                if (100 + i * 310) < mouse[0] < (390 + i * 310) and (350 + j * 120) < mouse[1] < (450 + j * 120):
                    #print(2*j+i)
                    if question == 9:
                        if 2 * j + i == 0 and lives == 1:
                            question += 1
                        else:
                            lives -= 1
                    elif question == 3:
                        opening = 2 * j + i
                        question += 1
                    elif question == 16:
                        if 2 * j + i == move[opening]:
                            question += 1
                        else:
                            lives -= 1
                    elif question == 21:
                        if 2 * j + i == 2 and bgcol == ORANGE:
                            question += 1
                            stime = None
                        else:
                            lives -= 1
                    elif question == 22:
                        if 2 * j + i == 0 and clicks == 1:
                            question += 1
                            lives += 1
                            clicks = 0
                        elif 2 * j + i == 1:
                            clicks = 1
                            lives -= 1
                        else:
                            lives -= 1
                    elif question == 25:
                        lives -= 1
                    elif question == 26:
                        if loop == 1:
                            question += 1
                        else:
                            question -= 3
                            loop = 1
                    elif question == 27:
                        if time.time() - stime >= 60 and 2 * j + i == 0:
                            question += 1
                            stime = None
                        else:
                            lives -= 1
                    elif question == 28:
                        question += 1
                    else:
                        if 2 * j + i == int(answers[question-1]):
                            question += 1
                            draw_board()
                        else:
                            lives -= 1
                            if question == 10:
                                lives += 2
                                if lives == 3:
                                    prompts[question] = "Don't get greedy..."
                                elif lives == 4:
                                    prompts[question] = "I'm warning you..."
                                elif lives >= 5:
                                    lives = 0


def draw_board():
    global stime, clicks, bgcol, question, stage, mouse
    bgcol = (200, 200, 200)
    if question == 21 and stime is not None:
        bgcol = colcycle[int(((time.time()-stime)//0.5-1) % len(colcycle))]
    screen.fill(bgcol)
    if lives <= 0:
        question = 0
        stage = 2
    elif question == 31:
        question = 0
        stage = 3
    if stage == 0:
        write("The (Barely) Possible Quiz", (400, 200), (0, 0, 0), 60)
        boxcol = (150, 150, 150)
        if 260 < mouse[0] < 260 + 280 and 350 < mouse[1] < 450:
            boxcol = (120, 120, 120)
        pygame.draw.rect(screen, boxcol, pygame.Rect(260, 350, 280, 100))
        write("PLAY", (400, 400), (0, 0, 0), 60)
    elif stage == 2:
        write("GAME OVER", (400, 400), (0, 0, 0), 60)
    elif stage == 3:
        write("You won!", (400, 400), (0, 0, 0), 60)
        message = ["But 1 life remaining? You just got lucky.", "But 2 lives remaining? Disappointing.", "But 3 lives remaining? I know you cheated.", "4 lives remaining? Not bad."][lives-1]
        write(message, (400, 600), (0, 0, 0), 40)
    else:
        write("Lives:", (150, 700), (0, 0, 0), 35)
        lcolor = [(150, 0, 0), (200, 150, 0), (0, 150, 0), (0, 0, 150), (0, 0, 150)][lives-1]
        write(lives, (200, 700), lcolor, 35)
        if question in (1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 20, 22, 23, 25, 26, 28, 29, 30):
            draw_options()
        elif question == 4:
            write("Click the green button 10 times!", (400, 180), (0, 0, 0), 50)
            pygame.draw.rect(screen, (150, 0, 0) if 5 <= clicks <= 8 else (0, 150, 0), pygame.Rect(100, 405, 290, 105))
            pygame.draw.rect(screen, (0, 150, 0) if 5 <= clicks <= 8 else (150, 0, 0), pygame.Rect(410, 405, 290, 105))
            write(clicks, ((555, 452.5) if 5 <= clicks <= 8 else (245, 452.5)), (0, 0, 0), 50)
        elif question == 8:
            write("Patience is generally key in life...", (400, 180), (0, 0, 0), 50)
        elif question == 13:
            write("Click the button below", (400, 180), (0, 0, 0), 50)
            pygame.draw.rect(screen, (0, 150, 0), pygame.Rect(255, 347.5, 290, 105))
            if 255 < mouse[0] < 545 and 347.5 < mouse[1] < 452.5:
                if stime is None:
                    stime = time.time()
                if time.time() - stime >= 3:
                    clicks = 1
                    write("Okay now!", (400, 400), (0, 0, 0), 20)
                else:
                    write("Wait, not yet!", (400, 400), (0, 0, 0), 20)
            else:
                write("Click me!", (400, 400), (0, 0, 0), 20)
        elif question == 19:
            write("Click the green button 30 times", (400, 180), (0, 0, 0), 50)
            pygame.draw.rect(screen, (0, 150, 0), pygame.Rect(100, 405, 290, 105))
            pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(410, 405, 290, 105))
            write(clicks, (245, 452.5), (0, 0, 0), 50)
        elif question == 21:
            draw_options()
            if stime == None:
                stime = time.time()
        elif question == 24:
            draw_options()
            ws = 25
            write("P.S. Stalker refers to the Old Man", (400, 750), (0, 0, 0), 30)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, mouse[1] - ws))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, mouse[1] + ws, 800, 800 - mouse[1] - ws))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, mouse[0] - ws, 800))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(mouse[0] + ws, 0, 800 - mouse[0] - ws, 800))
        elif question == 27:
            draw_options()
            if stime is None:
                stime = time.time()


async def main():
    global stime, skips, question, stage, mouse
    run = True
    while run:
        draw_board()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #print(mouse)
                if stage == 0 and 260 < mouse[0] < 260 + 280 and 350 < mouse[1] < 450:
                    stage = 1
                elif stage == 1:
                    #print("tried running")
                    run_click()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and question == 25:
                    question += 1
                    stime = None
                elif event.key == pygame.K_s and skips > 0:
                    skips -= 1
                    question += 1
                elif event.key == pygame.K_6 and question == 27:
                    question += 1
                    stime = None
        clock.tick(30)
        await asyncio.sleep(0)

asyncio.run(main())
