import os
import sys

import pygame
import event_handler
import global_variables as gb
import utility_functions as uf
import obj

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.init()
pygame.display.set_icon(uf.load_image('icon.png'))
pygame.display.set_caption('Broken Lightbulb')
# init obj
gb.debug = False  ################################################################### gb.debug

first = True
song_list = []

resp = uf.load()
if resp:
    lvl_name, pos = resp
else:
    uf.load_animation()
    lvl_name, pos = 'start', (0, 0)
gb.playerpos_x, gb.playerpos_y = pos
gb.cur_lvl = uf.load_level(lvl_name)
gb.player, level_x, level_y = uf.generate_level(gb.cur_lvl)

mousePoint, cam = obj.Mouse(), obj.Camera()

gb.every_half_a_second = pygame.USEREVENT + 1
pygame.time.set_timer(gb.every_half_a_second, 500)


while gb.running:
    isinfocus = bool(pygame.mouse.get_focused())

    event_handler.check()

    # rendering
    gb.screen.fill((0, 0, 0))

    gb.all_sprites.update()
    gb.light_group.update()
    gb.all_sprites.draw(gb.screen)

    if gb.darken and not gb.debug:
        uf.darken()
        gb.light_group.draw(gb.screen)

    cam.update(gb.player)
    for sprite in gb.all_sprites:
        cam.apply(sprite)

    gb.mouse.update()
    gb.mouse.draw(gb.screen)
    if gb.mode == 1:
        uf.draw_msg()
    if gb.mode == 2:
        uf.draw_inv()

    if gb.debug:
        uf.debug_hud()

    pygame.display.flip()
    if not pygame.mixer.music.get_busy():
        uf.play_music(gb.current_music_theme)
    gb.clock.tick(60)
pygame.quit()
