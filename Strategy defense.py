import os
import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 120
WIDTH = 1600
HEIGHT = 900
STEP = 21
ENEMY_STEP_ON_X = []
ENEMY_STEP_ON_Y = []

dead = False
win = False
shoot = False
enemy_shoot = False
game_over_variable = False
congratulation_variable = False
escape_pressed = -1
tab_pressed = -1
dialogue_1_string_number = 1
dialogue_2_string_number = 1
quest_available = False
commanders_count = 3

dialogue_1_enabled = False
dialogue_2_enabled = False

arrow_moving = 'R'
captain_rotation = None

pygame.display.set_caption("Strategy Defense")
pygame.display.set_icon(pygame.image.load("image/icon.png"))

music = pygame.mixer.Sound('music/music3.mp3')
dead_sound = pygame.mixer.Sound('music/Dead_sound.mp3')
game_over = pygame.mixer.Sound('music/Game_over.mp3')
game_win = pygame.mixer.Sound('music/win.mp3')
arrow_throw = pygame.mixer.Sound('music/Arrow_throw.mp3')
arrow_collide_sprite = pygame.mixer.Sound('music/Arrow_collide_sprite.mp3')

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
captain_enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
teammates_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('image', name)
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
    filename = "level generation/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y, walking_enemy_on_x, walking_enemy_on_y, captains, mage = None, None, None, [], [], [], None
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
            elif level[y][x] == 'x':
                captains.append(Enemy('captain', x, y))

            elif level[y][x] == '&':
                walking_enemy_on_x.append(WalkingEnemyOnX('archer', x, y))
                ENEMY_STEP_ON_X.append(5)
            elif level[y][x] == 'M':
                walking_enemy_on_x.append(WalkingEnemyOnX('horse_rider', x, y))
                ENEMY_STEP_ON_X.append(10)
            elif level[y][x] == '8':
                walking_enemy_on_x.append(WalkingEnemyOnX('rifleman', x, y))
                ENEMY_STEP_ON_X.append(5)
            elif level[y][x] == 'W':
                walking_enemy_on_x.append(WalkingEnemyOnX('bycicle_rider', x, y))
                ENEMY_STEP_ON_X.append(15)
            elif level[y][x] == '%':
                walking_enemy_on_y.append(WalkingEnemyOnY('archer', x, y))
                ENEMY_STEP_ON_Y.append(5)
            elif level[y][x] == '|':
                walking_enemy_on_y.append(WalkingEnemyOnY('rifleman', x, y))
                ENEMY_STEP_ON_Y.append(5)

            elif level[y][x] == '@':
                new_player = Player(x, y)

            elif level[y][x] == 'H':
                mage = Teammates(x, y)

    return new_player, x, y, walking_enemy_on_x, walking_enemy_on_y, captains, mage


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
                music = pygame.mixer.Sound('music/music1.mp3')
                return
        pygame.display.flip()
        clock.tick(FPS)


def screen_fill():
    global game_over_variable
    global congratulation_variable
    global quest_available
    screen.fill(pygame.Color(0, 0, 0))

    tiles_group.draw(screen)
    desert_tiles_group.draw(screen)
    water_tiles_group.draw(screen)
    road_tiles_group.draw(screen)
    tiles_with_trees_group.draw(screen)
    danger_enemy_group.draw(screen)
    captain_enemy_group.draw(screen)
    enemy_group.draw(screen)
    player_group.draw(screen)
    teammates_group.draw(screen)
    bullet_group.draw(screen)

    screen.blit(Tree_ground, (0, 0))
    screen.blit(Tree_ground3, (0, 0))
    screen.blit(Tree_ground2, (1501, 0))
    screen.blit(Tree_ground4, (0, 800))

    if escape_pressed > 0:
        intro_text = ["Инструкция:",
                      "Ходить: W, A, S, D и стрелки",
                      "Стрелять из лука: Пробел",
                      "Открыть список заданий: TAB",
                      "Перезапустить музыку: Z"]

        font = pygame.font.SysFont('Haettenschweiler', 30)
        pygame.draw.rect(screen, 'black', ((590, 220), (395, 520)))
        pygame.draw.rect(screen, 'grey', ((600, 230), (375, 500)))

        text_coord = 245
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            instruction_rect = string_rendered.get_rect()
            text_coord += 10
            instruction_rect.top = text_coord
            instruction_rect.x = 620
            text_coord += instruction_rect.height
            screen.blit(string_rendered, instruction_rect)

    if tab_pressed > 0:
        intro_text = ["Текущие задания:",
                      "Убить трёх командиров"]

        font = pygame.font.SysFont('Haettenschweiler', 30)
        pygame.draw.rect(screen, 'black', ((590, 220), (395, 520)))
        pygame.draw.rect(screen, 'grey', ((600, 230), (375, 500)))

        text_coord = 245
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            instruction_rect = string_rendered.get_rect()
            text_coord += 10
            instruction_rect.top = text_coord
            instruction_rect.x = 620
            text_coord += instruction_rect.height
            if quest_available or line == "Текущие задания:":
                screen.blit(string_rendered, instruction_rect)
            if not quest_available and line != "Текущие задания:":
                string_rendered = font.render("Пусто", 1, pygame.Color('black'))
                screen.blit(string_rendered, instruction_rect)

    if dialogue_1_enabled:
        intro_text = ("- Привет.", "- Приятно увидеть в этом лесу заблудшего путника.",
                      "- Но я полагаю, ты пришёл сюда не ради прогулки по лесу?",
                      "- Если да, то я думаю мы сможем помочь друг другу.",
                      "- Видишь ли... В лес пришли войска короля Стардокса.",
                      "- Я предлагаю тебе разобраться с тремя командирами.",
                      "- Когда закончишь с ними, возвращайся ко мне.",
                      "- Удачи тебе путник!")

        font = pygame.font.SysFont('Haettenschweiler', 35)
        try:
            string_rendered = font.render(intro_text[dialogue_1_string_number], 1, pygame.Color('black'))
            text_after_dead = pygame.font.SysFont('Calibri', 30).render('Нажмите пробел, чтобы продолжить диалог', 1,
                                                                        pygame.Color('black'))
            pygame.draw.rect(screen, 'black', ((470, 220), (750, 520)))
            pygame.draw.rect(screen, 'grey', ((480, 230), (730, 500)))
            screen.blit(text_after_dead, (490, 700))
            screen.blit(string_rendered, (490, 300))
            screen.blit(string_rendered, (490, 300))

            quest_available = True

        except IndexError:
            pass

    if dialogue_2_enabled:
        intro_text = ("Ты снова пришёл!",
                      "Полагаю, ты выполнил мою просьбу?",
                      "Отлично, теперь в этих лесах будет спокойней.",
                      "Спасибо тебе путник.",
                      "Лёгкой тебе дороги!")

        font = pygame.font.SysFont('Haettenschweiler', 40)
        try:
            string_rendered = font.render(intro_text[dialogue_2_string_number], 1, pygame.Color('black'))
            text_after_dead = pygame.font.SysFont('Calibri', 30).render('Нажмите пробел, чтобы продолжить диалог', 1,
                                                                        pygame.Color('black'))
            pygame.draw.rect(screen, 'black', ((470, 220), (750, 520)))
            pygame.draw.rect(screen, 'grey', ((480, 230), (730, 500)))
            screen.blit(text_after_dead, (490, 700))
            screen.blit(string_rendered, (490, 300))
            screen.blit(string_rendered, (490, 300))

            quest_available = True

        except IndexError:
            pass

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

    if win:
        text_after_win = pygame.font.SysFont('Calibri', 80).render('Нажмите Esc, чтобы закончить', 1,
                                                                   pygame.Color('white'))
        congratulation = pygame.font.SysFont('Haettenschweiler', 250).render('CONGRATULATION', 1,
                                                                             pygame.Color('white'))
        screen.fill(pygame.Color(0, 0, 0))
        if not congratulation_variable:
            screen.fill(pygame.Color(0, 0, 0))
            congratulation_variable = True
        else:
            screen.blit(congratulation, (140, 305))
            congratulation_variable = False
        screen.blit(text_after_win, (270, 700))
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
               'rifleman': load_image('Rifleman.png'), 'bycicle_rider': load_image('Motobyke.png'),
               'captain': load_image('captain.png')}
teammates_image = load_image('Mage.png')
bullet_image = load_image('Arrow.png')
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
        super().__init__(water_tiles_group, all_sprites)
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
        if 1555 >= self.rect.x >= -65 and 1000 >= self.rect.y >= -100:
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
        if (pygame.sprite.spritecollide(walking_enemy_on_y[i], water_tiles_group, False)) or \
                (pygame.sprite.spritecollide(walking_enemy_on_y[i], tiles_with_trees_group, False)):
            ENEMY_STEP_ON_Y[i] = -ENEMY_STEP_ON_Y[i]
        if 1700 >= self.rect.x >= -100 and 1800 >= self.rect.y >= -70:
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
        elif enemy_type == 'captain':
            super().__init__(captain_enemy_group, all_sprites)
            self.image = enemy_image[enemy_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def captains_update(self):
        if captain_rotation == 'L':
            self.image = pygame.transform.flip(enemy_image['captain'], 1, 0)
        elif captain_rotation == 'R':
            self.image = pygame.transform.flip(enemy_image['captain'], 0, 0)


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

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        all_sprites.add(bullet)
        bullet_group.add(bullet)


class Teammates(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(teammates_group, all_sprites)
        self.image = teammates_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bullet_group, all_sprites)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y + 60
        self.speedx = 20
        self.last_direction = None

    def update(self, direction):
        if (self.last_direction == 'L') or (self.last_direction == 'R'):
            if self.last_direction == 'L':
                direction = 'L'
            elif self.last_direction == 'R':
                direction = 'R'

        if direction == 'R':
            self.rect.x += self.speedx
            self.image = pygame.transform.flip(bullet_image, 0, 0)
            self.last_direction = 'R'
        elif direction == 'L':
            self.rect.x -= self.speedx
            self.image = pygame.transform.flip(bullet_image, 1, 0)
            self.last_direction = 'L'


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

player, level_x, level_y, walking_enemy_on_x, walking_enemy_on_y, captains, teammate_mage \
    = generate_level(load_level('first_layer.txt'))
generate_level(load_level('second_layer.txt'))
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
        elif event.type == pygame.KEYDOWN and win:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYDOWN and not dead and not win:
            if event.key == pygame.K_ESCAPE:
                escape_pressed *= -1
            if event.key == pygame.K_SPACE and not dialogue_1_enabled and not dialogue_2_enabled:
                if not shoot:
                    player.shoot()
                    arrow_throw.play().set_volume(0.25)
                    shoot = True
            if event.key == pygame.K_SPACE and dialogue_1_enabled:
                dialogue_1_string_number += 1
            if event.key == pygame.K_SPACE and dialogue_2_enabled:
                dialogue_2_string_number += 1

            if event.key == pygame.K_TAB:
                tab_pressed *= -1

            if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and not \
                    (dialogue_1_enabled or dialogue_2_enabled):
                player.rect.x -= STEP
                moving = 'L'
                arrow_moving = 'L'
                player.update()
                if pygame.sprite.groupcollide(player_group, water_tiles_group, False, False) or \
                        pygame.sprite.groupcollide(player_group, tiles_with_trees_group, False, False):
                    player.rect.x += STEP
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and not \
                    (dialogue_1_enabled or dialogue_2_enabled):
                player.rect.x += STEP
                moving = 'R'
                arrow_moving = 'R'
                player.update()
                if pygame.sprite.groupcollide(player_group, water_tiles_group, False, False) or \
                        pygame.sprite.groupcollide(player_group, tiles_with_trees_group, False, False):
                    player.rect.x -= STEP
            elif (event.key == pygame.K_w or event.key == pygame.K_UP) and not \
                    (dialogue_1_enabled or dialogue_2_enabled):
                player.rect.y -= STEP
                if pygame.sprite.groupcollide(player_group, water_tiles_group, False, False) or \
                        pygame.sprite.groupcollide(player_group, tiles_with_trees_group, False, False):
                    player.rect.y += STEP
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and not \
                    (dialogue_1_enabled or dialogue_2_enabled):
                player.rect.y += STEP
                if pygame.sprite.groupcollide(player_group, water_tiles_group, False, False) or \
                        pygame.sprite.groupcollide(player_group, tiles_with_trees_group, False, False):
                    player.rect.y -= STEP

            if event.key == pygame.K_z:
                music.stop()
                music.play().set_volume(0.25)

    for i in range(len(captains)):
        if captains[i].rect.y + 53 > player.rect.y > captains[i].rect.y - 53 and not enemy_shoot and not dead and \
                not win:
            if captains[i].rect.x <= 767:
                captain_rotation = 'L'
            elif captains[i].rect.x >= 767:
                captain_rotation = 'R'
            if -25 < captains[i].rect.x < 1575:
                captains[i].captains_update()

    for i in range(len(walking_enemy_on_x)):
        walking_enemy_on_x[i].walk_x()

    for i in range(len(walking_enemy_on_y)):
        walking_enemy_on_y[i].walk_y()

    camera.update(player)

    bullet_group.update(arrow_moving)

    if not bullet_group:
        shoot = False

    if pygame.sprite.groupcollide(bullet_group, enemy_group, True, True):
        dead_sound.play().set_volume(0.25)
    elif pygame.sprite.groupcollide(bullet_group, danger_enemy_group, True, False):
        arrow_collide_sprite.play().set_volume(0.25)
    elif pygame.sprite.groupcollide(bullet_group, tiles_with_trees_group, True, False):
        arrow_collide_sprite.play().set_volume(0.25)
    elif pygame.sprite.groupcollide(bullet_group, teammates_group, True, False):
        arrow_collide_sprite.play().set_volume(0.25)
    elif pygame.sprite.groupcollide(bullet_group, water_tiles_group, True, False):
        arrow_collide_sprite.play().set_volume(0.25)
    elif pygame.sprite.groupcollide(bullet_group, captain_enemy_group, True, False):
        arrow_collide_sprite.play().set_volume(0.25)

    if pygame.sprite.groupcollide(player_group, enemy_group, False, True):
        dead_sound.play().set_volume(0.25)
    elif pygame.sprite.groupcollide(player_group, captain_enemy_group, False, True):
        dead_sound.play().set_volume(0.25)
        commanders_count -= 1
    elif pygame.sprite.groupcollide(player_group, danger_enemy_group, True, False):
        music.stop()
        game_over.play().set_volume(0.25)
        dead = True

    for sprite in all_sprites:
        camera.apply(sprite)

    screen_fill()

    if pygame.sprite.groupcollide(player_group, teammates_group, False, False):
        if dialogue_1_string_number <= 7 and commanders_count != 0:
            dialogue_1_enabled = True
        elif dialogue_1_string_number == 8:
            dialogue_1_enabled = False
        if dialogue_2_string_number <= 5 and not dialogue_1_enabled and commanders_count == 0:
            dialogue_2_enabled = True
        elif dialogue_2_string_number == 6:
            dialogue_2_enabled = False

    if not pygame.sprite.groupcollide(player_group, teammates_group, False, False):
        if dialogue_1_string_number != 7 and commanders_count != 0:
            dialogue_1_enabled = False
            dialogue_1_string_number = 0
        if dialogue_2_string_number != 5 and not dialogue_1_enabled and commanders_count == 0:
            dialogue_2_enabled = False
            dialogue_2_string_number = 0

    if commanders_count == 0:
        quest_available = False

    if dialogue_2_string_number == 5 and not win:
        music.stop()
        game_win.play().set_volume(0.25)
        win = True

terminate()
