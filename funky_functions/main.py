import pygame
#import pygame.scrap as scrap
import time
import function_eval as fe
import sys
import asyncio
from dialogues import dialogues


pygame.init()

pygame.display.set_caption("Funky Functions")
screen = pygame.display.set_mode([1150, 650])


#scrap.init()


running = True
stage = "level"
level = 1
dial = 0
chars = "1234567890+-*/()x."
cursor = 0
typedf = ""
typedg = ""
row = 0
substage = "dial"
dialnum = 0
clock = pygame.time.Clock()


BG_COLS = [(115, 175, 115), (115, 175, 115), (35, 70, 35), (255, 240, 130), (240, 180, 85), (240, 180, 85), (125, 25, 25), (60, 0, 45)]
BOX_COLS = [(85, 145, 85), (85, 145, 85), (25, 55, 25), (235, 210, 115), (220, 160, 70), (220, 160, 70), (110, 15, 15), (45, 0, 35)]
LEV_NAMES = ["The First Machine", "The Enhancer", "The Expunger", "F.E.L.I.X.", "Optimus Prime", "The Dimensioner", "Fortune Teller",
             "The Dimensioner 2.0", "The Absolutron", "The Zero Exterminator", "F.E.L.I.X. Proofreader", "The Mini Exterminator", "The Decimator",
             "The Elevator", "The Style Tester", "The Styler", "The Shortener", "The Collatzer", "The Factory Eel", "The Shortener 2.0",
             "The Terminator", "The Time Machine", "Binary Adder", "The Final Machine"]


def test(inp, out, func, g=0, hide=0):
    if func == "()":
        write("Empty Function Error!", 575, 560, 30, (200, 0, 0))
        return None
    try:
        actual_out = fe.evaluate(func.replace("x", f"({inp})"), func, g)
    except SyntaxError:
        write("Syntax Error!", 575, 560, 30, (200, 0, 0))
        return None
    except RecursionError:
        if level == 24:
            return True
        write("Stack Overflow!", 575, 560, 30, (200, 0, 0))
        return None
    except OverflowError:
        write("Overflow Error!", 575, 560, 30, (200, 0, 0))
        return None
    except ZeroDivisionError:
        if out == "undefined":
            return True
        write(f"Test Fail: In = {inp}, Out = undefined, Expected = {out}", 575, 560, 30, (200, 0, 0))
        return None
    except:
        write("Error", 575, 560, 30, (200, 0, 0))
        return None
    if out == "undefined":
        write(f"Test Fail: In = {inp}, Out = {actual_out}, Expected = {out}", 575, 560, 30, (200, 0, 0))
        return None
    if level == 24:
        write("Test Fail: Machine Still Works!", 575, 560, 30, (200, 0, 0))
        return None
    try:
        if float(actual_out) == float(out) or round(float(actual_out), 3) == float(out):
            return True
        else:
            if hide:
                write("Test Fail: Test Hidden", 575, 560, 30, (200, 0, 0))
            else:
                write(f"Test Fail: In = {inp}, Out = {actual_out}, Expected = {out}", 575, 560, 30, (200, 0, 0))
            return False
    except:
        write("Error", 575, 560, 30, (200, 0, 0))
        return None


def write(t, x, y, s, col=(0, 0, 0), center=1):
    font = pygame.font.Font(None, s)
    textimg = font.render(t, True, col)
    isize = textimg.get_size()
    if center:
        screen.blit(textimg, (x-isize[0]/2, y-isize[1]/2))
    else:
        screen.blit(textimg, (x, y-isize[1]/2))
    return 575-isize[0]/2


def runfunc(f, g):
    if level == 1:
        return test(3, 3, f, g) and test(7, 7, f, g)
    if level == 2:
        return test(5, 6, f, g) and test(9, 10, f, g)
    if level == 3:
        return test(6, "undefined", f, g) and test(11, 11, f, g)
    if level == 4:
        return test(13, 42, f, g) and test(666, 642, f, g)
    if level == 5:
        return test(13, 999, f, g) and test(17, 999, f, g, 1)
    if level == 6:
        return test(4, 64, f, g) and test(2, 8, f, g)
    if level == 7:
        return test(1, 40, f, g) and test(3, 280, f, g) and test(5, 1240, f, g, 1)
    if level == 8:
        return test(1, 6, f, g) and test(8, 24, f, g) and test(64, 96, f, g, 1)
    if level == 9:
        return test(-3, 3, f, g) and test(7, 7, f, g) and test(0, 0, f, g)
    if level == 10:
        return test(0, 0, f, g) and test(14, 1, f, g) and test(19, 1, f, g, 1)
    if level == 11:
        return test(42, 1, f, g) and test(642, 1, f, g) and test(100, 0, f, g)
    if level == 12:
        return test(49, 0, f, g) and test(50, 1, f, g) and test(75, 1, f, g, 1)
    if level == 13:
        return test(14, 1, f, g) and test(12.6, 0, f, g) and test(-3, 1, f, g) and test(0.5, 0, f, g)
    if level == 14:
        return test(0.3, 1, f, g) and test(4.9, 5, f, g) and test(7, 7, f, g) and test(0.0001, 1, f, g)
    if level == 15:
        return test(100, 100, f) and test(9, 0, f) and test(820, 820, f, g, 1)
    if level == 16:
        return test(120, 80, f) and test(100, 100, f) and test(199, 1, f, g, 1)
    if level == 17:
        return test(13, 4, f) and test(99, 9, f) and test(782, 8, f, g, 1)
    if level == 18:
        return test(60, 30, f) and test(13, 40, f) and test(21, 64, f, g, 1)
    if level == 19:
        return test(4, 24, f) and test(1, 1, f) and test(6, 720, f, g, 1)
    if level == 20:
        return test(98, 17, f) and test(12, 3, f) and test(184, 13, f, g, 1)
    if level == 21:
        return test(0.6, 8, f) and test(0.375, 11, f) and test(0.5, 3, f, g, 1)
    if level == 22:
        return test(813, 318, f, g) and test(420, 24, f, g) and test(1034, 4301, f, g, 1)
    if level == 23:
        return test(6, 2, f, g) and test(16, 1, f, g) and test(1, 1, f, g) and test(52, 3, f, g, 1)
    if level == 24:
        return test(1, 1, f, g)


def run():
    global substage
    try:
        f = fe.modify(typedf)
        g = fe.modify(typedg)
    except:
        write("Error", 575, 560, 30, (200, 0, 0))
        return None
    if runfunc(f, g):
        substage = "won"
        draw_board()
        write("Success!", 575, 560, 40, (0, 100, 0))


def run_click():
    global substage, typedg, typedf, cursor, dialnum
    x = mouse[0]
    y = mouse[1]
    if 900 < x < 1080 and 515 < y < 605:
        run()
    elif 70 < x < 250 and 515 < y < 605:
        # copied = str(pygame.scrap.get(pygame.SCRAP_TEXT))[2:-5]
        # for el in copied:
        #     if el not in chars:
        #         return None
        # if row:
        #     typedg = copied
        # else:
        #     typedf = copied
        # cursor = len(copied)
        draw_board()
    elif 1015 < x < 1105 and 25 < y < 55:
        # print("RESET")
        dialnum = 0
        substage = "dial"
        typedf = ""
        typedg = ""
        cursor = 0
        draw_board()


# async def inter6():
#     write("The company has started to quickly grow in power.", 575, 108, 40)
#     write("We are giving you a new power that allows your inputs to quickly grow too.", 575, 216, 40)
#     write("This 'power' is formally called an 'exponent.'", 575, 324, 40)
#     write("Type '^' to use it in a machine.", 575, 432, 40)
#     write("Use it wisely.", 575, 540, 40)



def draw_board():
    global chars
    if stage == "menu":
        screen.fill((155, 155, 155))
        write("Funky Functions", 575, 85, 70)
    elif stage == "level":
        screen.fill(BG_COLS[(level-1)//3])
        textcol = (0, 0, 0) if level < 22 else (255, 255, 255)
        write(LEV_NAMES[level-1], 575, 40, 50, textcol)
        boxcol = BOX_COLS[(level-1)//3]
        pygame.draw.rect(screen, boxcol, pygame.Rect(275, 85, 600, 85))
        if level < 22:
            pygame.draw.rect(screen, boxcol, pygame.Rect(160, 300, 830, 80))
            if substage == "won":
                if level < 13 or level > 18:
                    curx = write(typedf, 575, 340, 40, (200, 160, 40), 1)
                else:
                    curx = write(typedf, 575, 340, 40, (135, 135, 150), 1)
            else:
                curx = write(typedf, 575, 340, 40, textcol, 1)
            write("f(x) = ", 80, 340, 40, (30, 30, 30))
            tfont = pygame.font.Font(None, 40)
            curx += tfont.size(typedf[:cursor])[0]
            if substage == "type":
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(curx, 320, 3, 40))
        else:
            pygame.draw.rect(screen, boxcol, pygame.Rect(160, 230, 830, 80))
            pygame.draw.rect(screen, boxcol, pygame.Rect(160, 350, 830, 80))
            write("f(x) = ", 80, 270, 40, (200, 200, 200))
            write("g(x) = ", 80, 390, 40, (200, 200, 200))
            tfont = pygame.font.Font(None, 40)
            if row == 0:
                if substage == "won":
                    write(typedg, 575, 390, 40, (200, 160, 40), 1)
                    curx = write(typedf, 575, 270, 40, (200, 160, 40), 1)
                else:
                    write(typedg, 575, 390, 40, textcol, 1)
                    curx = write(typedf, 575, 270, 40, textcol, 1)
                curx += tfont.size(typedf[:cursor])[0]
                if substage == "type":
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(curx, 250, 3, 40))
            else:
                if substage == "won":
                    write(typedf, 575, 270, 40, (200, 160, 40), 1)
                    curx = write(typedg, 575, 390, 40, (200, 160, 40), 1)
                else:
                    write(typedf, 575, 270, 40, textcol, 1)
                    curx = write(typedg, 575, 390, 40, textcol, 1)
                curx += tfont.size(typedg[:cursor])[0]
                if substage == "type":
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(curx, 370, 3, 40))
        pygame.draw.rect(screen, boxcol, pygame.Rect(900, 515, 180, 90))
        pygame.draw.rect(screen, boxcol, pygame.Rect(70, 515, 180, 90))
        if substage != "dial":
            write("RUN", 990, 560, 50, textcol)
            write("PASTE", 160, 560, 50, textcol)
        write(f"Lvl. {level}", 90, 40, 40, boxcol)
        write("RESET", 1060, 40, 40, boxcol)
        if dialnum != 0:
            text = dialogues[level-1][dialnum-1]
            if "|" in text:
                texts = text.split("|")
                write(texts[0], 575, 115, 30, textcol)
                write(texts[1], 575, 145, 30, textcol)
            else:
                write(text, 575, 127.5, 30, textcol)
        if substage == "dial":
            write("(click)", 575, 560, 40, boxcol)
    elif stage == "inter":
        screen.fill((235, 225, 225))
        pygame.display.update()
        if level == 6:
            write("The company has started to quickly grow in power.", 575, 108, 40)
            write("We are giving you a new power that allows your inputs to quickly grow too.", 575, 216, 40)
            write("This 'power' is formally called an 'exponent.'", 575, 324, 40)
            write("Type '^' to use it in a machine.", 575, 432, 40)
            write("Use it wisely.", 575, 540, 40)
            chars += "^"
        elif level == 9:
            write("Why? How? What?", 575, 108, 40)
            write("We must now start asking ourselves questions - and using conditions.", 575, 216, 40)
            write("You can now type '==' between two values like 'a' and 'b' to compare them.", 575, 324, 40)
            write("If a is equal to b, a==b is 1. If not, a==b is 0.", 575, 432, 40)
            write("Now get to work.", 575, 540, 40)
            chars += "="
        elif level == 12:
            write("We would say our business is fairly well-rounded.", 575, 108, 40)
            write("Your machines, unfortunately, are not.", 575, 216, 40)
            write("No, they are instead quite cube-like in structure.", 575, 324, 40)
            write("You can now type '[]' to round the number inside the brackets to the nearest integer.", 575, 432, 40)
            write("Hop to it!", 575, 540, 40)
            chars += "[]"
        elif level == 18:
            write("It seems the manager has been cursed again... or, uh... recursed?", 575, 108, 40)
            write("Anyway, you can now use recursion in your machines.", 575, 216, 40)
            write("Simply type f() with an input and it will call itself. f(0) is always 0.", 575, 324, 40)
            write("Two more tools: '{x}' is the floor of x and '<x>' tests whether x is an integer.", 575, 432, 40)
            write("Now hurry up!", 575, 540, 40)
            chars += "f<>{}"
        elif level == 21:
            write("6 is twice as efficient as 3.", 575, 108, 40)
            write("28 is twice as good as 14.", 575, 216, 40)
            write("We now have a brand new function: 'g'", 575, 324, 40)
            write("Use it with f in the next machine.", 575, 432, 40)
            write("Did you like my poem? :-)", 575, 540, 40)
            chars += "g"


#draw_board()
async def main():
    global running, mouse, dialnum, stage, substage, level, dialogues, typedf, typedg, cursor, row
    while running:
        # screen.fill((200, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if substage == "type":
                    run_click()
                elif substage == "dial":
                    if dialnum < len(dialogues[level-1]):
                        dialnum += 1
                    else:
                        substage = "type"
                    draw_board()
                elif substage == "won":
                    if level in [6, 9, 12, 18, 21]:
                        stage = "inter"
                        substage = "none"
                        draw_board()
                    else:
                        level += 1
                        if level == 25:
                            level = 1
                        typedf = ""
                        typedg = ""
                        substage = "dial"
                        dialnum = 0
                        cursor = 0
                        draw_board()
                elif stage == "inter":
                    stage = "level"
                    level += 1
                    typedf = ""
                    typedg = ""
                    substage = "dial"
                    dialnum = 0
                    cursor = 0
                    draw_board()
            elif event.type == pygame.KEYDOWN and substage == "type":
                if event.key == pygame.K_BACKSPACE:
                    if cursor > 0:
                        if row:
                            typedg = typedg[:cursor-1] + typedg[cursor:]
                        else:
                            typedf = typedf[:cursor-1] + typedf[cursor:]
                        cursor -= 1
                elif event.key == pygame.K_DELETE:
                    if row:
                        typedg = typedg[:cursor] + typedg[cursor+1:]
                    else:
                        typedf = typedf[:cursor] + typedf[cursor+1:]
                elif event.key == pygame.K_LEFT:
                    cursor = max(0, cursor-1)
                elif event.key == pygame.K_RIGHT:
                    cursor = min(len(typedf if not row else typedg), cursor+1)
                elif event.key == pygame.K_HOME:
                    cursor = 0
                elif event.key == pygame.K_END:
                    cursor = len(typedf if not row else typedg)
                elif event.unicode in chars and event.unicode != "":
                    if row:
                        typedg = typedg[:cursor] + event.unicode + typedg[cursor:]
                    else:
                        typedf = typedf[:cursor] + event.unicode + typedf[cursor:]
                    cursor += 1
                elif event.unicode == "c":
                    cursor = 0
                    if row:
                        typedg = ""
                    else:
                        typedf = ""
                elif event.key in [pygame.K_DOWN, pygame.K_UP] and level > 21:
                    row = 1 - row
                    cursor = len(typedf if not row else typedg)
                draw_board()
                if event.key == pygame.K_RETURN:
                    run()
        clock.tick(30)
        await asyncio.sleep(0)


asyncio.run(main())
