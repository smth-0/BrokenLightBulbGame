import random

import obj
import utility_functions as uf
import global_variables as gb
import pygame


class Lightbulb(obj.ItemOnGround):
    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    if self.item_in_inventory not in gb.invertory:
                        gb.invertory.append(self.item_in_inventory)
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


class Dialogue1(obj.AbstractDialogueTile):
    def update(self, *args):
        if pygame.sprite.collide_rect(self, gb.player.collisionObj) and not self.called:
            gb.msg_query.append(
                (obj.MSG('Oh, look! There\'s a light over there!'), uf.face('niko')))
            gb.mode = 1
            self.called = True


class Dialogue2(obj.AbstractDialogueTile):
    def update(self, *args):
        if pygame.sprite.collide_rect(self, gb.player.collisionObj) and not self.called:
            gb.msg_query.append(
                (obj.MSG('Mama said me once - never give up. I will never give up. '), uf.face('niko', 'eyeclosed')))
            gb.mode = 1
            self.called = True


class PC(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        # self.image = pygame.transform.scale(self.image, (64, 50))

        self.rect.y -= 30
        self.rect.x -= 10

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    uf.play_sound('pc_on')
                    gb.msg_query.append(
                        (obj.MSG('uhh... i remember one of this speaking to me'), uf.face('niko', 'upset')))
                    gb.msg_query.append((obj.MSG('Yes. To you. And to %s.' % gb.player_name), uf.face('pc', '1')))
                    text = """You awoke in a unfamiliar place.
You encountered a being of no form.
Telling you and %s there is only One Shot.
When you experienced that world for the first time.
You saw with your own two eyes the state of that world.
There was not much you could have done, but you did.
You met two children during your journey.
One being a wise boy, and the other being a energetic girl.
There was nothing you could have done then.
You had to continue.
You helped those in need.
And they helped you in return.
You were going to help those who needed it.
You were alone.
You were not prepared for what was to come.
The choice you made.
Did not matter.
If you still didn\'t gave up, you can go there and try again.""" % gb.player_name
                    for i in text.split('\n'):
                        gb.msg_query.append((obj.MSG(i), uf.face('pc', '1')))
                    gb.mode = 1


class Bed(obj.AbstractMachinery):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(pos_x, pos_y, image)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * gb.tile_width
        self.rect.y = pos_y * gb.tile_height - 40

        # self.rect.y -= 30

    def update(self, *args):
        if args:
            if args[0] == 'pick_up':
                if pygame.sprite.collide_rect(self, gb.player.pick_up_collision):
                    gb.msg_query.append((obj.MSG('uhh... i woke up here.'), uf.face('niko')))
                    gb.mode = 1
                    print(gb.player.rect)


class Banner(obj.Prop):
    def update(self, *args):
        pass


playerpos = 6, 4

# playerpos = 7, 27

tile_size = tile_width, tile_height = 50, 50
music_theme = 'Nightmargin (Casey Gu), ft Eliza Velasquez and Michael Shirt - OneShot Soundtrack - 01 My Burden Is Light.wav'

wall_down = ['tiles/dark_corridor/down_%d.png' % i for i in range(1, 6)]
wall2 = ['tiles/dark_corridor/up_%d.png' % i for i in range(2, 4)]

tile_images_links = {'w1': [obj.AbstractWall, [wall_down]],
                     'w2': [obj.AbstractWall, [wall2]],
                     'fl': [obj.AbstractTile, ['tiles/square_tiles.png']],
                     'f2': [obj.AbstractTile, ['tiles/square_tiles_light2.png']],
                     'f9': [obj.AbstractTile, ['tiles/square_tiles_transition.png']],
                     'd1': [Dialogue1, ['tiles/square_tiles.png']],
                     'd2': [Dialogue2, ['tiles/square_tiles.png']],
                     'dr': [obj.DoorTileLevelSwitch, ['tiles/square_tiles_light.png', 'old_house']],
                     '  ': [obj.Emptiness, ['tiles/empty.png']],
                     }
tile_map = [
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'w2', 'w2', 'w2', 'w2', 'w2', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'w1', 'w1', 'w1', 'w1', 'w1', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'd1', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'f9', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'f2', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'dr', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],

]
items_on_ground_links = {'pc': [PC, [('characters/pc/pc_off.png', -1)]],
                         'bd': [Bed, [('player/bed/bed_empty.png', -1)]],
                         'b1': [Banner, [('titles/authors1.png', (0, 0, 0))]],
                         'b2': [Banner, [('titles/authors2.png', (0, 0, 0))]],
                         'b3': [Banner, [('titles/authors3.png', (0, 0, 0))]],
                         '  ': None}
items_map = [
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'bd', '  ', 'pc', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', 'b1', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'b2'],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', 'b3', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],

]

bulb = False


def init():
    gb.darken = True
    uf.open_eyes_animation()

    gb.msg_query.append((obj.MSG('It\'s not my village!'), uf.face('niko', 'wtf')))
    gb.msg_query.append((obj.MSG('Where am I?'), uf.face('niko', 'what')))
    gb.msg_query.append((obj.MSG('Am i still there?'), uf.face('niko', 'upset')))

    gb.mode = 1
