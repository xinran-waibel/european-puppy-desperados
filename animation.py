import pygame
import math

class animated_image():
    def __init__( self, file_name, width, height ):
        self.image = pygame.image.load( file_name )
        self.width = width
        self.height = height
        self.max_x = math.ceil(self.image.get_width() / self.width)
        self.max_y = math.ceil(self.image.get_height() / self.height)
    def get_image( self, number ):
        x = number % self.max_x
        y = int( number / self.max_x )
        if y >= self.max_y:
            y = x = 0
        
        self.image.set_clip(pygame.Rect(x*self.width, y*self.height, self.width, self.height)) #find the sprite you want
        return self.image.subsurface(self.image.get_clip()) #grab the sprite you want

class animation():
    def __init__( self ,animated_image, sections, looping = False, delay = 1 ):
        self.animated_image = animated_image
        self.sections = sections
        self.looping = looping
        self.delay = delay

    def get_image( self, index ):
        return self.animated_image.get_image( self.sections[index] )

    
class animation_runner():
    def __init__( self , anim = None ):
        self.anim = anim
        self.on_image = 0
        self.current_delay = self.anim.delay
        self.completed = False

    def update( self ):
        if self.current_delay <= 0:
            self.completed = False
            self.current_delay = self.anim.delay
            if self.on_image + 1 < len(self.anim.sections):
                self.on_image += 1
            elif self.anim.looping:
                self.on_image = 0
            else: self.completed = True
        else:
            self.current_delay -= 1

    def set_animation( self, anim ):
        self.anim = anim
        self.on_image = 0
        self.current_delay = self.anim.delay
        self.completed = False

    def has_completed( self ):
        return self.completed
    
    def reset( self ):
        self.current_delay = self.anim.delay
        self.on_image = 0

    def get_image(self):
        return self.anim.get_image( self.on_image )