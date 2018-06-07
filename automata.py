import numpy as np
import pygame
from pygame.locals import *
import pygame.surfarray as surfarray
import time
import argparse
import sys
import json

# define dimensions of world space
world_x_limit = 96
world_y_limit = 96
# define shape of world space
world_size = (world_x_limit, world_y_limit)
# define ratio of world space size to display size
display_sc_y = 10
display_sc_x = 10
# define shape of display
display_size = (world_x_limit * display_sc_x, world_y_limit * display_sc_y)
# populate world space with inactive elements
world_space = np.zeros(world_size)
new_world_space = np.zeros(world_size)
# define vectors surrounding each element to which rule checks are applied
vectors = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
# initialise pygame instance
pygame.init()
# set display caption
pygame.display.set_caption('automata')
# initialise pygame font
pygame.font.init()
# set game font
gamefont = pygame.font.SysFont('Ariel', 24)
# set display canvas
world_screen = pygame.display.set_mode(display_size)


# parse external arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(description='A cellular automata application')
    parser.add_argument('-s',
                        '--seed',
                        help='seed cells for first generation',
                        required=True,
                        default='r_pentomino.json')
    results = parser.parse_args(args)
    return results.seed


# insert seed array for first generation into world space
def inject_seed(seed_json):
    with open('./data/seeds/' + seed_json, 'r') as f:
        seed_dict = json.load(f)
    seed_array = seed_dict['seed_array']
    seed_name = seed_dict['seed_name']
    c_x = int(round((world_x_limit / 2) - 1))
    c_y = int(round((world_y_limit / 2) - 1))
    world_space[c_x:c_x + 3, c_y: c_y + 3] = seed_array
    return seed_name


# return volume of active cells adjacent to target cell
def report_adjacent_cells(x, y):
    adjacent_active_cells = 0
    # iterate through location of each adjacent cell
    for vector in vectors:
        # plot location of adjacent cell
        x_vector = x - vector[0]
        y_vector = y - vector[1]
        # check adjacent cell is in world space
        if (0 < x_vector <= world_x_limit - 1) and (0 < y_vector <= world_x_limit - 1):
            # check adjacent cell is active
            if world_space[x_vector, y_vector] > 0:
                # increment volume of adjacent active cells
                adjacent_active_cells += 1
    return adjacent_active_cells


def report_cell_outcome(x, y):
    adjacent_cells = report_adjacent_cells(x, y)
    cell_outcome = world_space[x, y]

    if cell_outcome == 1:
        if adjacent_cells < 2 or adjacent_cells > 3:
            cell_outcome = 0
        else:
            cell_outcome = 1
    else:
        if adjacent_cells == 3:
            cell_outcome = 1

    return cell_outcome


def main():
    running = True
    gen_count = 0

    # from seed argument, load seed array into world space
    seed_file = check_arg(sys.argv[1:])
    seed_label = inject_seed(seed_file)

    while running:
        timer_start = time.time()
        
        # capture escape event
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        # populate next generation of elements
        for x, y in np.ndindex(world_space.shape):
            cell_outcome = report_cell_outcome(x, y)
            rect_size_x = display_sc_x - 1
            rect_size_y = display_sc_y - 1
            rect_x = x * display_sc_x
            rect_xa = rect_x - rect_size_x
            rect_y = y * display_sc_y
            rect_ya = rect_y - rect_size_y
            rect_shape = [rect_xa, rect_ya, rect_x, rect_y]
            if cell_outcome > 0:
                pygame.draw.rect(world_screen, (17, 102, 0), rect_shape)
            else:
                pygame.draw.rect(world_screen, (0, 0, 0), rect_shape)

            new_world_space[x, y] = cell_outcome

        # load next generation of elements to world space
        world_space[:] = new_world_space

        # apply post processing
        rgbarray = surfarray.array3d(world_screen)
        factor = np.array((8,), np.int32)
        soften = np.array(rgbarray, np.int32)
        soften[1:, :] += rgbarray[:-1, :] * factor
        soften[:-1, :] += rgbarray[1:, :] * factor
        soften[:, 1:] += rgbarray[:, :-1] * factor
        soften[:, :-1] += rgbarray[:, 1:] * factor
        soften //= 16
        screen = pygame.display.set_mode(soften.shape[:2], 0, 32)
        surfarray.blit_array(screen, soften)

        gen_count += 1
        timer_stop = time.time()
        timer_delta = str(timer_stop - timer_start)
        text_surface = gamefont.render(
            "gen: {x}  cycle: {y}  seed: {z}".format(x=gen_count,
                                                                  y=timer_delta,
                                                                  z=seed_label),
            False, (17, 102, 0))
        world_screen.blit(text_surface, (5, 5))

        # render screen
        pygame.display.flip()


if __name__ == "__main__":
    main()
