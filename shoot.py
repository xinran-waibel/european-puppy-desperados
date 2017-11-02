import entity
import pygame
import types
import values
import vector
import math
import tiledtmxloader
import animation

class shoot(entity.entity):
    def __init__(self,posX,posY,direction,group):
        super().__init__(posX,posY)
        self.velocity.x = direction * self.speed*3
        self.heading=direction
        self.group=group
        
        self.speed = .5

        self.body.width = 26
        self.body.height = 14
        self.image = None
        self.sprite = None

        if(group == 1):
            self.image = animation.animated_image("graphics/shoot_puppy.png", 26, 14);
            rect = self.image.get_image(0).get_rect()
            rect.topleft = (posX, posY)
            self.sprite = tiledtmxloader.helperspygame.SpriteLayer.Sprite(self.image.get_image(0), rect)
        else:
            self.body.width = 34
            self.body.height = 17
            self.image = animation.animated_image("graphics/shoot_mice.png", 34, 17);
            rect = self.image.get_image(0).get_rect()
            rect.topleft = (posX, posY)
            self.sprite = tiledtmxloader.helperspygame.SpriteLayer.Sprite(self.image.get_image(0), rect)
    
        self.sprite.image = pygame.transform.flip(self.image.get_image(0), self.heading == -1, False)


    def on_collide_left(self, other = None):
        if other!=None:
            if(self.group!=other.group):
                other.die()
                self.die()
        else:
            self.die()

    def on_collide_right(self, other = None):
        if other!=None:
            if(self.group!=other.group):
                other.die()
                self.die()
        else:
            self.die()
            
    def on_collide_up(self, other = None):
        if other!=None:
            if(self.group!=other.group):
                other.die()
                self.die()
        else:
            self.die()
            
    def on_collide_down(self, other = None):
        if other!=None:
            if(self.group!=other.group):
                other.die()
                self.die()
        else:
            self.die()

    def hit_with(self, other):
        if other!=None:
            if(self.group!=other.group):
                other.die()
                self.die()
        else:
            self.die()

    def update(self):
        self.velocity.x = self.speed*self.heading*values.delta_time
        self.move(self.velocity)
    
