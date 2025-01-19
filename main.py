import pygame
import sys
import os
import time

pygame.init()
size = WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50
start_time = time.time()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
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


def time_elapsed():
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
    # вернем игрока, а также размер поля в клетках
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


def start_screen():
    intro_text = ["HAPPY GARDEN", "",
                  "Правила игры:",
                  "-",
                  "-"]

    fon = pygame.transform.scale(load_image('f1.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Georgia', 33)
    text_coord = 50

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 250, 220))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
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
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player(player, 'up')
            if event.key == pygame.K_DOWN:
                move_player(player, 'down')
            if event.key == pygame.K_LEFT:
                move_player(player, 'left')
            if event.key == pygame.K_RIGHT:
                move_player(player, 'right')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.change_image()

    screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    time_elapsed()
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
