import numpy as np
import time

world_x_limit = 16
world_y_limit = 16
world_size = (world_x_limit, world_y_limit)
world_space = np.zeros(world_size)
new_world_space = np.zeros(world_size)
vectors = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]

# populate seed elements: beacon pattern
def return_seed_elements():
    seed = [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]
    return seed


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

    world_space[4:8, 4:8] = return_seed_elements()

    while running:

        for x, y in np.ndindex(world_space.shape):
            new_world_space[x, y] = report_cell_outcome(x, y)

        world_space[:] = new_world_space

        print(world_space)

        time.sleep(2)


main()
