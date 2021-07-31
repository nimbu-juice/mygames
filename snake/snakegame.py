import pygame
import random

pygame.init()

width, height = (600, 400)

window = pygame.display.set_mode((width, height))

pygame.display.set_caption("Snake Game")
icon = pygame.image.load('retro/snake/snake.png')
pygame.display.set_icon(icon)
font_style = pygame.font.SysFont("Arial", 25)

text_surface = font_style.render('Click P to play again', True, (255, 255, 255))
text_rect = text_surface.get_rect(midbottom=(width/2, height/2))

snake_block = 10


def your_score(score):
    value = font_style.render("" + str(score), True, (255, 255, 255))
    window.blit(value, [250, 0])

def snake(snake_block, snake_list):
    for i in snake_list:
        pygame.draw.rect(window, (255, 255, 255), [i[0], i[1], snake_block, snake_block])


FPS = pygame.time.Clock()


def game_loop():
    game_over = False
    game_close = False

    x1 = width/2
    y1 = height/2

    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            window.fill((0, 0, 0))
            window.blit(text_surface, text_rect)
            your_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_loop()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != 10:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -10:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -10:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_UP and y1_change != 10:
                    y1_change = -snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        window.fill((0, 0, 0))
        pygame.draw.rect(window, (255, 255, 255), [food_x, food_y, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_Head:
                game_close = True

        snake(snake_block, snake_list)
        your_score(snake_length - 1)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(10, width-10) / 10.0) * 10.0
            food_y = round(random.randrange(10, height-10) / 10.0) * 10.0
            snake_length += 1

        FPS.tick(15)

    pygame.quit()
    quit()


game_loop()

# SNAKE GAME DON'T EDIT
