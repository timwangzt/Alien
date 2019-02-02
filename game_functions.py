import sys
import pygame

from settings import Settings
from bullet import Bullet
from alien import Alien

def check_KEYDOWN_events(event, ai_settings, screen, ship, bullets):
#reponse to keyboard and mouse's events"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
       fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_KEYUP_events(event, ship):
#reponse to keyboard and mouse's events"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
#reponse to keyboard and mouse's events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_KEYDOWN_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_KEYUP_events(event, ship)

def update_screen(ai_screen, screen, ship, aliens, bullets):
    screen.fill(ai_screen.bg_color)

    for bullet in bullets:
        bullet.draw_bullet()

    ship.blitme()

    aliens.draw(screen)


    # the latest screen visisuable
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):

    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #  print(len(bullets))
    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # print(len(aliens))
    if len(aliens) == 0:
        bullets.empty
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullets(ai_settings, screen, ship, bullets):
    # create a bullet and add it into bullets
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):

    alien = Alien(ai_settings,screen)
    number_alien_x = get_number_alien_x(ai_settings,alien)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)

def get_number_alien_x(ai_settings, alien):
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2* alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):

    available_space_y = ai_settings.screen_height - (3 * alien_height + ship_height)
    number_rows = int(available_space_y / (alien_height * 2))
    return  number_rows

def update_aliens(ai_settings, aliens):

    check_fleet_edges(ai_settings,aliens)
    aliens.update()

def check_fleet_edges(ai_setting, aliens):

    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_setting, aliens)

    for alien in aliens.copy():
        if alien.check_out_screen():
            aliens.remove(alien)

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1

