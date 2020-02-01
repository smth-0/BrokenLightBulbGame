import random
# todo
import obj
import utility_functions as uf
import global_variables as gb
import pygame

playerpos = 24, 5
bulb = True
tile_size = tile_width, tile_height = 64, 64

wall_down = ['tiles/barrens/down_%d.png' % i for i in range(1, 6)]
wall2 = ['tiles/barrens/wallG%d.png' % i for i in range(2, 6)]
floor = ['tiles/barrens/floor_%d.png' % i for i in range(1, 11)]

tile_images_links = {'w1': [obj.AbstractWall, ['tiles/barrens/wallG1.png']],
                     'w2': [obj.AbstractWall, [wall2]],
                     'fl': [obj.AbstractTile, [floor]],
                     'f2': [obj.AbstractTile, ['tiles/square_tiles_light2.png']],
                     'f9': [obj.AbstractTile, ['tiles/square_tiles_transition.png']],
                     'dr': [obj.DoorTileLevelSwitch, ['tiles/square_tiles_light.png', 'old_house']],
                     '  ': [obj.Emptiness, ['tiles/empty.png']],
                     }
tile_map = [
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', '  ', '  ', '  ', 'w2', 'w2', 'w2', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'w2', 'w2', 'w2', 'w2',
     'w2', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'w2', 'w2', 'w2', 'w1', 'w1', 'w1', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'w2', 'w2', 'w2', '  ', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', '  ', '  ', 'w1', 'w1', 'w1', 'w1',
     'w1', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'w1', 'w1', 'w1', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'w1', 'w1', 'w1', '  ', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', '  ', '  ', 'fl', 'fl', 'fl', 'fl',
     'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'fl', 'fl', 'fl', 'w2', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'w2', 'w2', 'fl', '  ', '  ', '  ',
     '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'fl', 'fl', 'fl', 'w1', 'fl', '  ', '  ', '  ', '  ', 'fl', 'w1', 'w1', 'fl', '  ', '  ', '  ',
     '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'w2', 'w2', 'w2', '  ', 'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'w1', 'w1', 'w1', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', '  ', 'fl', 'w2', 'w2', 'w2', 'w2', 'w2', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', 'fl', 'w1', 'w1', 'w1', 'w1', 'w1', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'w2', 'w2', 'w2', '  ', '  ', '  ', '  ', 'fl', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'w2',
     'w2', 'w2', 'w2', 'w2', 'w2', 'w2', '  ', '  ', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'fl', 'w2', 'w2', 'w2', 'w2',
     'w2', 'w2', 'w2', 'w2', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'w1', 'w1', 'w1', '  ', '  ', '  ', '  ', 'fl', '  ', 'fl', '  ', '  ', '  ', '  ', 'fl', 'w1',
     'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w2', 'w2', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'fl', 'w1', 'w1', 'w1', 'w1',
     'w1', 'w1', 'w1', 'w1', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'fl', 'fl', 'fl', 'w2', 'w2', 'w2', 'w2', 'fl', 'w2', 'fl', '  ', '  ', '  ', '  ', 'fl', 'fl',
     'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'w1', 'w1', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl',
     'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'fl', 'fl', 'fl', 'w1', 'w1', 'w1', 'w1', 'fl', 'w1', 'fl', '  ', '  ', '  ', '  ', 'fl', '  ',
     '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ',
     '  ', '  ', '  ', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ', 'fl', '  ',
     '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', 'w2', 'w2', 'fl', 'w2',
     '  ', '  ', '  ', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'w2', 'w2', 'w2', 'w2', 'fl', '  ',
     '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'w1', 'w1', 'fl', 'w1',
     '  ', '  ', '  ', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'w1', 'w1', 'w1', 'w1', 'fl', '  ',
     '  ', '  ', '  ', '  ', 'fl', 'w2', 'w2', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl',
     '  ', '  ', '  ', 'fl', 'w2', '  ', '  ', ],
    ['  ', '  ', 'w2', 'fl', 'w2', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ',
     '  ', '  ', '  ', '  ', 'fl', 'w1', 'w1', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'w2', '  ', 'fl',
     '  ', '  ', '  ', 'fl', 'w1', '  ', '  ', ],
    ['  ', '  ', 'w1', 'fl', 'w1', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'w1', '  ', 'fl',
     'w2', 'w2', 'w2', 'fl', 'fl', '  ', '  ', ],
    ['  ', '  ', 'fl', 'fl', 'fl', 'w2', 'w2', 'w2', 'w2', '  ', '  ', '  ', 'fl', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2',
     'w2', 'w2', '  ', '  ', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', '  ', 'fl',
     'w1', 'w1', 'w1', 'fl', 'fl', '  ', '  ', ],
    ['  ', '  ', 'fl', 'fl', 'fl', 'w1', 'w1', 'w1', 'w1', '  ', '  ', '  ', 'fl', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1',
     'w1', 'w1', '  ', '  ', '  ', 'fl', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', 'fl',
     'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', ],
    ['  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl',
     'fl', 'fl', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'w2', 'w2', 'fl', '  ', '  ',
     '  ', '  ', '  ', 'fl', 'fl', '  ', '  ', ],
    ['  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ',
     '  ', 'fl', '  ', '  ', 'w2', 'w2', 'fl', 'w2', 'w2', '  ', '  ', '  ', 'w2', 'w2', 'w1', 'w1', 'fl', '  ', '  ',
     '  ', '  ', '  ', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', 'fl', '  ', 'w2', 'w2', 'w2', 'w2', 'fl', '  ', '  ', '  ', '  ', '  ', 'fl', '  ', '  ', '  ', '  ',
     '  ', 'fl', '  ', '  ', 'w1', 'w1', 'fl', 'w1', 'w1', '  ', '  ', '  ', 'w1', 'w1', 'fl', 'fl', 'fl', '  ', '  ',
     '  ', '  ', '  ', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', 'fl', '  ', 'w1', 'w1', 'w1', 'w1', 'fl', '  ', '  ', '  ', 'w2', 'w2', 'fl', 'w2', 'w2', '  ', '  ',
     '  ', 'fl', 'w2', 'w2', 'fl', 'fl', 'fl', 'fl', 'fl', 'w2', 'w2', 'w2', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', 'fl', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ', 'w1', 'w1', 'fl', 'w1', 'w1', '  ', '  ',
     '  ', 'fl', 'w1', 'w1', 'fl', 'fl', 'fl', 'fl', 'fl', 'w1', 'w1', 'w1', 'fl', 'fl', 'fl', 'w2', 'w2', 'w2', 'w2',
     'w2', 'w2', 'w2', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', 'fl', '  ', 'fl', '  ', '  ', '  ', 'fl', 'w2', 'w2', 'w2', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ',
     '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'w1', 'w1', 'w1', 'w1',
     'w1', 'w1', 'w1', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', 'fl', 'w2', 'fl', '  ', '  ', '  ', 'fl', 'w1', 'w1', 'w1', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl',
     'fl', 'fl', 'fl', 'fl', '  ', '  ', '  ', ],
    ['  ', '  ', 'fl', 'w1', 'fl', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'w2', 'w2', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl', 'fl', 'fl', 'w2', 'w2',
     'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'w2', 'fl', 'w1', 'w1', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', 'fl', 'fl', 'fl', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'w1', 'w1',
     'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'w1', 'fl', 'fl', 'fl', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'fl', 'fl', 'fl',
     'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', 'fl', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
]
items_on_ground_links = {
    'bd': [obj.SaveBed, [(r'player\bed\bed_empty.png', -1)]],
    '  ': None
}
items_map = [
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', 'bd', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ',
     '  ', '  ', '  ', '  ', '  ', '  ', '  ', ],
]

music_theme = 'Nightmargin (Casey Gu), ft Eliza Velasquez and Michael Shirt - OneShot Soundtrack - 22 On Little Cat Feet.wav'


def init():
    pass