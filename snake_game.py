import pygame
import time
import random

pygame.init()

width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 102)
purple = (138, 43, 226)

clock = pygame.time.Clock()
snake_block = 10
initial_speed = 15
font = pygame.font.SysFont("bahnschrift", 25)

def message(msg, color, y=None):
    mesg = font.render(msg, True, color)
    pos_y = y if y else height / 3
    win.blit(mesg, [width / 6, pos_y])

def show_score(score):
    value = font.render("Score: " + str(score), True, red)
    win.blit(value, [0, 0])

def show_high_score(high_score):
    value = font.render("High Score: " + str(high_score), True, green)
    win.blit(value, [width - 180, 0])

def show_level(score):
    level = (score // 10) + 1
    value = font.render("Level: " + str(level), True, blue)
    win.blit(value, [width // 2 - 50, 0])

def show_length(length):
    value = font.render("Length: " + str(length), True, purple)
    win.blit(value, [0, 30])

def show_help():
    lines = [
        "Use arrow keys to move.",
        "Press P to pause/resume.",
        "Eat green food: +1 point.",
        "Eat yellow food: +3 points.",
        "Avoid purple obstacles.",
        "Press H to toggle this help.",
        "Press M to return to main menu."
    ]
    for i, line in enumerate(lines):
        message(line, black, 40 + i * 30)

def draw_menu():
    win.fill(white)
    message("SNAKE GAME", blue, 70)
    message("Press S to Start | H for Help | Q to Quit", black, 150)
    pygame.display.update()

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(win, purple, [obs[0], obs[1], snake_block, snake_block])

def draw_food(foodx, foody, color=green):
    pygame.draw.rect(win, color, [foodx, foody, snake_block, snake_block])

def pause():
    paused = True
    while paused:
        win.fill(white)
        message("Game Paused. Press P to Resume.", blue)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        clock.tick(5)

def multi_message(msgs, color, start_y=80, spacing=35):
    for i, l in enumerate(msgs):
        mesg = font.render(l, True, color)
        win.blit(mesg, [width // 2 - mesg.get_width() // 2, start_y + i * spacing])


def gameLoop(high_score):
    game_over = False
    game_close = False
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    show_help_overlay = False

    
    obstacles = []
    for _ in range(10):
        ox = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        oy = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
        obstacles.append((ox, oy))

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    bonus_food = None
    bonus_timer = 0
    bonus_interval = 50

    score = 0

    while not game_over:
        while game_close:
            win.fill(black)
            multi_message([
                "You Lost!",
                "Press Q to Quit",
                "C to Play Again",
                "M for Menu"
            ], red, start_y=80, spacing=35)
            show_score(score)
            show_high_score(high_score)
            show_level(score)
            show_length(Length_of_snake)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return high_score
                    if event.key == pygame.K_m:
                        return 'menu'


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block; y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block; y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block; x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block; x1_change = 0
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_h:
                    show_help_overlay = not show_help_overlay
                elif event.key == pygame.K_m:
                    return 'menu'

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        if (x1, y1) in obstacles:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        win.fill(white)
        draw_obstacles(obstacles)

        draw_food(foodx, foody, green)
        if bonus_food:
            draw_food(*bonus_food, yellow)

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for block in snake_List:
            pygame.draw.rect(win, black, [block[0], block[1], snake_block, snake_block])

        if show_help_overlay:
            show_help()

        show_score(score)
        show_high_score(high_score)
        show_level(score)
        show_length(Length_of_snake)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1

        bonus_timer += 1
        if bonus_timer > bonus_interval:
            bonus_food = (
                round(random.randrange(0, width - snake_block) / 10.0) * 10.0,
                round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            )
            bonus_timer = 0

        if bonus_food and x1 == bonus_food[0] and y1 == bonus_food[1]:
            score += 3
            Length_of_snake += 2
            bonus_food = None

        if score > high_score:
            high_score = score

        snake_speed = initial_speed + (score // 5)
        clock.tick(snake_speed)

    pygame.quit()
    quit()

def main_menu():
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(); quit()
                elif event.key == pygame.K_h:
                    win.fill(white)
                    show_help()
                    pygame.display.update()
                    time.sleep(3)
                elif event.key == pygame.K_s:
                    return


high_score = 0
while True:
    main_menu()
    result = gameLoop(high_score)
    if result == 'menu':
        continue
    elif isinstance(result, int):
        high_score = result
