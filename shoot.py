import pygame
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

pygame.init()

done = False

main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Shooting Game')

font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

background_img = pygame.image.load('resources/image/background.png').convert()

plane_img = pygame.image.load('resources/image/shoot.png').convert_alpha()

player_plane_rect = pygame.Rect(0, 99, 102, 126)

player_plane_img = plane_img.subsurface(player_plane_rect)

player_position = [189, 600]

old_player_rect = pygame.Rect(player_position[0],player_position[1], 102, 126)

new_player_rect = None

while not done:
    active_rect_list = []

    main_screen.fill(0)
    main_screen.blit(background_img, (0, 0))

    player_position[1] = player_position[1] - 1
    main_screen.blit(player_plane_img, player_position)

    new_player_rect = old_player_rect.move(0, -1)

    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    main_screen.blit(fps, (50, 50))

    active_rect_list.append(old_player_rect)
    active_rect_list.append(new_player_rect)
    #active_rect_list.append(pygame.Rect(50,50,30,10))

    print('old:', old_player_rect)
    print('new:', new_player_rect)


    pygame.display.update([(0,0,50,50)])
    clock.tick()

    old_player_rect = new_player_rect

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.quit()
sys.exit()
