import pygame
import global_variables as gb
import utility_functions as uf


count = 0


def check():
    # if its just walking and etc
    if gb.mode == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gb.running = False
            if event.type == pygame.MOUSEMOTION:
                gb.mousepos = event.pos
            if event.type == gb.every_half_a_second:
                gb.all_sprites.update('animation')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    gb.ctrl_is_down = True
                if event.key == gb.inventory:
                    gb.mode = 2
                if event.key == gb.action:
                    uf.pick_up_event()
                if event.key == gb.debug_key:
                    gb.debug = not gb.debug

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    gb.ctrl_is_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # if the left button is pressed
                if event.button == 1:
                    pass
                # if the right button is pressed
                elif event.button == 3:
                    pass
        keys = pygame.key.get_pressed()
        if keys:
            if keys[gb.left]:
                gb.velocity_x = -1
                gb.velocity_y = 0
            elif keys[gb.right]:
                gb.velocity_x = 1
                gb.velocity_y = 0
            elif keys[gb.up]:
                gb.velocity_x = 0
                gb.velocity_y = -1
            elif keys[gb.down]:
                gb.velocity_x = 0
                gb.velocity_y = 1
            else:
                gb.velocity_x = 0
                gb.velocity_y = 0
            gb.count += 1
            if gb.count == 7:
                gb.count = 0
                # print(gb.velocity_x, gb.velocity_x_actual, gb.velocity_y, gb.velocity_y_actual, gb.gl_comm)
                if gb.velocity_x_actual == 6 or gb.velocity_x_actual == -6:
                    gb.velocity_x_actual = 0
                if gb.velocity_x == 1 or gb.velocity_x_actual > 0:
                    gb.velocity_x_actual += 1
                    gb.velocity_y_actual = 0
                elif gb.velocity_x == -1 or gb.velocity_x_actual < 0:
                    gb.velocity_x_actual -= 1
                    gb.velocity_y_actual = 0

                if gb.velocity_y_actual == 6 or gb.velocity_y_actual == -6:
                    gb.velocity_y_actual = 0
                if gb.velocity_y == 1 or gb.velocity_y_actual > 0:
                    gb.velocity_y_actual += 1
                    gb.velocity_x_actual = 0
                elif gb.velocity_y == -1 or gb.velocity_y_actual < 0:
                    gb.velocity_y_actual -= 1
                    gb.velocity_x_actual = 0
    # if its msg
    if gb.mode == 1:
        for event in pygame.event.get():
            gb.velocity_x = 0
            gb.velocity_y = 0
            gb.velocity_x_actual = 0
            gb.velocity_y_actual = 0

            if event.type == pygame.QUIT:
                gb.running = False
            if event.type == pygame.MOUSEMOTION:
                gb.mousepos = event.pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    gb.ctrl_is_down = True
                if event.key == gb.inventory:
                    gb.mode = 0
                if event.key == gb.action:
                    gb.msg_query.remove(gb.msg_query[0])
                    if len(gb.msg_query) == 0:
                        gb.mode = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    gb.ctrl_is_down = False
    if gb.mode == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gb.running = False
            if event.type == pygame.MOUSEMOTION:
                gb.mousepos = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    gb.ctrl_is_down = True
                if event.key == gb.inventory:
                    gb.mode = 0
                if event.key == gb.action:
                    pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    gb.ctrl_is_down = False
