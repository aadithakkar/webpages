import pygame, sys, random, asyncio

pygame.init()

screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("Monkey Typing")

def draw_screen(screen, phrase, gen, mode, targ, mr, pg, cs, sel):
    screen.fill((200, 200, 200))
    if mode == 0:
        mrs = str(mr) + "%"
        bl = ["Off", "Normal", "By Letter"][cs]
        write("Infinite Monkey Simulator", (400, 150), (0, 0, 0), 60, screen)
        write(f"Target Phrase: {targ}", (400, 500), (0, 0, 0) if sel != 1 else (100, 100, 100), 40, screen)
        write(f"Offspring Per Generation: {pg}", (400, 575), (0, 0, 0) if sel != 2 else (100, 100, 100), 40, screen)
        write(f"Mutation Rate: {mrs}", (400, 650), (0, 0, 0) if sel != 3 else (100, 100, 100), 40, screen)
        write(f"Cumulative Selection: {bl}", (400, 725), (0, 0, 0), 40, screen)
    else:
        write(phrase, (400, 400), (0, 0, 0), 40, screen)
        write(gen, (400, 200), (0, 0, 0), 50, screen)

all_sprites = pygame.sprite.LayeredUpdates()

def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))

def score(old, target, byletter):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    count = 0
    for i in range(len(old)):
        if not byletter:
            if old[i] == target[i]:
                count += 1
        else:
            count -= (alpha.index(old[i]) - alpha.index(target[i])) ** 2
    return count

def mutate(old, mr, alpha, byletter):
    if byletter:
        return "".join([alpha[max(0, min(26, alpha.index(old[i]) + random.choice([-1, 1])))] if random.random() < mr / 100 else old[i] for i in range(len(old))])
    return ("".join([random.choice(alpha) if random.random() < mr / 100 else old[i] for i in range(len(old))]))

def new_phrase(old, target, alpha, mr, per_gen, bl):
    # return "".join([random.choice(alpha) for _ in range(len(old))])
    closest = old
    closest_score = score(old, target, bl)
    for _ in range(per_gen):
        mutation = mutate(old, mr, alpha, bl)
        mutant_score = score(mutation, target, bl)
        if mutant_score > closest_score:
            closest = mutation
            closest_score = mutant_score
    return closest
    return "".join([random.choice(alpha) for _ in range(len(old))])

async def main():
    running = True
    clock = pygame.time.Clock()
    target = "MONKEYS"
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    length = len(target)
    phrase = "".join([random.choice(alpha) for _ in range(length)])
    generation = 0
    mode = 0
    mutation_rate = 20
    per_gen = 500
    cumulative = 1
    selected = 0
    while running:
        if mode == 1 and phrase != target:
            if not cumulative:
                phrase = "".join([random.choice(alpha) for _ in range(length)])
            else:
                phrase = new_phrase(phrase, target, alpha, mutation_rate, per_gen, cumulative - 1)
            generation += 1
        all_sprites.update()
        draw_screen(screen, phrase, generation, mode, target, mutation_rate, per_gen, cumulative, selected)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected = 0
                my = pygame.mouse.get_pos()[1]
                if 470 < my < 530:
                    selected = 1
                elif 545 < my < 605:
                    selected = 2
                elif 620 < my < 680:
                    selected = 3
                elif 695 < my < 755:
                    cumulative = (cumulative + 1) % 3
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if selected == 1 and len(target) > 0:
                        target = target[:-1]
                    elif selected == 2:
                        per_gen = per_gen // 10
                    elif selected == 3:
                        mutation_rate = mutation_rate // 10
                elif event.key == pygame.K_DELETE:
                    if selected == 1:
                        target = ""
                elif event.key == pygame.K_RETURN:
                    selected = 0
                    mode = 1 - mode
                    length = len(target)
                    phrase = "".join([random.choice(alpha) for _ in range(length)])
                    generation = 0
                elif event.unicode != "":
                    if selected == 1 and event.unicode.upper() in alpha and len(target) < 35:
                        target += event.unicode.upper()
                    elif selected == 2 and event.unicode in "1234567890" and per_gen < 1000:
                        per_gen *= 10
                        per_gen += int(event.unicode)
                    elif selected == 3 and event.unicode in "1234567890" and mutation_rate < 10:
                        mutation_rate *= 10
                        mutation_rate += int(event.unicode)
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
