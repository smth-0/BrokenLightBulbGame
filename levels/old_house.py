import random

import obj
import utility_functions as uf
import global_variables as gb
import pygame


class DoorClosed(obj.AbstractDialogueTile):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.add(gb.not_passable_group)
        self.add(gb.intractable_group)

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    uf.play_sound('door_locked')
                    var = ['It\'s closed.',
                           'I can\'t open it.',
                           'Door is locked.',
                           ]
                    gb.msg_query.append((obj.MSG(random.choice(var)), uf.face('niko', 'distressed')))
                    gb.mode = 1


class DynamicDoor(obj.DoorTile):
    def update(self, *args):
        if pygame.sprite.collide_rect(self, gb.player.collisionObj) and self.goto_pos:
            if gb.player.bulb == 'without_bulb':
                gb.player.collisionObj.rect.x += self.goto_pos[0] * gb.tile_width
                gb.player.collisionObj.rect.y += self.goto_pos[1] * gb.tile_height
                uf.door_move()
            else:
                uf.lvl_change('hub')


class Lightbulb(obj.ItemOnGround):
    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    if self.item_in_inventory not in gb.invertory:
                        gb.invertory.append(self.item_in_inventory)
                        gb.darken = False
                        gb.player.bulb = 'with_bulb'
                        gb.player.indexed = True
                        uf.pick_up_bulb_animation()
                        gb.all_sprites.update()
                        gb.all_sprites.draw(gb.screen)
                        pygame.display.flip()
                        if self.item_in_inventory.descriptions:
                            gb.mode = 1
                            get = self.item_in_inventory.descriptions.get()
                            if any([i.id == 1 for i in gb.invertory]):
                                get = (obj.MSG('Definitely lighter than battery!'), uf.face('niko', 'smile'))

                            gb.msg_query.append(get)
                        self.kill()


class PC(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.image = pygame.transform.scale(self.image, (64, 50))
        self.rect.y -= 30
        self.rect.x += self.rect.w // 8
        self.called = 0

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    uf.play_sound('pc_on')
                    if self.called == 0:
                        gb.msg_query.append((obj.MSG('uhh... It is turned off...'), uf.face('niko', 'upset')))
                        gb.msg_query.append((obj.MSG('I don\'t think i can turn it on...'), uf.face('en', 'speak')))
                        gb.msg_query.append((obj.MSG('I don\'t even know how to use it! '), uf.face('niko', 'huh')))
                        gb.msg_query.append(
                            (obj.MSG('It seems like it is my reflection there'), uf.face('en', 'smile')))
                        gb.msg_query.append((obj.MSG(
                            'uhh... I missed one thing.\nWhich I was hearing time by time from mama!'),
                                             uf.face('en')))
                        gb.msg_query.append((obj.MSG('I am adorable!'), uf.face('niko', 'pancakes')))
                        self.called = 1
                    elif self.called == 1:
                        gb.msg_query.append((obj.MSG('password tip: flower_count^4'), uf.face('pc', '1')))
                        gb.msg_query.append((obj.MSG('ok. maybe it will be useful.'), uf.face('niko', 'what')))
                        self.called = 2
                    elif self.called == 2:
                        ans = uf.digit_password_ask('6561')
                        if ans:
                            gb.msg_query.append((obj.MSG('PASSWORD ACCEPTED. You are adorable.\nACCESS TO TV GRANTED.'),
                                                 uf.face('pc', '1')))
                            gb.msg_query.append((obj.MSG('ok.'), uf.face('niko', 'what')))
                            gb.PC_access_granted = True
                        else:
                            gb.msg_query.append((obj.MSG('WRONG PASSWORD. Maybe next time?'), uf.face('pc', '1')))
                            gb.msg_query.append((obj.MSG('yea... next time...'), uf.face('niko')))
                    gb.mode = 1


class Coach(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        coef = 1.0
        self.image = pygame.transform.scale(self.image, (int(self.rect.w * coef), int(self.rect.h * coef)))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * gb.tile_width - 40
        self.rect.y = pos_y * gb.tile_height - 40

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    # uf.play_sound('pc_on')
                    var = ['Looks old.',
                           'It\'s a sofa.',
                           'I don\'t think i want to sleep here.',
                           ]
                    gb.msg_query.append((obj.MSG(random.choice(var)), uf.face('niko')))
                    gb.mode = 1


class Summit(obj.Prop):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        coef = 2.0
        self.image = pygame.transform.scale(self.image, (int(self.rect.w * coef), int(self.rect.h * coef)))
        self.remove(gb.not_passable_group)


class Window(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.rect.x = pos_x * gb.tile_width
        self.rect.y = pos_y * gb.tile_height

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    # uf.play_sound('pc_on')
                    chance = 20 * [0]
                    chance.append(1)
                    if random.choice(chance) == 0:
                        var = ['It\'s a window. Indeed.',
                               'There\'s nothing. Like it\'s not a window at all.',
                               'Imagine being blind and thinking that\nwindows are invented to hurt your hands when you close them.',
                               ]
                        gb.msg_query.append((obj.MSG(random.choice(var)), uf.face('niko')))
                    else:
                        gb.msg_query.append((obj.MSG('You know what is madness? It\'s doing the same over and over.\n' +
                                                     'With hope that sometime you will get another result...'),
                                             uf.face('niko', 'sad')))

                    gb.mode = 1


class Hole(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        self.called = False
        super().__init__(pos_x, pos_y, image)

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    # uf.play_sound('pc_on')
                    if gb.player.bulb == 'without_bulb' or self.called:
                        var = ['It\'s a hole in a floor. Indeed. Nothing really special.',
                               'There\'s nothing. It\'s a hole.',
                               'ehh... I will try to avoid falling into it, ok?',
                               ]
                        gb.msg_query.append((obj.MSG(random.choice(var)), uf.face('niko')))
                    else:
                        gb.msg_query.append(
                            (obj.MSG('oh, I see something there! In the dark!'), uf.face('niko', 'what')))
                        gb.msg_query.append((obj.MSG(
                            'oh uh... sorry sweetie, i lasted here too much.\nGood luck you and %s.' % gb.player_name),
                                             uf.face('lunar', '0')))
                        gb.msg_query.append((obj.MSG('WHAT THE...'), uf.face('niko', 'wtf')))
                        gb.msg_query.append((obj.MSG('Ok it seems like sometimes there\'s a things to forget.'),
                                             uf.face('niko', 'what2')))
                        self.called = True
                    gb.mode = 1


class Fridge(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.rect.x = pos_x * gb.tile_width
        self.rect.y = pos_y * gb.tile_height
        self.called = False

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    # uf.play_sound('pc_on')

                    var = ['This fridge is too cold to touch it. Unfortunately.',
                           'Ouch! I think it\'s better to not touch such a cold thing.',
                           'ehh...no alcohol this time.',
                           ]
                    gb.msg_query.append((obj.MSG(random.choice(var)), uf.face('niko')))
                    give_or_not_to_give = False
                    for i in gb.invertory:
                        if i.id == 3:
                            give_or_not_to_give = True
                    if give_or_not_to_give and not self.called:
                        gb.msg_query.append(
                            (obj.MSG('Wait. I know how to open it.\nLet me try!'), uf.face('niko')))
                        gb.msg_query.append(
                            (
                                obj.MSG('I used gloves to not get frosty and found this weird glowing box.'),
                                uf.face('niko')))
                        gb.invertory.append(battery)
                        self.called = True
                    gb.mode = 1


class Shelf(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.rect.x = pos_x * gb.tile_width
        self.rect.y = pos_y * gb.tile_height

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    # uf.play_sound('pc_on')w
                    var = ['Dusty books. More dusty books to dusty books king.',
                           'How would you call dusty books king? I would call him Dusty.',
                           'ehh...no remotes this time.',
                           ]
                    gb.msg_query.append((obj.MSG(random.choice(var)), uf.face('niko')))
                    gb.mode = 1


class Table(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.rect.x = pos_x * gb.tile_width
        self.rect.y = pos_y * gb.tile_height + (self.rect.h // 2) - 5

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    # uf.play_sound('pc_on')
                    give_or_not_to_give = True
                    for i in gb.invertory:
                        if i.id == 3:
                            give_or_not_to_give = False
                    if give_or_not_to_give:
                        gb.msg_query.append((obj.MSG('oh, look! I found this warm gloves!'), uf.face('niko', 'smile')))
                        gb.invertory.append(gloves)
                    else:
                        gb.msg_query.append((obj.MSG('Uhh... there\'s no water in it.'), uf.face('niko')))
                    gb.mode = 1


class Flower(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.rect.x = pos_x * gb.tile_width
        self.rect.y = pos_y * gb.tile_height - (self.rect.h // 2)

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    var = ['Ugly flower.',
                           'Looks like a dead but it\'s not.',
                           'ehh...',
                           'I think it\'s better to watch out. These plants are everywhere.',
                           ]
                    gb.msg_query.append((obj.MSG(random.choice(var)), uf.face('niko')))
                    gb.mode = 1


class TV(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.rect.x = pos_x * gb.tile_width
        self.rect.y = pos_y * gb.tile_height - (self.rect.h // 2) - 5
        self.second_pic = uf.load_image('tiles/old_house/TV2.png', -1)

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    do_we_have_battery = False
                    for i in gb.invertory:
                        if i.id == 3:
                            do_we_have_battery = True

                    if (do_we_have_battery and gb.PC_access_granted) or gb.debug:
                        self.image = self.second_pic
                        x, y = -5, 25
                        gb.player.collisionObj.rect.x += x * gb.tile_width
                        gb.player.collisionObj.rect.y += y * gb.tile_height
                        gb.velocity_y, gb.velocity_y_actual = 1, 1
                        gb.velocity_x, gb.velocity_x_actual = 0, 0
                        uf.door_move()
                        gb.msg_query.append((obj.MSG('whaaa...'), uf.face('niko', 'wtf')))
                        gb.current_music_theme = 'Nightmargin (Casey Gu), ft Eliza Velasquez and Michael Shirt - OneShot Soundtrack - 03 Puzzle Solved.wav'
                    elif gb.PC_access_granted or do_we_have_battery:
                        gb.msg_query.append((obj.MSG('Probably, something is missing.'), uf.face('niko')))
                    else:
                        var = ['It\'s a broken TV.',
                               'It seems like something can be putted in.',
                               'It\'s a weird TV!',
                               'No sparks this time.',
                               ]
                        gb.msg_query.append((obj.MSG(random.choice(var)), uf.face('niko')))
                    gb.mode = 1


class Sofa(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        coef = 1.0
        self.image = pygame.transform.scale(self.image, (int(self.rect.w * coef), int(self.rect.h * coef)))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * gb.tile_width
        self.rect.y = pos_y * gb.tile_height

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    # uf.play_sound('pc_on')
                    var = ['Looks old.',
                           'It\'s a chair.',
                           'I don\'t think i want to seat here.',
                           ]
                    gb.msg_query.append((obj.MSG(random.choice(var)), uf.face('niko')))
                    gb.mode = 1


wall_down = ['tiles/old_house/wallD%d.png' % i for i in range(1, 6)]
wall_down.extend(['tiles/old_house/wallD1.png' for i in range(1, 7)])

wall2 = ['tiles/old_house/wall%d.png' % i for i in range(1, 4)]

floor = ['tiles/old_house/plank1.png' for i in range(1, 5)]
floor2 = 'tiles/old_house/floor2.png'
floor.extend(['tiles/old_house/plank%d.png' % i for i in range(1, 7)])

playerpos = 4, 4

tile_size = tile_width, tile_height = 50, 50
tile_images_links = {'w1': [obj.AbstractWall, [wall2]],
                     'w2': [obj.AbstractWall, [wall_down]],
                     'wl': [obj.AbstractWall, ['tiles/tile2.png']],
                     'fl': [obj.AbstractTile, [floor]],
                     'f2': [obj.AbstractTile, [floor2]],
                     'd1': [obj.AbstractWall, ['tiles/old_house/door1.png']],
                     'd2': [DoorClosed, ['tiles/old_house/door2.png']],
                     'e2': [obj.AbstractTile, ['tiles/tile2.png']],
                     'dr': [DynamicDoor, ['tiles/tile3.png', (-4, -43)]],
                     '  ': [obj.Emptiness, ['tiles/empty.png']],
                     }
tile_map = [
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', 'w1', 'w1', 'd1', 'w1', 'w1', 'w1', '  ', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', '  ', '  '],
    ['  ', '  ', 'w2', 'w2', 'd2', 'w2', 'w2', 'w2', 'w1', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', '  ', '  '],
    ['  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'w2', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', 'fl', 'fl', 'fl', '  ', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', '  ', '  ', 'fl', 'w1', 'w1', 'w1', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w1', 'w1', 'fl', 'w2', 'w2', 'w2', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'w2', 'w2', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', '  ', 'w1', 'w1', 'fl', 'w1', 'w1', 'w1', '  ', '  '],
    ['  ', '  ', '  ', '  ', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w1', 'w2', 'w2', 'fl', 'w2', 'w2', 'w2', '  ', '  '],
    ['  ', '  ', '  ', '  ', 'f2', 'f2', 'f2', 'f2', 'f2', 'f2', 'w2', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', 'f2', 'f2', 'f2', 'f2', 'f2', 'f2', 'f2', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'w1', 'fl', 'w1', 'w1', 'w1', 'w1', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'w2', 'fl', 'w2', 'w2', 'w2', 'w2', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'dr', 'dr', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'e2', 'e2', 'e2', 'e2', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'e2', 'e2', 'e2', 'e2', 'e2', 'e2', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'e2', 'e2', 'e2', 'e2', 'e2', 'e2', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'e2', 'e2', 'e2', 'e2', 'e2', 'e2', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'e2', 'e2', 'e2', 'e2', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
]

battery = obj.ItemInInventory(('items/battery.png', 0), 1, 'charged battery',
                              obj.Desc('niko',
                                       [obj.MSG('Looks cool! i wonder what it does...'),
                                        obj.MSG('Looks like a battery, but very heavy one...'),
                                        obj.MSG('I hope i will not get electric shock...', 'smile')
                                        ])
                              )

bulb = obj.ItemInInventory('items/lightbulb.png', 2, 'lightbulb',
                           obj.Desc('niko',
                                    [
                                        obj.MSG('It lights itlesf up? wow!'),
                                        obj.MSG('I don\'t think it will fit in my pocket'),
                                        obj.MSG('WAAARM!', 'smile')
                                    ]
                                    )
                           )
gloves = obj.ItemInInventory('items/gloves.png', 3, 'warm gloves', obj.Desc('niko',
                                                                            [
                                                                                obj.MSG(
                                                                                    'I think I will found a way to use these.'),
                                                                                obj.MSG(
                                                                                    'It\'s not winter but who knows where they come being useful?'),
                                                                                obj.MSG('WAAARM!', 'smile')
                                                                            ]
                                                                            )
                             )

holes = [('tiles/old_house/hole%d.png' % i, -1) for i in range(1, 5)]
flowers = [('tiles/old_house/flower%d.png' % i, -1) for i in range(1, 8)]

music_theme = 'Nightmargin (Casey Gu), ft Eliza Velasquez and Michael Shirt - OneShot Soundtrack - 02 Someplace I Know.wav'
items_on_ground_links = {'battery': [obj.ItemOnGround, ['items/battery.png', battery]],
                         'bulb': [Lightbulb, [('items/lightbulb.png', (0, 0, 0)), bulb]],
                         'pc': [PC, [('characters/pc/pc_off.png', -1)]],
                         'ch': [Coach, [('tiles/old_house/coach.png', -1)]],
                         'sf': [Sofa, [('tiles/old_house/chair.png', (255, 0, 0))]],
                         'sm': [Summit, ['summit.png']],
                         'ho': [Hole, [holes]],
                         'wd': [Window, ['tiles/old_house/window.png']],
                         'sh': [Shelf, ['tiles/old_house/shelf.png']],
                         'fr': [Fridge, [('tiles/old_house/fridge.png', -1)]],
                         'tb': [Table, [('tiles/old_house/table.png', (255, 0, 0))]],
                         'fw': [Flower, [flowers]],
                         'TV': [TV, [('tiles/old_house/TV1.png', -1)]],
                         }
items_map = [
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, 'wd', None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'fw', None, None, 'fw', None, None, None, None, None, None, None, None, None, 'fw', None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, 'sh', None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, 'pc', None, 'fw', None, None, None, None, None, None, None, 'fw', None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, 'ho', None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, 'wd', None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, 'fr', 'tb', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, 'fw', None, None, None, None, 'fw', None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'sf', None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'sf', None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'sf', None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, 'fw', None, None, None, 'TV', None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'sf', None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, 'ch', None, None, 'sf', None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'sm', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, 'bulb', None, None, None, None, None, None, None,
     None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],

]

bulb = False
def init():
    # uf.walk_in()
    uf.play_sound('door_close_heavy')
    gb.playerpos_x, gb.playerpos_y = playerpos[0] * tile_width, playerpos[1] * tile_height
    gb.PC_access_granted = False
    gb.darken = True
