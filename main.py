import pygame
import sys
import os
import time

pygame.init()
size = WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
wilted_time = 10
happy_garden_time = 15
FPS = 50



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'flower': load_image('flower1.png'),
    'flower-wint': load_image('flower-wilt1.png'),
    'fangflower': load_image('fangflower1.png'),
    'empty': load_image('grass02.png'),
    'life': load_image('life-count1.png'),
    'timeee': load_image('white-fon.jpg')

}

tile_width = tile_height = 50
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def time_elapsed(start_time):
    time_elapsed = int(time.time() - start_time)
    font = pygame.font.SysFont('Arial Black', 25)
    text_surface = font.render("Garden happy for: " + str(time_elapsed) + " seconds", True, (0, 80, 0))
    screen.blit(text_surface, (10, 5))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('cow.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)
        self.cow = 'cow.png'
        self.water = 'cow-water.png'
        self.cur_img = self.cow

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)

    def change_image(self):
        if self.cur_img == self.cow:
            self.cur_img = self.water
        else:
            self.cur_img = self.cow
        self.image = load_image(self.cur_img)


class Flower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('flower1.png')
        pass


class FangFlower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('fangflower1.png')
        pass


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '%':
                Tile('timeee', x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '$':
                Tile('life', x, y)
            elif level[y][x] == '#':
                Tile('flower', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def move_player(player, direction):
    x, y = player.pos
    if direction == 'up':
        if y > 0 and level[y - 1][x] in ['.', '@']:
            player.move(x, y - 1)
    elif direction == 'down':
        if y < level_y and level[y + 1][x] in ['.', '@']:
            player.move(x, y + 1)
    elif direction == 'left':
        if x > 0 and level[y][x - 1] in ['.', '@']:
            player.move(x - 1, y)
    elif direction == 'right':
        if x < level_x - 1 and level[y][x + 1] in ['.', '@']:
            player.move(x + 1, y)


def terminate():
    pygame.quit()
    sys.exit()


def mutate():
    pass


def start_screen():
    intro_text = ["HAPPY GARDEN",
                  "Правила игры:",
                  "1. Игра начинается с появления коровы и цветка в саду.",
                  "2. Каждые 10 секунд в саду имеющийся ",
                  "    цветок начинает увядать.",
                  "3. Чтобы перемещать корову к увядшему цветку, ",
                  "     используйте клавиши со стрелками.",
                  "4. Чтобы полить цветок, игрок должен нажать ",
                  "     клавишу пробел.",
                  "5. Если какой-либо цветок остается увядшим более",
                  "     10 секунд, игра заканчивается.",
                  "6. Если сад счастлив более 15 секунд, один из цветов ",
                  "     мутирует в клыкоцвет и пытается задушить корову.",
                  "7. Игра заканчивается, если:",
                  "    - Любой цветок остается увядшим более 10 секунд.",
                  "    - Корову 5 раз атакует клыкоцветок.",
                  "8. Цель игры: полить как можно больше цветов."]

    fon = pygame.transform.scale(load_image('f1.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Georgia', 15, 2)
    text_coord = 50

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 250, 230))
        intro_rect = string_rendered.get_rect()
        text_coord += 6
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


level = load_level('map3.txt')
player, level_x, level_y = generate_level(level)
start_screen()
start_time = time.time()
time_elapsed(start_time)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            time_elapsed()
            if event.key == pygame.K_UP:
                move_player(player, 'up')
            if event.key == pygame.K_DOWN:
                move_player(player, 'down')
            if event.key == pygame.K_LEFT:
                move_player(player, 'left')
            if event.key == pygame.K_RIGHT:
                move_player(player, 'right')
            if event.key == pygame.K_SPACE:
                player.change_image()

    screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    time_elapsed(start_time)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
