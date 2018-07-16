import numpy as np
import json
import os
import sys

# The model holds the state of the robot. It has no methods at all, just data.


class AutomataModel(object):

    # The __init__ method is a special method called a constructor. It takes three parameters
    # for the construction of the automata model. Seed is the name of the file containing the
    # initial automata state as a 2d list array. Rules are expressed in the B/S format. Xaxis
    # and yaxis are integers representing the dimensions of the automata model.The first parameter 'self'
    # is required by Python and refers to the object being created.
    def __init__(self, seed, rules, xaxis, yaxis, speed):

        self.xaxis = xaxis
        self.yaxis = yaxis
        self.clock = speed
        self.speed = speed
        # populate sectors with inactive elements
        self.world = np.zeros((xaxis, yaxis))
        self.new_world = np.zeros((xaxis, yaxis))

        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(dir_path + '/data/seeds/' + seed, 'r') as f:
            seed_dict = json.load(f)

        seed_array = seed_dict['seed_array']
        self.seed_name = seed_dict['seed_name']
        if self.seed_name == 'Low Density Noise':
            self.world[:] = np.random.binomial(1, 0.05, size=(xaxis, yaxis))
        else:
            size_x = len(seed_array[0])
            size_y = len(seed_array)
            c_x = int(round((xaxis / 2) - 1))
            c_y = int(round((yaxis / 2) - 1))
            self.world[c_x:c_x + size_x, c_y: c_y + size_y] = seed_array

        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(dir_path + '/data/rules/' + rules, 'r') as f:
            rules_dict = json.load(f)

        self.birth_list = rules_dict['birth']
        self.survive_list = rules_dict['survival']
