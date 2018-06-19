import numpy as np
import pygame
from pygame.locals import *
import pygame.surfarray as surfarray
import time
import argparse
import sys
import json
import psutil
import os

# define vectors surrounding each element to which rule checks are applied
vectors = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
# initialise pygame instance
pygame.init()
# set display caption
pygame.display.set_caption('automata')
# initialise pygame font
pygame.font.init()
# set game font
gamefont = pygame.font.SysFont('Impact', 20)
#gamefont.set_bold(True)


# parse external arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(description='A cellular automata application')
    parser.add_argument('-s',
                        '--seed',
                        help='seed cells for first generation',
                        required=True,
                        default='r_pentomino.json')
    parser.add_argument('-x',
                        '--xaxis',
                        help='number of cells for world space x axis',
                        type=int,
                        required=True,
                        default='64')
    parser.add_argument('-y',
                        '--yaxis',
                        help='number of cells for world space y axis',
                        type=int,
                        required=True,
                        default='64')
    parser.add_argument('-S',
                        '--scale',
                        help='pixel scale for each cell',
                        type=int,
                        required=True,
                        default='10')
    results = parser.parse_args(args)
    return results.seed, results.xaxis, results.yaxis, results.scale


# insert seed array for first generation into world space
def inject_seed(seed_json):
    dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(dir_path + '/data/seeds/' + seed_json, 'r') as f:
        seed_dict = json.load(f)
    seed_array = seed_dict['seed_array']
    seed_name = seed_dict['seed_name']
    size_x = len(seed_array[0])
    size_y = len(seed_array)
    c_x = int(round((world_x_limit / 2) - 1))
    c_y = int(round((world_y_limit / 2) - 1))
    world_space[c_x:c_x + size_x, c_y: c_y + size_y] = seed_array
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

    while running:
        timer_start = time.time()

        # capture escape event
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        # populate next generation of elements
        for x, y in np.ndindex(world_space.shape):
            cell_outcome = report_cell_outcome(x, y)
            rect_size = display_sc - 1
            rect_x = x * display_sc
            rect_xa = rect_x - rect_size
            rect_y = y * display_sc
            rect_ya = rect_y - rect_size
            rect_shape = [rect_xa, rect_ya, rect_x, rect_y]
            if cell_outcome > 0:
                pygame.draw.rect(world_screen, (21, 128, 0), rect_shape)
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
        timer_delta = str(timer_stop - timer_start)[:5]
        cpu_usage = psutil.cpu_percent()
        text_surface = gamefont.render("seed: {s}".format(s=seed_label), False, (17, 102, 0))
        world_screen.blit(text_surface, (5, 5))
        text_surface = gamefont.render("gen: {g}".format(g=gen_count), False, (17, 102, 0))
        world_screen.blit(text_surface, (5, 20))
        text_surface = gamefont.render("cycle: {c}".format(c=timer_delta), False, (17, 102, 0))
        world_screen.blit(text_surface, (5, 35))
        text_surface = gamefont.render("cpu: {p}%".format(p=cpu_usage), False, (17, 102, 0))
        world_screen.blit(text_surface, (5, 50))
        text_surface = gamefont.render("size: {x}x{y}".format(x=world_x_limit, y=world_y_limit), False, (17, 102, 0))
        world_screen.blit(text_surface, (5, 65))
        text_surface = gamefont.render("scale: {S}".format(S=display_sc), False, (17, 102, 0))
        world_screen.blit(text_surface, (5, 80))

        # render screen
        pygame.display.flip()


if __name__ == "__main__":
    # ingest external arguments
    seed_file, world_x_limit, world_y_limit, display_sc = check_arg(sys.argv[1:])
    # define shape of world space
    world_size = (world_x_limit, world_y_limit)
    # define shape of display
    display_size = (world_x_limit * display_sc, world_y_limit * display_sc)
    # populate world space with inactive elements
    world_space = np.zeros(world_size)
    new_world_space = np.zeros(world_size)
    # set display canvas
    world_screen = pygame.display.set_mode(display_size)
    # from seed argument, load seed array into world space
    seed_label = inject_seed(seed_file)

    main()
