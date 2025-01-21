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
    'flower-wilt': load_image('flower-wilt1.png'),
    'fangflower': load_image('fangflower1.png'),
    'empty': load_image('grass02.png'),
    'life': load_image('life-count1.png'),
    'timeee': load_image('white-fon.jpg')
}

tile_width = tile_height = 50
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
flowers = []
start_time = time.time()


def time_elapsed(start_time):
    elapsed_time = int(time.time() - start_time)
    font = pygame.font.SysFont('Arial Black', 25)
    text_surface = font.render("Garden happy for: " + str(elapsed_time) + " seconds", True, (0, 80, 0))
    screen.blit(text_surface, (10, 5))
    return elapsed_time


def score():
    elapsed_time = 0
    font = pygame.font.SysFont('Arial Black', 25)
    text_surface = font.render("Score: " + str(elapsed_time), True, (199, 21, 133))
    screen.blit(text_surface, (450, 5))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('cow.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)
        self.cow = 'cow.png'
        self.water = 'cow-water.png'
        self.cur_img = self.cow

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)

    def change_image(self):
        if self.cur_img == self.cow:
            self.cur_img = self.water
        else:
            self.cur_img = self.cow
        self.image = load_image(self.cur_img)

    def can_water_flower(self):
        x, y = self.pos
        neighbors = [
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y)
        ]
        for nx, ny in neighbors:
            if 0 <= nx < level_x and 0 <= ny < level_y:
                for flower in flowers:
                    flower_x, flower_y = flower.rect.topleft
                    if (flower_x // tile_width, flower_y // tile_height) == (nx, ny) and flower.wilted:
                        return flower
        return None


class Flower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('flower1.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.wilted = False
        self.wilted_start_time = None
        self.last_watered_time = None
        self.watered_duration = 5  # живой

    def wilt(self):
        self.wilted = True
        self.image = tile_images['flower-wilt']
        self.wilted_start_time = time.time()

    def water(self):
        if self.wilted:
            self.wilted = False
            self.image = tile_images['flower']
            self.wilted_start_time = None
        self.last_watered_time = time.time()

    def update(self):
        if self.last_watered_time is not None:
            if time.time() - self.last_watered_time > self.watered_duration:
                self.wilt()


class FangFlower(Flower):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = load_image('fangflower1.png')


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
                flower = Flower(x, y)
                flowers.append(flower)
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
        if y < level_y - 1 and level[y + 1][x] in ['.', '@']:
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
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def display_message(message):
    font = pygame.font.Font(None, 20)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()


level = load_level('map1.txt')
player, level_x, level_y = generate_level(level)
start_screen()
start_time = time.time()
time_elapsed(start_time)

running = True
while running:
    elapsed_time = time_elapsed(start_time)
    for flower in flowers:
        flower.update()
        if flower.wilted:
            if time_elapsed(flower.wilted_start_time) > wilted_time:
                display_message("Игра окончена: цветок увял слишком долго!")
                terminate()
        else:
            if elapsed_time % 8 == 0 and elapsed_time > 0:
                flower.wilt()

    if elapsed_time > happy_garden_time and not any(isinstance(flower, FangFlower) for flower in flowers):
        fang_flower = FangFlower(flowers[0].pos[0], flowers[0].pos[1])
        flowers[0].kill()
        flowers.append(fang_flower)
        print("Цветок мутировал в клыкоцвет!")

    for flower in flowers:
        if isinstance(flower, FangFlower) and player.rect.colliderect(flower.rect):
            display_message("Игра окончена: корова была задушена клыкоцветом!")
            terminate()
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
            if event.key == pygame.K_SPACE:
                player.change_image()
                flower_to_water = player.can_water_flower()
                if flower_to_water:
                    flower_to_water.water()
                    break

    screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    time_elapsed(start_time)
    score()
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
