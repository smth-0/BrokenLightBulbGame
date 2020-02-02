import random

import pygame

import global_variables as gb
import utility_functions as uf


class Mouse(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__(gb.mouse)
        self.image = uf.load_image("arrow.png", (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        if bool(pygame.mouse.get_focused()):
            self.rect.x, self.rect.y = gb.mousepos
        else:
            self.rect.x, self.rect.y = (-100, -100)

    def get_event(self, *args):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, bulb):
        super().__init__(gb.all_sprites)
        sx, sy = 39, 50
        print('init player', x, y, gb.playerpos_x, gb.playerpos_y)
        self.bulb = 'with_bulb' if bulb or gb.invertory else 'without_bulb'
        self.indexed = False
        self.moving_left = [
            pygame.transform.scale(
                uf.load_image('player\\' + self.bulb + '\walking_left\walk_' + str(i) + '.png', -1), gb.player_size) for
            i in
            range(1, 7)]
        self.moving_right = [
            pygame.transform.scale(
                uf.load_image('player\\' + self.bulb + '\walking_right\walk_' + str(i) + '.png', -1), gb.player_size)
            for i in
            range(1, 7)]
        self.walking_up = [
            pygame.transform.scale(
                uf.load_image('player\\' + self.bulb + '\walking_up\walk_' + str(i) + '.png', -1), gb.player_size) for
            i in range(1, 7)]
        self.walking_down = [
            pygame.transform.scale(
                uf.load_image('player\\' + self.bulb + '\walking_down\walk_' + str(i) + '.png', -1), gb.player_size) for
            i in range(1, 7)]
        self.down = uf.load_image('player/down.png', -1)
        self.image = self.walking_down[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * gb.tile_height + gb.playerpos_x, y * gb.tile_height + gb.playerpos_y
        self.collisionObj = CollisionOfThePlayer(x, y)
        self.pick_up_collision = Pick_up_collision(x, y, self.collisionObj)
        self.light_map = Niko_lightmap(x, y)
        self.is_down = False
        self.counter_for_movements = 0

    def update(self, *args):
        self.rect.x, self.rect.y = self.collisionObj.rect.x - ((self.rect.w - self.collisionObj.rect.w) / 2), \
                                   self.collisionObj.rect.y - self.rect.h + self.collisionObj.rect.h
        self.light_map.rect = self.rect
        if self.indexed:
            self.moving_left = [
                pygame.transform.scale(
                    uf.load_image('player\\' + self.bulb + '\walking_left\walk_' + str(i) + '.png', -1), gb.player_size)
                for i in
                range(1, 7)]
            self.moving_right = [
                pygame.transform.scale(
                    uf.load_image('player\\' + self.bulb + '\walking_right\walk_' + str(i) + '.png', -1),
                    gb.player_size) for i in
                range(1, 7)]
            self.walking_up = [
                pygame.transform.scale(
                    uf.load_image('player\\' + self.bulb + '\walking_up\walk_' + str(i) + '.png', -1), gb.player_size)
                for
                i in range(1, 7)]
            self.walking_down = [
                pygame.transform.scale(
                    uf.load_image('player\\' + self.bulb + '\walking_down\walk_' + str(i) + '.png', -1), gb.player_size)
                for
                i in range(1, 7)]
            self.indexed = False

        if self.collisionObj.prevMove:
            if gb.velocity_x_actual > 0:
                self.image = self.moving_right[uf.mod(gb.velocity_x_actual) - 1]
                gb.prev_move = 'right'
            if gb.velocity_x_actual < 0:
                self.image = self.moving_left[uf.mod(gb.velocity_x_actual) - 1]
                gb.prev_move = 'left'
            if gb.velocity_y_actual > 0:
                self.image = self.walking_down[uf.mod(gb.velocity_y_actual) - 1]
                gb.prev_move = 'down'
            if gb.velocity_y_actual < 0:
                self.image = self.walking_up[uf.mod(gb.velocity_y_actual) - 1]
                gb.prev_move = 'up'

            if gb.velocity_x_actual == 0 and gb.velocity_y_actual == 0:
                if gb.prev_move == 'right':
                    self.image = self.moving_right[0]
                if gb.prev_move == 'left':
                    self.image = self.moving_left[0]
                if gb.prev_move == 'down':
                    self.image = self.walking_down[0]
                if gb.prev_move == 'up':
                    self.image = self.walking_up[0]
        if self.is_down:
            self.image = self.down


class CollisionOfThePlayer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(gb.all_sprites)
        self.image_transparent = self.image = uf.load_image('collision.png', (0, 0, 0))
        self.image_not_transparent = uf.load_image('collision.png', (100, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * gb.tile_height + gb.playerpos_x, y * gb.tile_height + gb.playerpos_y
        self.prevMove = True

    def update(self, *args):
        speed = 3 if gb.ctrl_is_down else 2
        # prev =
        if gb.mode != 0:
            speed = 0
        if gb.velocity_x_actual > 0:
            self.rect.x += speed
            gb.playerpos_x += speed
        if gb.velocity_x_actual < 0:
            self.rect.x += -speed
            gb.playerpos_x += -speed
        if gb.velocity_y_actual > 0:
            self.rect.y += speed
            gb.playerpos_y += speed
        if gb.velocity_y_actual < 0:
            self.rect.y += -speed
            gb.playerpos_y += -speed
        self.prevMove = True
        collide = False
        for i in gb.not_passable_group:
            self.image = self.image_not_transparent
            if pygame.sprite.collide_mask(i, self):
                collide = True
            self.image = self.image_transparent
        if collide:
            if gb.velocity_x_actual > 0:
                self.rect.x += -speed
                gb.playerpos_x += -speed
            if gb.velocity_x_actual < 0:
                self.rect.x += speed
                gb.playerpos_x += speed
            if gb.velocity_y_actual > 0:
                self.rect.y += -speed
                gb.playerpos_y += -speed
            if gb.velocity_y_actual < 0:
                self.rect.y += speed
                gb.playerpos_y += speed
            self.prevMove = False
        gb.gl_comm = str(self.prevMove) + ', ' + str(gb.mode)


class Pick_up_collision(pygame.sprite.Sprite):
    def __init__(self, x, y, collision_obj):
        super().__init__(gb.all_sprites)
        self.collision_obj = collision_obj
        self.horizontal = uf.load_image('pick_up_collision_horizontal.png', (0, 0, 0))
        self.vertical = uf.load_image('pick_up_collision_vertical.png', (0, 0, 0))
        self.image = self.horizontal
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * gb.tile_height + 20 + gb.playerpos_x, y * gb.tile_height + gb.playerpos_y
        self.direction = 'right'

    def update(self, *args):

        if gb.velocity_x_actual > 0:
            self.image = self.horizontal
            self.rect = self.image.get_rect()
            self.rect.x = (gb.player.collisionObj.rect.x + (gb.player.collisionObj.rect.w // 2))
            self.rect.y = gb.player.collisionObj.rect.y
        if gb.velocity_x_actual < 0:
            self.image = self.horizontal
            self.rect = self.image.get_rect()
            self.rect.x = (gb.player.collisionObj.rect.x + (gb.player.collisionObj.rect.w // 2)) - self.rect.w
            self.rect.y = gb.player.collisionObj.rect.y

        if gb.velocity_y_actual > 0:
            self.image = self.vertical
            self.rect = self.image.get_rect()
            self.rect.x = (gb.player.collisionObj.rect.x + (gb.player.collisionObj.rect.w // 2 - self.rect.w // 2))
            self.rect.y = gb.player.collisionObj.rect.y
        if gb.velocity_y_actual < 0:
            self.image = self.vertical
            self.rect = self.image.get_rect()
            self.rect.x = (gb.player.collisionObj.rect.x + (gb.player.collisionObj.rect.w // 2 - self.rect.w // 2))
            self.rect.y = gb.player.collisionObj.rect.y - self.rect.h


class Niko_lightmap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(gb.light_group)
        path = 'player/without_bulb/'

        self.moving_left = [pygame.transform.scale(uf.load_image(path + 'walking_left/light1.png', -1), gb.player_size),
                            pygame.transform.scale(uf.load_image(path + 'walking_left/light2.png', -1), gb.player_size)]
        self.moving_right = [
            pygame.transform.scale(uf.load_image(path + 'walking_right/light1.png', -1), gb.player_size),
            pygame.transform.scale(uf.load_image(path + 'walking_right/light2.png', -1), gb.player_size)]
        self.moving_down = [pygame.transform.scale(uf.load_image(path + 'walking_down/light1.png', -1), gb.player_size),
                            pygame.transform.scale(uf.load_image(path + 'walking_down/light2.png', -1), gb.player_size)]
        self.empty = uf.load_image('empty.png', -1)
        self.image = self.moving_down[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * gb.tile_height, y * gb.tile_height

    def update(self, *args):
        self.rect = gb.player.rect
        if gb.velocity_y_actual < 0:
            self.image = self.empty
        if gb.velocity_y_actual > 0:
            self.image = self.moving_down[(1 if gb.player.counter_for_movements in [1, 4] else 0) % 6]
        if gb.velocity_x_actual < 0:
            self.image = self.moving_left[(1 if gb.player.counter_for_movements in [1, 4] else 0) % 6]
        if gb.velocity_x_actual > 0:
            self.image = self.moving_right[(1 if gb.player.counter_for_movements in [1, 4] else 0) % 6]
        pass


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 100
        self.dy = 100

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - gb.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - gb.height // 2)


class AbstractTile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image=None):
        super().__init__(gb.tiles_group, gb.all_sprites)

        self.image = pygame.transform.scale(uf.load_image('tiles/tile1.png', (0, 0, 0)) if image is None else image,
                                            (gb.tile_width, gb.tile_height))

        self.rect = self.image.get_rect().move(gb.tile_width * pos_x, gb.tile_height * pos_y)
        self.rect.h, self.rect.w = gb.tile_height, gb.tile_width


class DoorTileLevelSwitch(AbstractTile):
    def __init__(self, pos_x, pos_y, image, goto):
        super().__init__(pos_x, pos_y)
        self.goto = goto
        self.image = pygame.transform.scale(image, (gb.tile_width, gb.tile_height))

    def update(self, *args):
        if pygame.sprite.collide_rect(self, gb.player.collisionObj) and self.goto:
            uf.lvl_change(self.goto)


class DoorTile(AbstractTile):
    def __init__(self, pos_x, pos_y, image, goto_pos):
        super().__init__(pos_x, pos_y)
        self.goto_pos = goto_pos
        self.image = pygame.transform.scale(image, (gb.tile_width, gb.tile_height))

    def update(self, *args):
        if pygame.sprite.collide_rect(self, gb.player.collisionObj) and self.goto_pos:
            gb.player.collisionObj.rect.x += self.goto_pos[0] * gb.tile_width
            gb.player.collisionObj.rect.y += self.goto_pos[1] * gb.tile_height
            uf.door_move()


class ItemInInventory:
    def __init__(self, image, id, name, description_list):
        self.image, self.id, self.name, self.descriptions = image, id, name, description_list


class MSG:
    def __init__(self, msg, mood='idle'):
        self.msg = msg
        self.mood = mood

    def get_msg(self):
        return self.msg, self.mood


class Desc:
    def __init__(self, person, msgs):
        self.person = person
        self.msgs = msgs

    def get(self):
        ans = random.choice(self.msgs)

        return ans, uf.face(self.person, ans.mood)


class AbstractWall(AbstractTile):
    def __init__(self, pos_x, pos_y, image=None):
        super().__init__(pos_x, pos_y, image)
        self.add(gb.not_passable_group)


class Emptiness(AbstractWall):
    def __init__(self, pos_x, pos_y, local_map):
        x, y = pos_x, pos_y
        image = pygame.transform.scale(uf.load_image('tiles/empty.png'), (gb.tile_width, gb.tile_height))
        emptiness = local_map[0][0]
        line = pygame.transform.scale(uf.load_image('tiles/line.png', (0, 0, 0)), (gb.tile_width, gb.tile_height))
        dot = pygame.transform.scale(uf.load_image('tiles/dot.png', (0, 0, 0)), (gb.tile_width, gb.tile_height))
        # lines
        upline = pygame.transform.rotate(line, -90)
        downline = pygame.transform.rotate(line, 90)
        leftline = pygame.transform.rotate(line, 0)
        rightline = pygame.transform.rotate(line, 180)

        # dots
        left_down = pygame.transform.rotate(dot, 180)
        right_down = pygame.transform.rotate(dot, -90)
        left_up = pygame.transform.rotate(dot, 90)
        right_up = pygame.transform.rotate(dot, 0)

        pos = (0, 0)
        try:
            small_map = [
                [local_map[y - 1][x - 1], local_map[y - 1][x], local_map[y - 1][x + 1]],
                [local_map[y][x - 1], local_map[y][x], local_map[y][x + 1]],
                [local_map[y + 1][x - 1], local_map[y + 1][x], local_map[y + 1][x + 1]]
            ]
        except Exception as e:
            print((x, y), 'stack:', e)
            small_map = [
                [None, None, None],
                [None, None, None],
                [None, None, None],
            ]

        # if pos_x > 0:
        #     if pos_y > 0:
        #         small_map[0][0] = local_map[pos_y - 1][pos_x - 1] is not Emptiness
        #     small_map[1][0] = local_map[pos_y][pos_x - 1] is not Emptiness
        #     if pos_y < len(local_map):
        #         small_map[0][0] = local_map[pos_y - 1][pos_x - 1] is not Emptiness
        empty = True
        if (small_map[0][1]) != emptiness:
            image.blit(upline, pos)
            empty = False
        if (small_map[1][2]) != emptiness:
            image.blit(rightline, pos)
            empty = False
        if (small_map[2][1]) != emptiness:
            image.blit(downline, pos)
            empty = False
        if (small_map[1][0]) != emptiness:
            image.blit(leftline, pos)
            empty = False

        if (small_map[0][0]) != emptiness:
            image.blit(left_up, pos)
            empty = False
        if (small_map[0][2]) != emptiness:
            image.blit(right_up, pos)
            empty = False
        if (small_map[2][2]) != emptiness:
            image.blit(right_down, pos)
            empty = False
        if (small_map[2][0]) != emptiness:
            image.blit(left_down, pos)
            empty = False

        if not empty:
            super().__init__(pos_x, pos_y, image)
            self.add(gb.not_passable_group)


class Prop(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(gb.all_sprites)
        self.add(gb.not_passable_group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * gb.tile_width + gb.tile_width // 2 - self.rect.w // 2
        self.rect.y = pos_y * gb.tile_height + gb.tile_height // 2 - self.rect.h // 2


class AbstractMachinery(Prop):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.add(gb.intractable_group)


class AbstractNPC(Prop):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.add(gb.npc_group)


class ItemOnGround(Prop):
    def __init__(self, pos_x, pos_y, image, item_in_inventory):
        super().__init__(pos_x, pos_y, image)
        self.add(gb.intractable_group)
        self.item_in_inventory = item_in_inventory

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    if self.item_in_inventory not in gb.invertory:
                        gb.invertory.append(self.item_in_inventory)
                        if self.item_in_inventory.descriptions:
                            gb.mode = 1
                            get = self.item_in_inventory.descriptions.get()
                            gb.msg_query.append(get)
                    self.kill()


class AbstractDialogueTile(AbstractTile):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.called = False


class SaveBed(AbstractMachinery):
    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    if uf.ask_nap():
                        uf.fade_out()
                        uf.save()
                        exit(0)
                    else:
                        gb.msg_query.append((MSG('ok, maybe later.'), uf.face('niko', 'distressed')))
                        gb.mode = 1


class DynamicClickableDoor(AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.passable = False
        self.closed = uf.load_image('tiles/barrens/ddoor1.png', (255, 0, 0))
        self.opened = uf.load_image('tiles/barrens/ddoor2.png', (255, 0, 0))
        self.called = False

    def update(self, *args):
        if args:
            if args[0] == 'click':
                x, y = gb.mousepos
                if self.rect.x <= x <= self.rect.x + self.rect.w and self.rect.y <= y <= self.rect.y + self.rect.h:
                    self.passable = not self.passable
                    if self.passable:
                        if self in gb.not_passable_group:
                            self.remove(gb.not_passable_group)
                            self.image = self.opened
                    else:
                        if self not in gb.not_passable_group:
                            self.add(gb.not_passable_group)
                            self.image = self.closed
                            if pygame.sprite.collide_rect(gb.player.collisionObj, self):
                                if gb.player.bulb == 'with_bulb':
                                    self.called = True
                                    gb.msg_query.append((MSG('WHY DID YOU DO THIS?!\n my coat is now so wet! Oh wait...'),
                                                         uf.face('niko', 'what')))
                                    gb.msg_query.append((MSG('WHERE\'S THE BULB?'), uf.face('niko', 'what')))
                                    gb.player.down = True
                                    gb.mode = 1

                    uf.play_sound('door_locked')
            if args[0] == 'pick_up':
                if not self.passable:
                    var = ['ehh... I don\'t want to get wet.',
                           'There\'s slight mark on side.\nIt says "pure energy PSU required."\nI wonder what it means.',
                           'It\'s a trap door. ',
                           ]
                else:
                    var = ['ehh... I don\'t want to get wet.\nPlease do not open it while I\'m on it.',
                           '"pure energy PSU required." mark on side probably means power of gods.',
                           'It\'s a trap door. You closed it. Obviously',
                           ]
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    gb.msg_query.append((MSG(random.choice(var)), uf.face('niko')))
                    gb.mode = 1
            if args[0] == 'animation':
                if self.called and pygame.sprite.collide_rect(gb.player.collisionObj, self):
                    uf.broken_bulb()
                    gb.player.collisionObj.rect.y += 64
                if self not in gb.not_passable_group and not pygame.sprite.collide_rect(gb.player.collisionObj, self):
                    self.add(gb.not_passable_group)
                    self.passable = False
                    self.image = self.closed
