import numpy as np
import time
import pygame

world_x_limit = 128
world_y_limit = 128
world_size = (world_x_limit, world_y_limit)
# world_space = np.zeros(world_size)
world_space = np.random.binomial(1, 0.1, size=(world_x_limit, world_y_limit))
new_world_space = np.zeros(world_size)
vectors = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]

# initialise pygame instance
pygame.init()
pygame.display.set_caption('automata')
# set game canvas
world_screen = pygame.display.set_mode((world_x_limit, world_y_limit))


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
            if world_space[x_vector, y_vector] == 1:
                # increment volume of adjacent active cells
                adjacent_active_cells += 1
    return adjacent_active_cells


def report_cell_outcome(x, y):

    adjacent_cells = report_adjacent_cells(x, y)

    cell_outcome = world_space[x, y]

    # Each dead cell adjacent to
    # exactly three live neighbors
    # will become live in the next generation
    if adjacent_cells == 3 and world_space[x, y] == 0:
        cell_outcome = 1
    else:
        if world_space[x, y] == 1:
            # Each live cell with one or
            # fewer live neighbors will die
            # in the next generation
            if adjacent_cells < 1:
                cell_outcome = 0
            else:
                # Each live cell with either two or
                # three live neighbors will remain
                # alive for the next generation.
                if adjacent_cells < 4:
                    cell_outcome = 1
                else:
                    # Each live cell with four or more
                    # live neighbors will die in the
                    # next generation
                    cell_outcome = 0
    return cell_outcome


def main():

    running = True

    while running:

        for x, y in np.ndindex(world_space.shape):
            cell_outcome = report_cell_outcome(x, y)
            if cell_outcome == 1:
                world_screen.set_at((x, y), (255, 255, 255))
            else:
               world_screen.set_at((x, y), (0, 0, 0))
                
            new_world_space[x, y] = cell_outcome

        world_space[:] = new_world_space

        # render screen
        pygame.display.flip()

        time.sleep(0.1)


main()
