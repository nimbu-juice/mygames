import pygame
from random import randint

pygame.init()

width, height = (600, 400)

window = pygame.display.set_mode((width, height))

icon = pygame.image.load('retro/pong/pongicon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Pong Game")


black = (0, 0, 0)
white = (255, 255, 255)
grey = (71, 57, 57)

ball = pygame.image.load('retro/pong/pong.png').convert_alpha()
ball = pygame.transform.scale(ball, (30, 30))
ball_rect = ball.get_rect(center=(width/2, height/2))

# ball speed (tan y/x = 45 deg)
ball_x = 5
ball_y = 5

paddle1 = pygame.image.load('retro/pong/pongpaddle.png').convert_alpha()
paddle1_rect = paddle1.get_rect(center=(555, height/2))

paddle2 = pygame.image.load('retro/pong/pongpaddle.png').convert_alpha()
paddle2_rect = paddle2.get_rect(center=(45, height/2))

font = pygame.font.Font('retro/pong/Pixeltype.ttf', 40)

title_surface = font.render('PONG', False, white)
title_rect = title_surface.get_rect(center=(300, 50))

multi_surface = font.render('Local Multiplayer', False, white)
multi_rect = multi_surface.get_rect(center=(300, 200))

AI_surface = font.render('AI Singleplayer', False, white)
AI_rect = AI_surface.get_rect(center=(300, 250))

score_1 = 0
score_2 = 0


def print_score(score, x, y):
    value = font.render('' + str(score), False, white)
    window.blit(value, [x, y])


FPS = pygame.time.Clock()

gameplay = False
AI = False


def homescreen():

    global gameplay
    global AI

    while not gameplay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if multi_rect.collidepoint(event.pos):
                    gameplay = True
                    AI = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AI_rect.collidepoint(event.pos):
                    gameplay = True
                    AI = True
        window.fill(black)
        window.blit(title_surface, title_rect)
        pygame.draw.rect(window, grey, multi_rect)
        pygame.draw.rect(window, grey, AI_rect)
        window.blit(multi_surface, multi_rect)
        window.blit(AI_surface, AI_rect)
        pygame.display.update()


def gameloop():
    x_list = [3, 4, 5, 6]
    global AI
    global gameplay
    global ball_x
    global ball_y
    global score_1
    global score_2
    gameover = False
    game_end = True
    wait = 90
    timer = 0
    ball_rect.x = width / 2
    ball_rect.y = height / 2

    while not gameover:
        window.fill((0, 0, 0))

        if game_end:
            ball_rect.x = width/2
            ball_rect.y = height/2
            for num in range(len(x_list)):
                x_list[num] = abs(x_list[num])

            timer += 1
            if timer == wait:
                ball_x = 5
                ball_y = 5
                game_end = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # ball collision with paddle

        if ball_rect.colliderect(paddle1_rect):
            for num in range(len(x_list)):
                x_list[num] = x_list[num] * -1
            ball_x = x_list[randint(0, 3)]

        if ball_rect.colliderect(paddle2_rect):
            for num in range(len(x_list)):
                x_list[num] = x_list[num] * -1
            ball_x = x_list[randint(0, 3)]

        # player 1 input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not paddle1_rect.y < 0:
            paddle1_rect.y -= 4
        if keys[pygame.K_DOWN] and not paddle1_rect.y > 315:
            paddle1_rect.y += 4

        # player 2 input
        if not AI:
            if keys[pygame.K_w] and not paddle2_rect.y < 0:
                paddle2_rect.y -= 4
            if keys[pygame.K_s] and not paddle2_rect.y > 315:
                paddle2_rect.y += 4
        else:
            if ball_rect.y < paddle2_rect.y:
                paddle2_rect.y -= 4
            if ball_rect.y > paddle2_rect.y:
                paddle2_rect.y += 4

        # ball
        window.blit(ball, ball_rect)
        ball_rect.x += ball_x
        ball_rect.y += ball_y
        # ball ceiling collision
        if ball_rect.bottom > height or ball_rect.top < 0:
            ball_y = -ball_y

        if ball_rect.right > width:
            score_2 += 1
            timer = 0
            game_end = True
        if ball_rect.left < 0:
            score_1 += 1
            timer = 0
            game_end = True
        window.blit(paddle1, paddle1_rect)
        window.blit(paddle2, paddle2_rect)
        print_score(score_1, 425, 10)
        print_score(score_2, 175, 10)
        pygame.display.update()

        FPS.tick(60)

    pygame.quit()
    quit()


homescreen()
gameloop()
