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

clock = pygame.time.Clock()
snake_block = 10
initial_speed = 15
font = pygame.font.SysFont("bahnschrift", 25)

def message(msg, color):
    mesg = font.render(msg, True, color)
    win.blit(mesg, [width / 6, height / 3])

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

def pause():
    paused = True
    while paused:
        win.fill(white)
        message("Game Paused. Press P to Resume.", blue)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        clock.tick(5)

def gameLoop(high_score):
    game_over = False
    game_close = False
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            win.fill(black)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            show_score(Length_of_snake - 1)
            show_high_score(high_score)
            show_level(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return high_score  # End game and return score for next session

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause()

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        win.fill(white)
        pygame.draw.rect(win, green, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for block in snake_List:
            pygame.draw.rect(win, black, [block[0], block[1], snake_block, snake_block])

        current_score = Length_of_snake - 1
        if current_score > high_score:
            high_score = current_score

        show_score(current_score)
        show_high_score(high_score)
        show_level(current_score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        snake_speed = initial_speed + (Length_of_snake // 5)
        clock.tick(snake_speed)

    pygame.quit()
    quit()

high_score = 0
while True:
    high_score = gameLoop(high_score)
