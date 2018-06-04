import numpy as np
import pygame
from pygame.locals import *
import pygame.surfarray as surfarray

# define dimensions of world space
world_x_limit = 96
world_y_limit = 96
# define shape of world space
world_size = (world_x_limit, world_y_limit)
# define ratio of world space size to display size
display_sc_y = 8
display_sc_x = 8
# define shape of display
display_size = (world_x_limit * display_sc_x, world_y_limit * display_sc_y)
# populate world space with active element noise at ratio 1
## random seed noise:
## world_space = np.random.binomial(1, 0.05, size=world_size)
## R Pentomino seed:
world_space = np.zeros(world_size)
c_x = int(round((world_x_limit / 2) - 1))
c_y = int(round((world_y_limit / 2) - 1))
new_seed = [[0, 1, 1],  [1, 1, 0],  [0, 1, 0]]
world_space[c_x:c_x + 3, c_y: c_y + 3] = new_seed 
# populate next generation world space with inactive elements
new_world_space = np.zeros(world_size)
# define vectors surrounding each element to which rule checks are applied
vectors = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
# define color gradient of elements
colors = [(38, 230, 0),
          (34, 204, 0),
          (30, 179, 0),
          (26, 153, 0),
          (21, 128, 0),
          (17, 102, 0),
          (13, 77, 0),
          (9, 51, 0),
          (4, 26, 0)]
# initialise pygame instance
pygame.init()
# set display caption
pygame.display.set_caption('automata')
# set display canvas
world_screen = pygame.display.set_mode(display_size)


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

    # each inactive element adjacent to
    # exactly three active neighbors
    # will become active in the next generation
    #if adjacent_cells == 3 and world_space[x, y] == 0:
    #    cell_outcome = 1
    #else:
    #    if world_space[x, y] > 0:
            # each active element with one or
            # fewer active neighbors will become inactive
            # in the next generation
    #        if adjacent_cells < 1:
    #            cell_outcome = 0
    #        else:
                # each active element with either two or
                # three active neighbors will remain
                # active for the next generation and will
                # increase in age
    #            if adjacent_cells < 4:
    #                if cell_outcome < 9:
    #                    cell_outcome += 1
    #            else:
                    # each active element with four or more
                    # active neighbors will become inactive in the
                    # next generation
    #                cell_outcome = 0

    if adjacent_cells == 2:
        if 0 < cell_outcome < 9:
            cell_outcome += 1
    else:
        if adjacent_cells == 3:
            if 0 < cell_outcome < 9:
                cell_outcome += 1
            else:
                if cell_outcome == 0:
                    cell_outcome = 1
        else:
            cell_outcome == 0

    return cell_outcome


def main():
    running = True

    while running:

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
                pygame.draw.rect(world_screen, colors[int(cell_outcome - 1)], rect_shape)
            else:
                pygame.draw.rect(world_screen, (0, 0, 0), rect_shape)

            new_world_space[x, y] = cell_outcome

        # load next generation of elements to world space
        world_space[:] = new_world_space

        # apply post processing
        rgbarray = surfarray.array3d(world_screen)
        factor = np.array((8,), np.int32)
        # soften = np.array(rgbarray)
        soften = np.array(rgbarray, np.int32)
        soften[1:, :] += rgbarray[:-1, :] * factor
        soften[:-1, :] += rgbarray[1:, :] * factor
        soften[:, 1:] += rgbarray[:, :-1] * factor
        soften[:, :-1] += rgbarray[:, 1:] * factor
        # soften //= 33
        screen = pygame.display.set_mode(soften.shape[:2], 0, 32)
        surfarray.blit_array(screen, soften)

        # render screen
        pygame.display.flip()


if __name__ == "__main__":
    main()
