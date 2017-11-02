import pygame
import vector

class mouse():
    def __init__(self):
        self.position = vector.Vector2(0, 0)
        self.mouse_state = 0
        
    def on_mouse_down(self):
        self.mouse_state = 1
    
    def on_mouse_up(self):
        self.mouse_state = 0

    def update(self):
        self.position.set_values(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        if self.mouse_state == 1:
            self.mouse_state = 2

    def held(self):
        return self.mouse_state > 0

    def hit(self):
        return self.mouse_state == 1