import pygame
import time

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50

CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
game_over = False
finalized = False
garden_happy = True
fangflower_collision = False
time_elapsed = 0
start_time = time.time()
flower_list = []
wilted_list = []
fangflower_list = []
fangflower_vy_list = []
fangflower_vx_list = []


def draw():
    global game_over, time_elapsed, finalized
    if not game_over:
        # screen.clear() это что XD
        screen.blit(pygame.image.load("garden.png"), (0, 0))
        screen.blit(pygame.image.load("cow.jpg"), (100, 500))

        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()

        time_elapsed = int(time.time() - start_time)
        '''font = pygame.font.Font(None, 36)
        text = font.render("Garden happy for: " + str(time_elapsed) + " seconds", True, (0, 0, 0))
        screen.blit(text, (10, 10))'''
        screen.draw.text("Garden happy for: " + str(time_elapsed) + " seconds",
                         topleft=(10, 10), color="black")

    else:
        if not finalized:
            screen.blit(pygame.image.load("cow.jpg"), (100, 500))
            screen.draw.text(
                "Garden happy for: " + str(time_elapsed) + " seconds",
                topleft=(10, 10), color="black")

            '''if not garden_happy:
                screen.draw.text("GARDEN UNHAPPY - GAME OVER!")
            else:
                screen.draw.text("FANGFLOWER ATTACK - GAME OVER!")
            finalized = True'''

    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw()
    clock.tick(FPS)
pygame.quit()
