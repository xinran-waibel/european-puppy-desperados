import mice
import shoot
import values
import entity_manager
import animation
import pygame
import tiledtmxloader
import vector

class shootmice(mice.mice):
    def __init__(self,posX,posY):
        super().__init__(posX,posY)

        self.shotsPerTime = 3
        self.shotsTaken = 0
        self.shootDelayTime = 700
        self.shootDelay = 0

        self.body.width = 39
        self.body.height = 55

        self.image = animation.animated_image("graphics/mice_gun.png", 39, 55);
        self.shootSound = pygame.mixer.Sound( "sounds/miceshoots.wav" )
        self.shootSound.set_volume(.15)

        rect = self.image.get_image(0).get_rect()
        rect.topleft = (posX, posY)
        self.sprite = tiledtmxloader.helperspygame.SpriteLayer.Sprite(self.image.get_image(0), rect)
        self.heading = -1
        self.velocity.x = 0
        
    def on_collide_left(self, other = None):
        pass

    def on_collide_right(self, other = None):
        pass
    
    def update(self):
        #super().update()
        self.move(self.velocity)
        if not self.collide_down:
            self.velocity.addY(.05 * values.delta_time);

        self.sprite.image = pygame.transform.flip(self.image.get_image(0), self.heading == -1, False)
        
        dy=values.entity_manager.player.position.y-self.position.y
        if abs(dy)<=120 and self.shootDelay <= values.global_time:
            self.shootSound.play()
            miceshoot = shoot.shoot(self.body.left + (self.body.width/2) + self.heading*(self.body.width/2) ,self.center().y,self.heading,2)
            values.entity_manager.add(miceshoot)
            values.level.sprite_layers[1].add_sprite(miceshoot.sprite)
            self.shootDelay = values.global_time + self.shootDelayTime
            self.shotsTaken += 1
            if(self.shotsTaken == self.shotsPerTime):
                self.shotsTaken = 0
                self.shootDelay = values.global_time + 4*self.shootDelayTime
