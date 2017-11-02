import values
import entity
import tiledtmxloader
import level
import pygame
import mice

class cheese(entity.entity):
    def __init__(self,posX,posY):
        super().__init__(posX,posY)
        self.group=2

        self.ghost = True

        image = pygame.Surface( ( self.body.width, self.body.height ), pygame.SRCALPHA )
        image.fill((200, 200, 0, 200))
        rect = image.get_rect()
        rect.topleft = (posX, posY)
        self.sprite = tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

    
    def on_collide_left(self, other = None):
        pass

    def on_collide_right(self, other = None):
        pass
        
    def on_collide_up(self, other = None):
        pass
        
    def update(self):
        if(values.level.getNumberOfMice() == 0 and self.ghost):
            count = 0
            for entity in values.entity_manager.entities:
                if isinstance(entity, mice.mice):
                    count += 1
            if(count == 0):
                values.level.sprite_layers[1].add_sprite(self.sprite)
                self.ghost = False;
        pass
