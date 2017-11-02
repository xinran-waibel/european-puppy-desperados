import os, sys
import pygame
import random
import player
import entity_manager
import level
import vector
import values
import levels
import animation

SCREENRECT = pygame.Rect(0, 0, 640, 640)
pt_FPS = 60

black = 0, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
red = 255, 0, 0

def update(screen, entity_manager, level):
    
    # handle level collisions
    entity_manager.collide(level)
    # update all the entities
    entity_manager.update()
    # move viewport
    if not (entity_manager.player is None):
        level.set_cam_pos(entity_manager.player.body.center[0], entity_manager.player.body.center[1])

def main(winstyle = 0):
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    values.screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    values.entity_manager = entity_manager.entity_manager()
    values.entity_manager.load_next_level();
    values.entity_manager.level = values.level
    values.entity_manager.spawn_entities(values.level)

    theme = pygame.mixer.Sound( "sounds/DST-1990.wav" )
    theme.play(-1)
   
    heartimage = animation.animated_image("graphics/heart.png", 18, 17)
    bulletimage = animation.animated_image("graphics/bullet.png", 31, 11)

    while 1:

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    values.mouse.on_mouse_down()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    values.mouse.on_mouse_down()
    
        # update game state
        update(values.screen, values.entity_manager, values.level)
              
        # draw the game world
        values.screen.fill(black)
        values.level.draw(values.screen)        
        values.entity_manager.draw(values.screen)
        
        heart_rect = heartimage.get_image(0).get_rect()
        heartSurface = pygame.transform.scale(heartimage.get_image(0), (36,34))
        heart_rect.top = 48
        heart_rect.left = 20
        for x in range(values.entity_manager.player.hp):
            heart_rect.left += 38
            values.screen.blit(heartSurface, heart_rect)
        
        bullet_rect = bulletimage.get_image(0).get_rect()
        bullet_surface = pygame.transform.scale(bulletimage.get_image(0), (36,16))
        bullet_rect.top = 96
        bullet_rect.left = 20
        for x in range(values.entity_manager.player.nofshots):
            bullet_rect.left += 38
            values.screen.blit(bullet_surface, bullet_rect)

        # display drawn screen
        pygame.display.flip()
        
        # update utilities
        values.mouse.update()
        values.clock.tick(pt_FPS)
        values.change_time()

main()
