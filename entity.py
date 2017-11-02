import pygame
import vector
import tiledtmxloader
import math
import values

class entity:
    def __init__( self, posX, posY ):
        self.body = pygame.Rect( posX, posY, 32, 32 )
        self.position = vector.Vector2( posX, posY )
        self.is_player = False
        
        self.group = 0;
        self.ghost = False;

        self.speed = 1
        self.velocity = vector.Vector2(0, 0)
        self.heading = 1

        self.collide_left = False
        self.collide_right = False
        self.collide_up = False
        self.collide_down = False

        self.remove_self = False
    
        self.try_move_left = 0
        self.try_move_right = 0
        self.try_move_up = 0
        self.try_move_down = 0

        image = pygame.Surface( ( self.body.width, self.body.height ), pygame.SRCALPHA )
        image.fill((0, 255, 0, 200))
        rect = image.get_rect()
        rect.topleft = (posX, posY)
        self.sprite = tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

    def update( self ):
        pass

    def draw(self, screen, level = None):
        pass

    def move(self, velocity):
        self.position = self.position.plus(velocity)
        
        self.body.left = self.position.x
        self.body.top = self.position.y
        self.sprite.rect = self.body

    def die( self ):
        self.remove_self = True

    def on_collide(self, other = None):
        pass

    def on_collide_left(self, other = None):
        self.velocity.x = 0
        
    def on_collide_right(self, other = None):
        self.velocity.x = 0

    def on_collide_up(self, other = None):
        self.velocity.y = 0
    
    def on_collide_down(self, other = None):
        self.velocity.y = 0

    def collide_with( self, static_entity ):
        # self is entity 1, the other entity is 2
        collider = static_entity
        flag = False
        if isinstance(static_entity, entity):
            collider = static_entity.body
            flag = True
        else:
            static_entity = None

        if ((self.body.bottom + 1 + self.velocity.y > collider.top) and \
		    (self.body.top + self.velocity.y < collider.bottom) and \
            (self.body.right + self.velocity.x > collider.left) and \
            (self.body.left + self.velocity.x < collider.right) and \
            self.body.bottom <= collider.top):

            if (self.velocity.y >= 0):
                self.on_collide_down(static_entity)
                self.position.y = collider.top - self.body.height
                self.collide_down = True
                if flag:
                    static_entity.on_collide_up(self)
                    static_entity.collide_up = True

        if ((self.body.bottom + self.velocity.y > collider.top) and	\
            (self.body.top - 1 + self.velocity.y < collider.bottom) and \
            (self.body.right + self.velocity.x > collider.left) and \
            (self.body.left + self.velocity.x < collider.right) and \
            (self.body.top >= collider.bottom) ):

            if (self.velocity.y <= 0) :
                self.on_collide_up(static_entity)
                self.position.y = collider.bottom
                self.collide_up = True
                if flag:
                    static_entity.on_collide_down(self)
                    static_entity.collide_down = True


        if ((self.body.bottom + self.velocity.y > collider.top) and	\
        	(self.body.top + self.velocity.y < collider.bottom) and \
            (self.body.right + 1 + self.velocity.x > collider.left) and \
            (self.body.left + self.velocity.x < collider.right) and \
            self.body.right <= collider.left):   
            
            if (self.velocity.x >= 0): 
                self.on_collide_right(static_entity)
                self.position.x = collider.left - self.body.width
                self.collide_right = True
                if flag:
                    static_entity.on_collide_left(self)
                    static_entity.collide_left = True


        if ((self.body.bottom + self.velocity.y > collider.top) and \
		    (self.body.top + self.velocity.y < collider.bottom) and \
		    (self.body.right + self.velocity.x > collider.left) and \
		    (self.body.left - 1 + self.velocity.x < collider.right) and \
		    self.body.left >= collider.right):
            
            if (self.velocity.x <= 0):
                self.on_collide_left(static_entity)
                self.position.x = collider.right
                self.collide_left = True
                if flag:
                    static_entity.on_collide_right(self)
                    static_entity.collide_right = True
                
    def hit_with( self, entity ):
        pass

    def overlap( self, static_entity ):
        if ((self.body.bottom > static_entity.body.top) and \
		    (self.body.top < static_entity.body.bottom) and \
            (self.body.right > static_entity.body.left) and \
            (self.body.left < static_entity.body.right) ):
                self.hit_with( static_entity )
                static_entity.hit_with( self )

    def clear_collisions( self ):        
        self.collide_left = False
        self.collide_right = False
        self.collide_up = False
        self.collide_down = False

    def center( self ):
        return vector.Vector2( self.position.x + self.body.width / 2, self.position.y + self.body.height / 2 )