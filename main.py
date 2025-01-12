import pygame
import random
import time

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
game_over = False
finalised = False
garden_happy = True
fangflower_collision = False
time_elapsed = 0
start_time = time.time()
flower_list = []
wilted_list = []
fangflower_list = []
fangflower_vy_list = []
fangflower_vx_list = []
