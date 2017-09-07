import pygame
import sys
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
MOVE_DISTANCE = 5
PLAYER_PLANE_SIZE = (102, 126)

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

new_player_rect = old_player_rect

main_screen.fill(0)
main_screen.blit(background_img, (0, 0))
pygame.display.update()

while not done:
    active_rect_list = []

    main_screen.fill(0)
    main_screen.blit(background_img, (0, 0))

    # Key press event tracking
    key_press = pygame.key.get_pressed()
    if key_press[K_UP]:
        player_position[1] -= MOVE_DISTANCE
    if key_press[K_DOWN]:
        player_position[1] += MOVE_DISTANCE
    if key_press[K_LEFT]:
        player_position[0] -= MOVE_DISTANCE
    if key_press[K_RIGHT]:
        player_position[0] += MOVE_DISTANCE

    if player_position[0] < 0:
        player_position[0] = 0
    if player_position[0] > SCREEN_WIDTH - PLAYER_PLANE_SIZE[0]:
        player_position[0] = SCREEN_WIDTH - PLAYER_PLANE_SIZE[0]
    if player_position[1] < 0:
        player_position[1] = 0
    if player_position[1] > SCREEN_HEIGHT - PLAYER_PLANE_SIZE[1]:
        player_position[1] = SCREEN_HEIGHT - PLAYER_PLANE_SIZE[1]

    new_player_rect = pygame.Rect(player_position, PLAYER_PLANE_SIZE)

    #new_player_rect = old_player_rect.move(0, -MOVE_DISTANCE)
    #player_position[1] = player_position[1] - MOVE_DISTANCE
    main_screen.blit(player_plane_img, player_position)

    # For displaying FPS on top left corner.
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    main_screen.blit(fps, (50, 50))

    # Only update the rects that got changed, for performance optimization.
    active_rect_list.append(old_player_rect)
    active_rect_list.append(new_player_rect)
    active_rect_list.append(pygame.Rect(50,50,100,100))

    #print('old:', old_player_rect)
    #print('new:', new_player_rect)

    pygame.display.update(active_rect_list)
    clock.tick(60)

    old_player_rect = new_player_rect

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.quit()
sys.exit()
