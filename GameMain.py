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

PLAYER_SHOOT_FREQ = 10
player_shoot_counter = 0
bullet_available = True


ENEMY_INITIAL_SPAWN_FREQ = 30
enemy_spwan_freq = 30
ENEMY_EXPLODE_ANIMATE_FREQ = 10
enemy_spawn_counter = 0
enemies = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()
enemy = None

score = 0

pygame.init()

# Music and sound loading
PLAYER_SHOOT_SOUND = pygame.mixer.Sound('resources/sound/bullet.wav')
ENEMY_EXPLODE_SOUND = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
GAME_OVER_SOUND = pygame.mixer.Sound('resources/sound/game_over.wav')
PLAYER_SHOOT_SOUND.set_volume(0.3)
ENEMY_EXPLODE_SOUND.set_volume(0.3)
GAME_OVER_SOUND.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

done = False

main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Shooting Game')

from component_class import *

fps_font = pygame.font.Font(None, 30)
in_game_score_font = pygame.font.Font(None, 40)
game_over_score_font = pygame.font.Font(None, 70)

clock = pygame.time.Clock()

BACKGROUND_IMG = pygame.image.load('resources/image/background.png').convert()
GAME_OVER_IMG = pygame.image.load('resources/image/gameover.png')


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
    fps = fps_font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    main_screen.blit(fps, (50, 50))

    player_animate_counter += 1
    if player_animate_counter >= 2 * PLAYER_PLANE_ANIMATE_FREQ:
        player_animate_counter = 0

    if not bullet_available:
        player_shoot_counter += 1
    if player_shoot_counter >= PLAYER_SHOOT_FREQ:
        bullet_available = True
        player_shoot_counter = 0


    # Spawn enemy in a certain frequency, which increases with the score.
    if enemy_spwan_freq > 5:
        enemy_spwan_freq = ENEMY_INITIAL_SPAWN_FREQ - score // 10000

    enemy_spawn_counter += 1
    if enemy_spawn_counter >= enemy_spwan_freq:
        enemy_spawn_counter = 0
        enemy = Enemy('SMALL')
        enemies.add(enemy)

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
                PLAYER_SHOOT_SOUND.play()
                bullet_available = False

    if not player.got_hit is True:
        # For bullet out of screen, remove them
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom <= 0:
                player.bullets.remove(bullet)

        # Move enemry and see if it crashed on player or out of screen
        for enemy in enemies:
            enemy.move()
            if pygame.sprite.collide_mask(enemy, player):
                player.got_hit = True
                GAME_OVER_SOUND.play()
                enemies_down.add(enemy)
                enemies.remove(enemy)
            if enemy.rect.top >= SCREEN_HEIGHT:
                enemies.remove(enemy)
        # Find enemies planes that got hit by bullets
        enemies_got_hit = pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)

        for enemy in enemies_got_hit.keys():
            ENEMY_EXPLODE_SOUND.play()
            enemies_down.add(enemy)

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
    enemies.draw(main_screen)

    # Draw animation of enermy explosion
    for enemy in enemies_down:
        if enemy.explode_img_index == 0:
            score += 1000
        if enemy.explode_img_index >= len(enemy.explode_image) * ENEMY_EXPLODE_ANIMATE_FREQ:
            enemies_down.remove(enemy)
        else:
            index = enemy.explode_img_index // ENEMY_EXPLODE_ANIMATE_FREQ
            main_screen.blit(enemy.explode_image[index], enemy.rect)
            enemy.explode_img_index += 1


    # For displaying score on top right corner.
    score_text = in_game_score_font.render(str(score), True, pygame.Color('white'))
    main_screen.blit(score_text, (300, 50))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

# Display Game Over Image
main_screen.blit(GAME_OVER_IMG, (0, 0))

# Display Final score in center of screen
final_score_text = game_over_score_font.render('Score: '+ str(score), True, pygame.Color('white'))
text_rect = final_score_text.get_rect()
text_rect.centerx = main_screen.get_rect().centerx
text_rect.centery = main_screen.get_rect().centery + 30
main_screen.blit(final_score_text, text_rect)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
