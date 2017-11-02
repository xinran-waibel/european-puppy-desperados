import entity
import pygame
import types
import values
import vector
import math
import shoot
import mice
import cheese
import time
import entity_manager
import tiledtmxloader
import animation

class player( entity.entity ):
    def __init__( self, posX, posY ):
        super().__init__( posX, posY )
        self.is_player = True
        
        self.group = 1;

        self.jump_power = 13;
        self.speed = .32

        self.nofshots=3
        self.hp=3
        self.t1=time.time()
        self.t2=None

        self.shootDelayTime = 1200
        self.shootDelay = 0

        self.damageDelayTime = 125
        self.damageDelay = 0
        self.damagePulses = 6
        self.pulsesLeft = 0
        
        self.shootSound = pygame.mixer.Sound( "sounds/shoots.wav" )
        self.shootSound.set_volume(.4)
        self.jumpSound = pygame.mixer.Sound( "sounds/cartoon-jump.wav" )
        self.jumpSound.set_volume(.125)
        self.hurtSound = pygame.mixer.Sound( "sounds/puppyhurt.wav" )
        self.deathSound = pygame.mixer.Sound( "sounds/puppydead.wav" )

        self.heading = 1
        self.body.width = 38
        self.body.height = 53

        self.image = animation.animated_image("graphics/puppy_desperado.png", 57, 54);
        rect = self.image.get_image(0).get_rect()
        rect.topleft = (posX, posY)
        self.sprite = tiledtmxloader.helperspygame.SpriteLayer.Sprite(self.image.get_image(0), rect)
        
    def die(self):
        self.deathSound.play()
        super().die()

    def damaged(self):
        if self.pulsesLeft <= 0:
            self.pulsesLeft = self.damagePulses
            if self.hp>1:
                self.hurtSound.play()
                self.hp-=1
            else:
                self.die()

    def on_collide_up(self,other=None):
        super().on_collide_up(other)
        if other!=None and isinstance(other,mice.mice):
            self.damaged()

    def on_collide_down(self, other = None):
        super().on_collide_down(other)
        if other!=None:
            if isinstance(other,mice.mice):
                self.nofshots+=1
            elif isinstance(other,cheese.cheese):
                self.hp+=1
                values.entity_manager.load_next_level()

    def on_collide_left(self,other=None):
        super().on_collide_left(other)
        if other!=None:
            if isinstance(other,mice.mice):
                self.damaged()
            elif isinstance(other,cheese.cheese):
                self.hp+=1
                values.entity_manager.load_next_level()

    def on_collide_right(self,other=None):
        super().on_collide_right(other)
        if other!=None:
            if isinstance(other,mice.mice):
                self.damaged()
            elif isinstance(other,cheese.cheese):
                self.hp+=1
                values.entity_manager.load_next_level()
            
    def update( self ):
        key = pygame.key.get_pressed()  #checking pressed keys
        
        self.move(self.velocity)
        self.velocity.x = 0

        speed = self.speed * values.delta_time
        if key[pygame.K_a] and not self.collide_left:
            self.velocity.addX(-speed)
            self.heading = -1
        elif key[pygame.K_d] and not self.collide_right:
            self.velocity.addX(speed)
            self.heading = 1
            
        if self.collide_down:
            if key[pygame.K_w]:
                self.velocity.addY(-self.jump_power)
                self.jumpSound.play()
        else:
            self.velocity.addY(.05 * values.delta_time);

        if key[pygame.K_f]:
            self.t2=time.time()
            if self.nofshots>0 and self.t2-self.t1>0.2:
                t1=time.time()

            if self.nofshots>0 and self.shootDelay <= values.global_time:
                self.shootSound.play()
                myshoot = shoot.shoot(self.body.left + (self.body.width/2) + self.heading*(self.body.width/2),self.center().y,self.heading,self.group)
                values.entity_manager.add(myshoot)
                self.nofshots-=1
                values.level.sprite_layers[1].add_sprite(myshoot.sprite)
                self.shootDelay = values.global_time + self.shootDelayTime
        self.sprite.image = pygame.transform.flip(self.image.get_image(0), self.heading == -1, False)
        

        if(self.damageDelay < values.global_time and self.pulsesLeft > 0):
            self.damageDelay = values.global_time + self.damageDelayTime
            self.pulsesLeft -= 1
            if(self.pulsesLeft % 2 == 0):
                values.level.sprite_layers[1].add_sprite(self.sprite)
            else:
                values.level.sprite_layers[1].remove_sprite( self.sprite )