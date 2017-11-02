import values
import entity
import tiledtmxloader
import animation
import pygame

class mice(entity.entity):
    def __init__(self,posX,posY):
        super().__init__(posX,posY)
        self.velocity.x=self.speed
        self.heading=1
        self.group=2
        self.body.width = 38
        self.body.height = 53
        
        self.deathSound = pygame.mixer.Sound( "sounds/mousedead.wav" )

        self.image = animation.animated_image("graphics/mice_enemy.png", 38, 53);
        rect = self.image.get_image(0).get_rect()
        rect.topleft = (posX, posY)
        self.sprite = tiledtmxloader.helperspygame.SpriteLayer.Sprite(self.image.get_image(0), rect)
    
    def on_collide_left(self, other = None):
        self.heading=1
        self.velocity.x=self.speed*self.heading

    def on_collide_right(self, other = None):
        self.heading=-1
        self.velocity.x=self.speed*self.heading
        
    def on_collide_up(self, other = None):
        self.die()
        
    def update(self):
        self.move(self.velocity)
        if not self.collide_down:
            self.velocity.addY(.05 * values.delta_time);
        self.sprite.image = pygame.transform.flip(self.image.get_image(0), self.heading == -1, False)
        
        newPos = self.position.plus(self.velocity)
        newPos.x = newPos.x / values.level.tile_width
        newPos.y = newPos.y / values.level.tile_height
        newPos.y += 2
        
        coll_level = values.level.sprite_layers[3]
        if coll_level.content2D[int(newPos.y)][int(newPos.x)] is None:
            self.heading = -self.heading
            self.velocity.x = -self.velocity.x

            
    def die(self):
        self.deathSound.play()
        super().die()
