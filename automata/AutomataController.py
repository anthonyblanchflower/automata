import numpy as np
from AutomataModel import AutomataModel

# The automata controller joins the automata model and the automata view together; it uses the
# clock to update the model.


class AutomataController:

    # The controller class does not require a constructor (init  method) because it does not
    # contain any state and therefore does not need to contain any attributes.

    def update(self, delta_time, model):

        model.clock -= delta_time

        if model.clock < 0:
            model.clock += model.speed
            vectors = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
            for x, y in np.ndindex(model.world.shape):
                neighbours = 0
                for vector in vectors:
                    # plot location of neighbour cell
                    x_vector = x - vector[0]
                    y_vector = y - vector[1]
                    # check neighbour cell is in model
                    if (0 < x_vector <= model.xaxis - 1) and (0 < y_vector <= model.yaxis - 1):
                        # check neighbour cell is active
                        if model.world[x_vector, y_vector] > 0:
                            # increment volume of neighbour active cells
                            neighbours += 1
                if model.world[x, y] == 1:
                    if neighbours not in model.survive_list:
                        model.new_world[x, y] = 0
                    else:
                        model.new_world[x, y] = 1
                else:
                    if neighbours in model.birth_list:
                        model.new_world[x, y] = 1

            model.world[:] = model.new_world




