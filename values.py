import random
import mouse
import pygame

entity_manager = None
level = None
screen = None
node_map = None
rand = random.Random()
mouse = mouse.mouse()
global_time = 0
delta_time = 0

clock = pygame.time.Clock()

def change_time():
    global delta_time
    global global_time
    global clock
    delta_time = clock.get_time()
    global_time += delta_time