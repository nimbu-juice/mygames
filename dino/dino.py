import pygame
from random import randint

pygame.init()

# setup
WIDTH, HEIGHT = 567, 300
window = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font('dino/PressStart2P-Regular.ttf', 10)
pygame.display.set_caption("Dino Game")
icon = pygame.image.load('dino/cactusicon.png')
pygame.display.set_icon(icon)


cactus = pygame.image.load('dino/tree.png').convert_alpha()
cactus = pygame.transform.rotozoom(cactus, 0, 0.15)
flying = pygame.image.load('dino/meteor.png').convert_alpha()
flying = pygame.transform.rotozoom(flying, 0, 0.15)

cloud = pygame.image.load('dino/cloud.png').convert_alpha()
cloud = pygame.transform.rotozoom(cloud, 0, 0.5)

dino_walk_1 = pygame.image.load('dino/dino1.png').convert_alpha()
dino_walk_1 = pygame.transform.rotozoom(dino_walk_1, 0, 0.6)
dino_walk_2 = pygame.image.load('dino/dino2.png').convert_alpha()
dino_walk_2 = pygame.transform.rotozoom(dino_walk_2, 0, 0.6)
dino_walk_3 = pygame.image.load('dino/dino3.png').convert_alpha()
dino_walk_3 = pygame.transform.rotozoom(dino_walk_3, 0, 0.6)

dino_duck_1 = pygame.image.load('dino/dinoduck1.png').convert_alpha()
dino_duck_1 = pygame.transform.rotozoom(dino_duck_1, 0, 0.6)
dino_duck_2 = pygame.image.load('dino/dinoduck2.png').convert_alpha()
dino_duck_2 = pygame.transform.rotozoom(dino_duck_2, 0, 0.6)

dino_dead = pygame.image.load('dino/dinodead.png').convert_alpha()
dino_dead = pygame.transform.rotozoom(dino_dead, 0, 0.6)

dino_duck = [dino_duck_1, dino_duck_2]
dino_duck_index = 0
dino_duck_frame = dino_duck[dino_duck_index]

dino_walk = [dino_walk_1, dino_walk_2, dino_walk_3]
dino_index = 0
dino = dino_walk[dino_index]
dino_rect = dino.get_rect(midbottom=(70, 185))
dino_gravity = 0
dino_ducking = False
dino_hitbox = dino_rect


def dino_animation():
    global dino, dino_index, dino_ducking, dino_dead, game_active
    global dino_duck_index, dino_duck, dino_duck_frame, dino_hitbox, dino_rect
    if game_active:
        if dino_rect.bottom < 185:
            dino = dino_walk_1
            dino_hitbox = dino_rect
        else:
            if dino_ducking:
                dino_duck_index += 0.2
                if dino_duck_index >= len(dino_duck):
                    dino_duck_index = 0
                dino_duck_frame = dino_duck[int(dino_duck_index)]
                dino = dino_duck_frame
                dino_hitbox = dino_rect.inflate(0, -3)

            else:
                dino_index += 0.3
                if dino_index >= len(dino_walk):
                    dino_index = 0
                dino = dino_walk[int(dino_index)]
                dino_hitbox = dino_rect
    else:
        dino = dino_dead


play = pygame.image.load('dino/restart.png').convert_alpha()
play = pygame.transform.rotozoom(play, 0, 0.7)
play_rect = play.get_rect(center=(WIDTH/2, HEIGHT/2))


background = pygame.image.load('dino/dinogamebg.png').convert_alpha()

obstacle_rect_list = []
cloud_rect_list = []
game_active = True
white = (255, 255, 255)

score = 0
start_time = 0
speed = 4


def print_score():
    global score
    score = int((pygame.time.get_ticks() - start_time)/100)
    text_surface = font.render('Score: ' + str(score), True, (0, 0, 0))
    text_rect = text_surface.get_rect(midbottom=(WIDTH-80, 50))
    window.blit(text_surface, text_rect)


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= speed
            if obstacle_rect.bottom == 185:
                window.blit(cactus, obstacle_rect)
            else:
                window.blit(flying, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def cloud_movement(cloud_list):
    global cloud
    if cloud_list:
        for cloud_rect in cloud_list:
            cloud_rect.x -= 3
            window.blit(cloud, cloud_rect)

        cloud_list = [cloud for cloud in cloud_list if cloud.x > -100]

        return cloud_list
    else:
        return []


def collisions(dino, obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if dino.colliderect(obstacles_rect):
                return False
    return True


obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


FPS = pygame.time.Clock()

x = 0

while True:
    while speed < 6:
        speed += 0.000001
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            dino_ducking = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dino_rect.bottom >= 185:
                    dino_gravity = -9
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN]:
            dino_ducking = True

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    obstacle_rect_list.clear()
                    cloud_rect_list.clear()
                    dino_rect.y = 185
                    game_active = True
                    start_time = pygame.time.get_ticks()

        if event.type == obstacle_timer:
            random = randint(0, 3)
            if random == 0 or random == 1:
                obstacle_rect_list.append(cactus.get_rect(midbottom=(randint(900, 1100), 185)))
            elif random == 2:
                obstacle_rect_list.append(flying.get_rect(midbottom=(randint(900, 1100), 100)))
            elif random == 3:
                obstacle_rect_list.append(flying.get_rect(midbottom=(randint(900, 1100), 135)))
            cloud_rect_list.append(cloud.get_rect(midbottom=(randint(1300, 1500), 70)))
    if game_active:
        window.fill(white)

        rel_x = x % background.get_rect().width
        window.blit(background, (rel_x - background.get_rect().width, 51))
        if rel_x < WIDTH:
            window.blit(background, (rel_x, 51))
        x -= speed

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        cloud_rect_list = cloud_movement(cloud_rect_list)
        print_score()

        # dino physics
        dino_gravity += 0.4
        dino_rect.y += dino_gravity
        if dino_rect.bottom > 185:
            dino_rect.bottom = 185
# 185
        game_active = collisions(dino_hitbox, obstacle_rect_list)
        dino_animation()
        window.blit(dino, dino_rect)
        pygame.display.update()
    else:
        window.blit(play, play_rect)
        pygame.display.update()

    FPS.tick(60)
