import json
import os
import random
import sys
from math import sqrt, degrees, asin

import pygame
import global_variables as gb

import obj


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.getcwd() + newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_image(name, color_key=None):
    fullname = os.path.join('res', name)

    try:
        image = pygame.image.load(resource_path(fullname)).convert()
    except Exception as e:
        print('failed to load image %s. stack:' % fullname, e)
        image = pygame.image.load(resource_path('res/missing.png')).convert()

    if color_key is not None and not 0:
        if color_key == -1:
            color_key = image.get_at((0, 0))

        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(name):
    try:
        if name == 'barrens':
            from levels import barrens as lvl
        if name == 'start':
            from levels import start as lvl
        if name == 'old_house':
            from levels import old_house as lvl
        if name == 'hub':
            from levels import hub as lvl
        print(name)
        return lvl
    except Exception as e:
        print('stack:', e)
        raise ImportError


def generate_level(lvl):
    new_player, x, y = None, None, None
    fx, fy = lvl.playerpos

    gb.tile_width, gb.tile_height = lvl.tile_size
    map = lvl.tile_map
    for iy in range(len(map)):
        for ix in range(len(map[iy])):
            cur_cntstr = lvl.tile_images_links[map[iy][ix]][0]
            if cur_cntstr is obj.Emptiness:
                if 0 < iy < len(map) - 1 and 0 < ix < len(map[iy]) - 1:
                    obj.Emptiness(ix, iy, map)
            else:
                img = (lvl.tile_images_links[map[iy][ix]][1][0])
                color_key = -1
                if type(img) is tuple:
                    color_key = img[1]
                    img = img[0]
                if type(img) is list:
                    img = random.choice(img)
                if len(lvl.tile_images_links[map[iy][ix]][1]) == 1:
                    cur_cntstr(ix, iy, load_image(img))
                if len(lvl.tile_images_links[map[iy][ix]][1]) > 1:
                    cur_cntstr(ix, iy, load_image(img, color_key),
                               *lvl.tile_images_links[map[iy][ix]][1][1:])

    map = lvl.items_map
    for iy in range(len(map)):
        for ix in range(len(map[iy])):
            if map[iy][ix] and lvl.items_on_ground_links[map[iy][ix]]:
                cur_cntstr = lvl.items_on_ground_links[map[iy][ix]][0]

                img_link = lvl.items_on_ground_links[map[iy][ix]][1][0]
                color_key = None

                if type(img_link) is tuple:
                    color_key = img_link[1]
                    img_link = img_link[0]

                if type(img_link) is list:
                    img_link = random.choice(img_link)
                    print(img_link, 'rand9')

                if type(img_link) is tuple:
                    color_key = img_link[1]
                    img_link = img_link[0]

                if len(lvl.items_on_ground_links[map[iy][ix]][1]) == 1:
                    cur_cntstr(ix, iy, load_image(img_link, color_key))
                if len(lvl.items_on_ground_links[map[iy][ix]][1]) > 1:
                    cur_cntstr(ix, iy, load_image(img_link, color_key),
                               *lvl.items_on_ground_links[map[iy][ix]][1][1:])
    gb.cur_lvl.init()
    new_player = obj.Player(fx, fy, lvl.bulb)
    gb.current_music_theme = lvl.music_theme
    pygame.mixer.music.stop()
    return new_player, x, y


def lvl_change(lvl):
    fade_out()
    gb.all_sprites.empty()
    gb.cur_lvl = load_level(lvl)
    gb.player, level_x, level_y = generate_level(gb.cur_lvl)


def open_eyes_animation():
    for i in range(58):
        cur_img = pygame.transform.scale(load_image('player/wake_up/wake ' + str(i) + '.png'), gb.size)
        gb.screen.blit(cur_img, (0, 0))
        pygame.display.flip()
        gb.clock.tick(15)


def door_move():
    fade_out()
    walk_in()


def fade_out():
    for i in range(255):
        alpha = max(i, 0)
        alpha_surf = pygame.Surface(gb.size)
        alpha_surf.fill((255, 255, 255, alpha))
        gb.screen.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        pygame.display.flip()


def walk_in():
    moving_right = [
        load_image('player\\' + gb.player.bulb + '\walking_right\walk_' + str(i) + '.png', -1) for i in range(1, 7)]
    counter_for_movements = 0
    for i in range(36):
        alpha_surf = pygame.Surface(gb.size)
        alpha_surf.fill((0, 0, 0, 0))
        alpha_surf.blit(moving_right[counter_for_movements], (gb.width // 2 - 36, gb.height // 2 - 48))
        counter_for_movements += 1
        if counter_for_movements == 6:
            counter_for_movements = 0
        gb.screen.blit(alpha_surf, (0, 0))
        pygame.display.flip()
        gb.clock.tick(15)
    fade_out()


def draw_inv():
    img = load_image('invertory.png', -1).convert_alpha()
    sc = pygame.Surface(gb.size, pygame.SRCALPHA)

    sc.blit(img, (0, 10))
    x, y = 0, 0
    start_pos = 100, 100
    rigth_collum = 400
    for i in range(min(16, len(gb.invertory))):
        cur_item = gb.invertory[i]
        x = i % 2 * rigth_collum
        y = i // 2 * 60

        if type(cur_item.image) is tuple:
            cur_item.image = load_image(*cur_item.image)
        if type(cur_item.image) is str:
            cur_item.image = load_image(cur_item.image, -1)
        sc.blit(cur_item.image, (start_pos[0] + x, start_pos[1] + y))

        font = pygame.font.Font(None, 50)
        text = font.render(str(cur_item.name), 1, (167, 95, 12))
        sc.blit(text, (start_pos[0] + x + 70, start_pos[1] + y))

    gb.screen.blit(sc, (0, 10))


def pick_up_bulb_animation():
    frames = [
        pygame.transform.scale(load_image(r'pickup_bulb_animation\b' + str(i) + '.png', (0, 0, 0)), gb.size) for i in
        range(0, 10)]
    counter_for_movements = 0
    for i in range(199):
        alpha_surf = pygame.Surface(gb.size)
        # alpha_surf.fill((0, 0, 0, 0))
        try:
            alpha_surf.blit(frames[counter_for_movements], (0, 0))
        except:
            alpha_surf.blit(frames[-1], (0, 0))
        gb.screen.blit(alpha_surf, (0, 0))

        if i % 10 == 0 and counter_for_movements < 9:
            if counter_for_movements < 3:
                fade_out()
            counter_for_movements += 1
        pygame.display.flip()
        gb.clock.tick(30)
    fade_out()


def pick_up_event():
    gb.intractable_group.update("pick_up")


def draw_msg():
    sc = load_image('msg.png', -1).convert_alpha()
    msg, face = gb.msg_query[0]
    font = pygame.font.Font(None, 30)
    msgs = msg.msg.split('\n')
    for line in range(len(msgs)):
        text = font.render(str(msgs[line]), 1, (255, 255, 255))
        sc.blit(text, (30, 25 + 35 * line))

    sc.blit(face, (710, 5))

    gb.screen.blit(sc, (100, 565))


def face(person, mood='idle'):
    if mood == 'idle':
        imgs = [load_image('faces\\' + person + '\\' + person + str(i) + '.png', -2) for i in range(6)]
        return pygame.transform.scale(random.choice(imgs), (150, 150))
    else:
        return pygame.transform.scale(load_image('faces\\' + person + '\\' + person + '_' + mood + '.png', -2),
                                      (150, 150))


def make_color_darker(color, percentage):
    r, g, b = color
    percentage *= 0.001


def darken():
    alpha = 70
    alpha_surf = pygame.Surface(gb.size)
    alpha_surf.fill((alpha, alpha, alpha, 255))
    gb.screen.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


def distance_between_points(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def angle_between_points(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return round(degrees(asin((y2 - y1) / distance_between_points(pos1, pos2))))


def direction_to_star_at(pos1, pos2):
    #
    #
    ang = angle_between_points(pos1, pos2)
    if 45 >= ang >= 135:
        return 1
    if 135 >= ang >= 225:
        return 2
    if 225 > ang > 315:
        return 3
    if 315 > ang or ang < 45:
        return 4


def mod(x):
    return x if x > 0 else -x


def play_sound(sound):
    pygame.mixer.Sound('res/sounds/' + sound + '.wav').play()


def play_music(song=None):
    try:
        pygame.mixer.music.stop()
        if song:
            file = song
        else:
            file = random.choice(os.listdir('res/music/'))
        pygame.mixer.music.load('music/' + file)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.3)
    except Exception as e:
        print('failed to load music queue. stack:', e)


def debug_hud():
    data = """
    vX:%d   X_tile:%f   
    vY:%d   Y_tile:%f
    vX_act:%d
    vY_act:%d   sprites:%s
    start X:%d, Y:%d
    """ % (
        gb.velocity_x, gb.playerpos_x / gb.tile_width, gb.velocity_y, gb.playerpos_y / gb.tile_height,
        gb.velocity_x_actual,
        gb.velocity_y_actual, str(gb.all_sprites), gb.playerpos_x, gb.playerpos_y)
    font = pygame.font.Font(None, 30)
    msgs = data.split('\n')
    for line in range(len(msgs)):
        text = font.render(str(msgs[line]), 1, (255, 0, 0))
        gb.screen.blit(text, (10, 10 + 35 * line))


def digit_password_ask(password):
    """
    :param password: str
    :return: bool
    """
    nums = num1, num2, num3, num4 = [0, 0, 0, 0]
    cur = 0

    font = pygame.font.Font(None, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == gb.right:
                    cur += 1
                    if cur == 4:
                        cur = 0
                if event.key == gb.left:
                    cur -= 1
                    if cur == -1:
                        cur = 3
                if event.key == gb.up:
                    nums[cur] += 1
                    if nums[cur] == 10:
                        nums[cur] = 0
                if event.key == gb.down:
                    nums[cur] -= 1
                    if nums[cur] == -1:
                        nums[cur] = 9
                if event.key == gb.action:
                    return ''.join([str(i) for i in nums]) == password

        string_rendered = pygame.Surface((600, 100))

        for i in range(4):
            str1 = font.render(str(nums[i]), 1, pygame.Color('yellow' if cur == i else 'white'))
            string_rendered.blit(str1, (i * 40, 0))
        gb.screen.fill((0, 0, 0))
        gb.screen.blit(string_rendered, (gb.width // 2 - 90, gb.height // 2 - 30))
        pygame.display.flip()
        gb.clock.tick(gb.FPS)


def light_bulb_install():
    frames = [
        pygame.transform.scale(load_image(r'stand_animation/stand ' + str(i) + '.png', (0, 0, 0)), gb.size) for i in
        range(0, 4)]
    counter_for_movements = 0
    fade_out()
    for i in range(150):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gb.running = False

        alpha_surf = pygame.Surface(gb.size)
        # alpha_surf.fill((0, 0, 0, 0))
        try:
            frame = 0
            if counter_for_movements > 2:
                frame = 1
            if counter_for_movements > 4:
                frame = 2
            if counter_for_movements > 6:
                frame = 3

            alpha_surf.blit(frames[frame], (0, 0))
        except:
            alpha_surf.blit(frames[-1], (0, 0))
        gb.screen.blit(alpha_surf, (0, 0))

        if i % 10 == 0 and counter_for_movements < 8:
            counter_for_movements += 1
        pygame.display.flip()
        gb.clock.tick(30)
    fade_out()


def ask_nap():
    orig_frame = pygame.Surface(gb.size)
    orig_frame.blit(gb.screen, (0, 0))
    var_ques = ['It\'s a bed. It\'s soft and comfortable.\nMay i take a little nap?',
                'aw...I\'m quite tired of walking.\nIs it alright to take a little nap before we go?',
                'aw...%s, I\'m quite tired of walking.\nIs it alright to take a little nap before we go?' % gb.player_name,
                ]
    var_yes = ['yeah sure.',
               'Yeah it\'s alright.',
               'Sure, have a good night!'
               ]
    var_no = ['I think, we have what to do know.',
              'Not now, maybe a little bit later?',
              'uhhh...no.']
    msg, face1, face2 = random.choice(var_ques), face('niko', 'yawn'), face('niko')

    yes = random.choice(var_yes)
    no = random.choice(var_no)

    is_yes = False

    font = pygame.font.Font(None, 30)
    font2 = pygame.font.Font(None, 25)
    selection = load_image('selection.png')
    counter = 0

    while True:

        if counter < 50:
            counter += 1
            fface = face1
        else:
            fface = face2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gb.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return is_yes
                if event.key == gb.up or event.key == gb.down:
                    is_yes = not is_yes

        frame = pygame.Surface(gb.size)
        frame.blit(orig_frame, (0, 0))
        sc = load_image('msg.png', -1).convert_alpha()

        msgs = msg.split('\n')
        for line in range(len(msgs)):
            text = font.render(str(msgs[line]), 1, (255, 255, 255))
            sc.blit(text, (30, 25 + 35 * line))
        yellow = (255, 241, 35)
        white = (255, 255, 255)

        sc.blit(selection, (25, 80 if is_yes else 105))

        yes_txt = font2.render(yes, 1, yellow if is_yes else white)
        no_txt = font2.render(no, 1, yellow if not is_yes else white)
        sc.blit(yes_txt, (30, 85))
        sc.blit(no_txt, (30, 110))

        sc.blit(fface, (710, 5))

        frame.blit(sc, (100, 565))

        gb.screen.blit(frame, (0, 0))
        pygame.display.flip()
        gb.clock.tick(60)


def save():
    file_entry = open('res/data.txt', 'w')
    data = [gb.cur_lvl.name, (gb.playerpos_x, gb.playerpos_y)]
    json_file = json.dumps(data)
    file_entry.write(json_file)


def load():
    file_entry = open('res/data.txt', 'r')
    try:
        data = json.loads(file_entry.read())
        cur_lvl_name, player_pos = data
        gb.from_save = True
        return cur_lvl_name, player_pos
    except Exception as e:
        gb.from_save = False
        print('failed to load save, stack:', e)
        return None



