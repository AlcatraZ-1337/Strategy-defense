import os
import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 120
WIDTH = 1600
HEIGHT = 900
STEP = 20
ENEMY_STEP_ON_X = []
ENEMY_STEP_ON_Y = []

dead = False
game_over_variable = False

pygame.display.set_caption("Strategy Defense")
pygame.display.set_icon(pygame.image.load("icon.png"))

music = pygame.mixer.Sound('music3.mp3')
dead_sound = pygame.mixer.Sound('Dead_sound.mp3')
game_over = pygame.mixer.Sound('Game_over.mp3')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
desert_tiles_group = pygame.sprite.Group()
tiles_with_trees_group = pygame.sprite.Group()
water_tiles_group = pygame.sprite.Group()
road_tiles_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
danger_enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y, walking_enemy_on_x, walking_enemy_on_y = None, None, None, [], []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)

            elif level[y][x] == '[':
                WaterTile('top_water', x, y)
            elif level[y][x] == '=':
                WaterTile('middle_water', x, y)
            elif level[y][x] == ']':
                WaterTile('bottom_water', x, y)

            elif level[y][x] == '<':
                RoadTile('top_desert_road', x, y)
            elif level[y][x] == '+':
                RoadTile('middle_road', x, y)
            elif level[y][x] == '>':
                RoadTile('bottom_desert_road', x, y)
            elif level[y][x] == '{':
                RoadTile('top_grass_road', x, y)
            elif level[y][x] == '-':
                RoadTile('middle_road', x, y)
            elif level[y][x] == '}':
                RoadTile('bottom_grass_road', x, y)

            elif level[y][x] == '`':
                DesertTile('sand', x, y)
            elif level[y][x] == '"':
                DesertTile('stones', x, y)

            elif level[y][x] == '#':
                TileWithTrees('tree_1', x, y)
            elif level[y][x] == '*':
                TileWithTrees('tree_2', x, y)

            elif level[y][x] == '!':
                Enemy('archer', x, y)
            elif level[y][x] == 'm':
                Enemy('horse_rider', x, y)
            elif level[y][x] == '0':
                Enemy('rifleman', x, y)
            elif level[y][x] == 'w':
                Enemy('bycicle_rider', x, y)

            elif level[y][x] == '&':
                walking_enemy_on_x.append(WalkingEnemyOnX('archer', x, y))
                ENEMY_STEP_ON_X.append(5)
            elif level[y][x] == '8':
                walking_enemy_on_x.append(WalkingEnemyOnX('rifleman', x, y))
                ENEMY_STEP_ON_X.append(5)
            elif level[y][x] == '%':
                walking_enemy_on_y.append(WalkingEnemyOnY('archer', x, y))
                ENEMY_STEP_ON_Y.append(5)
            elif level[y][x] == '|':
                walking_enemy_on_y.append(WalkingEnemyOnY('rifleman', x, y))
                ENEMY_STEP_ON_Y.append(5)

            elif level[y][x] == '@':
                new_player = Player(x, y)

    return new_player, x, y, walking_enemy_on_x, walking_enemy_on_y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global music
    intro_text = [" ",
                  "Strategy defense"]

    fon = pygame.transform.scale(load_image('main_picture.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, 'black', ((0, 400), (670, 100)))
    font = pygame.font.SysFont('Haettenschweiler', 120)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 80
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    music.play().set_volume(0.25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                music.stop()
                music = pygame.mixer.Sound('music1.mp3')
                return
        pygame.display.flip()
        clock.tick(FPS)


def screen_fill():
    global game_over_variable
    screen.fill(pygame.Color(0, 0, 0))

    tiles_group.draw(screen)
    desert_tiles_group.draw(screen)
    tiles_with_trees_group.draw(screen)
    water_tiles_group.draw(screen)
    road_tiles_group.draw(screen)
    danger_enemy_group.draw(screen)
    enemy_group.draw(screen)
    player_group.draw(screen)

    screen.blit(Tree_ground, (0, 0))
    screen.blit(Tree_ground3, (0, 0))
    screen.blit(Tree_ground2, (1501, 0))
    screen.blit(Tree_ground4, (0, 800))

    if dead:
        text_after_dead = pygame.font.SysFont('Calibri', 80).render('Нажмите пробел, чтобы закончить', 1,
                                                                    pygame.Color('white'))
        screen.fill(pygame.Color(0, 0, 0))
        if not game_over_variable:
            screen.fill(pygame.Color(0, 0, 0))
            game_over_variable = True
        else:
            screen.blit(Game_over_picture, (160, 100))
            game_over_variable = False
        screen.blit(text_after_dead, (215, 700))
        clock.tick(5)

    pygame.display.flip()

    clock.tick(FPS)


tile_images = {'grass': load_image('grass.png'), 'tree_1': load_image('Tree1.png'), 'tree_2': load_image('Tree2.png'),
               'sand': load_image('sand.png'), 'stones': load_image('Sand_and_stones.png'),
               'top_water': load_image('Water1.png'), 'middle_water': load_image('Water3.png'),
               'bottom_water': load_image('Water2.png'), 'top_desert_road': load_image('Desert_Road1.png'),
               'middle_road': load_image('Road.png'), 'bottom_desert_road': load_image('Desert_Road2.png'),
               'top_grass_road': load_image('Grass_Road1.png'), 'bottom_grass_road': load_image('Grass_Road2.png')}
player_image = load_image('Hero.png')
enemy_image = {'archer': load_image('Archer.png'), 'horse_rider': load_image('Horse.png'),
               'rifleman': load_image('Rifleman.png'), 'bycicle_rider': load_image('Motobyke.png')}
Tree_ground = load_image('Treeground.png')
Tree_ground2 = load_image('Treeground2.png')
Tree_ground3 = load_image('Treeground3.png')
Tree_ground4 = load_image('Treeground4.png')
Game_over_picture = load_image('game_over_picture.jpg')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class DesertTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(desert_tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_with_trees_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class RoadTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(road_tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class TileWithTrees(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_with_trees_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class WalkingEnemyOnX(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos_x, pos_y):
        if enemy_type == 'archer' or enemy_type == 'horse_rider':
            super().__init__(enemy_group, all_sprites)
            self.image = enemy_image[enemy_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        elif enemy_type == 'rifleman' or enemy_type == 'bycicle_rider':
            super().__init__(danger_enemy_group, all_sprites)
            self.image = enemy_image[enemy_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def walk_x(self):
        if pygame.sprite.groupcollide(enemy_group, water_tiles_group, False, False) or \
                pygame.sprite.spritecollide(walking_enemy_on_x[i], tiles_with_trees_group, False):
            ENEMY_STEP_ON_X[i] = -ENEMY_STEP_ON_X[i]
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect.x -= ENEMY_STEP_ON_X[i]


class WalkingEnemyOnY(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos_x, pos_y):
        if enemy_type == 'archer' or enemy_type == 'horse_rider':
            super().__init__(enemy_group, all_sprites)
            self.image = enemy_image[enemy_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        elif enemy_type == 'rifleman' or enemy_type == 'bycicle_rider':
            super().__init__(danger_enemy_group, all_sprites)
            self.image = enemy_image[enemy_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def walk_y(self):
        if pygame.sprite.groupcollide(enemy_group, water_tiles_group, False, False) or \
                pygame.sprite.spritecollide(walking_enemy_on_y[i], tiles_with_trees_group, False):
            ENEMY_STEP_ON_Y[i] = -ENEMY_STEP_ON_Y[i]
        self.rect.y -= ENEMY_STEP_ON_Y[i]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos_x, pos_y):
        if enemy_type == 'archer' or enemy_type == 'horse_rider':
            super().__init__(enemy_group, all_sprites)
            self.image = enemy_image[enemy_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        elif enemy_type == 'rifleman' or enemy_type == 'bycicle_rider':
            super().__init__(danger_enemy_group, all_sprites)
            self.image = enemy_image[enemy_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self):
        if moving == 'L':
            self.image = pygame.transform.flip(player_image, 1, 0)
        elif moving == 'R':
            self.image = pygame.transform.flip(player_image, 0, 0)


class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()

player, level_x, level_y, walking_enemy_on_x, walking_enemy_on_y = generate_level(load_level('levelex.txt'))
generate_level(load_level('enemies.txt'))
camera = Camera((level_x, level_y))

music.play().set_volume(0.25)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and dead:
            if event.key == pygame.K_SPACE:
                running = False
        elif event.type == pygame.KEYDOWN and not dead:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.rect.x -= STEP
                moving = 'L'
                player.update()
                if pygame.sprite.groupcollide(player_group, water_tiles_group, False, False) or \
                        pygame.sprite.groupcollide(player_group, tiles_with_trees_group, False, False):
                    player.rect.x += STEP
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.rect.x += STEP
                moving = 'R'
                player.update()
                if pygame.sprite.groupcollide(player_group, water_tiles_group, False, False) or \
                        pygame.sprite.groupcollide(player_group, tiles_with_trees_group, False, False):
                    player.rect.x -= STEP
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.rect.y -= STEP
                if pygame.sprite.groupcollide(player_group, water_tiles_group, False, False) or \
                        pygame.sprite.groupcollide(player_group, tiles_with_trees_group, False, False):
                    player.rect.y += STEP
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.rect.y += STEP
                if pygame.sprite.groupcollide(player_group, water_tiles_group, False, False) or \
                        pygame.sprite.groupcollide(player_group, tiles_with_trees_group, False, False):
                    player.rect.y -= STEP

    for i in range(len(walking_enemy_on_x)):
        walking_enemy_on_x[i].walk_x()

    for i in range(len(walking_enemy_on_y)):
        walking_enemy_on_y[i].walk_y()

    camera.update(player)

    if pygame.sprite.groupcollide(player_group, enemy_group, False, True):
        dead_sound.play().set_volume(0.25)
    elif pygame.sprite.groupcollide(player_group, danger_enemy_group, True, False):
        music.stop()
        game_over.play().set_volume(0.25)
        dead = True

    for sprite in all_sprites:
        camera.apply(sprite)

    screen_fill()

terminate()
