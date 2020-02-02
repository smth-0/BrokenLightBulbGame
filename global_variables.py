import getpass

import pygame

from utility_functions import load_image
coef = 1.0
size = width, height = int(960 * coef), int(720 * coef)
running = True

mode = 0
screen = pygame.display.set_mode(size)

ctrl_is_down = False
isinfocus = bool(pygame.mouse.get_focused())

mousepos = -1, -1
playerpos = (0, 0)
playerpos_x = 0
playerpos_y = 0
player_size = (52, 64)
player_name = getpass.getuser()
debug = False
current_music_theme = None
gl_comm = ''

velocity_x = 0
velocity_y = 0
velocity_x_actual = 0
velocity_y_actual = 0
prev_move = None
clock = pygame.time.Clock()
FPS = 50
player = None
invertory = []
msg_query = []
is_invertory_open = False

# groups
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
not_passable_group = pygame.sprite.Group()
intractable_group = pygame.sprite.Group()
prop_group = pygame.sprite.Group()
npc_group = pygame.sprite.Group()
light_group = pygame.sprite.Group()

mouse = pygame.sprite.Group()


tile_width = tile_height = 50
cur_lvl = None
count = 0
from_save = False
up = pygame.K_w
down = pygame.K_s
left = pygame.K_a
right = pygame.K_d
action = pygame.K_SPACE
inventory = pygame.K_e
debug_key = pygame.K_F3
darken = False