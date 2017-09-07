import pygame
import sys
import random
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
PLAYER_INIT_POSITION = [189, 600]
PLAYER_PLANE_ANIMATE_FREQ = 6
PLAYER_PLANE_EXPLODE_ANIMATE_FREQ = 20
player_animate_counter = 0
player_explode_animate_counter = 2 * PLAYER_PLANE_EXPLODE_ANIMATE_FREQ

PLAYER_SHOOT_FREQ = 8
player_shoot_counter = 0
bullet_available = True

pygame.init()

done = False

main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Shooting Game')

from component_class import *

font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

BACKGROUND_IMG = pygame.image.load('resources/image/background.png').convert()

player = Player(PLAYER_INIT_POSITION)


main_screen.fill(0)
main_screen.blit(BACKGROUND_IMG, (0, 0))
pygame.display.update()

while not done:
    # Limit the fps to 60.
    clock.tick(60)

    # Draw the background image
    main_screen.fill(0)
    main_screen.blit(BACKGROUND_IMG, (0, 0))

    # For displaying FPS on top left corner.
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    main_screen.blit(fps, (50, 50))

    player_animate_counter += 1
    if player_animate_counter >= 2 * PLAYER_PLANE_ANIMATE_FREQ:
        player_animate_counter = 0


    if not bullet_available:
        player_shoot_counter += 1
    if player_shoot_counter >= PLAYER_SHOOT_FREQ:
        bullet_available = True
        player_shoot_counter = 0

    # Key press event tracking
    if not player.got_hit:
        key_press = pygame.key.get_pressed()
        if key_press[K_UP]:
            player.moveUp()
        if key_press[K_DOWN]:
            player.moveDown()
        if key_press[K_LEFT]:
            player.moveLeft()
        if key_press[K_RIGHT]:
            player.moveRight()
        if key_press[K_SPACE]:
            if bullet_available:
                player.shoot('SINGLE_NORMAL')
                bullet_available = False

    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom <= 0:
            player.bullets.remove(bullet)

    # Draw the player plane with animation
    if not player.got_hit:
        player.img_index = player_animate_counter // PLAYER_PLANE_ANIMATE_FREQ
        main_screen.blit(player.image[player.img_index], player.rect)
    else:
        player.img_index = player_explode_animate_counter // PLAYER_PLANE_EXPLODE_ANIMATE_FREQ
        main_screen.blit(player.image[player.img_index], player.rect)
        player_explode_animate_counter += 1
        if player_explode_animate_counter >= len(player.image) * PLAYER_PLANE_EXPLODE_ANIMATE_FREQ:
            player_explode_animate_counter = 0
            done = True

    player.bullets.draw(main_screen)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.quit()
sys.exit()
