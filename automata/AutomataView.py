import numpy as np
import pygame
import pygame.surfarray as surfarray

# The view displays the automata on the screen. It does not alter the automata model; it just
# reads the data from the model and decides what to display based upon the state of the
# model.


class AutomataView:

    # The __init__ method is a special method called a constructor. It takes three parameters
    # with which to view the automata model. Scale applies a display scaling factor to the dimensions.
    # Xaxis and yaxis are integers representing the dimensions of the automata model.The first parameter
    # 'self' is required by Python and refers to the object being created.
    def __init__(self, xaxis, yaxis, scale):

        self.xaxis = xaxis
        self.yaxis = yaxis
        self.scale = scale

    # method to draw on display canvas
    def draw(self, surface, model):

        # draw rectangles to display canvas
        for x, y in np.ndindex(model.world.shape):
            rect_x = x * self.scale
            rect_xa = rect_x - (self.scale - 1)
            rect_y = y * self.scale
            rect_ya = rect_y - (self.scale - 1)
            rect_shape = [rect_xa, rect_ya, rect_x, rect_y]
            if model.world[x, y] > 0:
                pygame.draw.rect(surface, (21, 128, 0), rect_shape)
            else:
                pygame.draw.rect(surface, (0, 0, 0), rect_shape)

        # apply post processing to display canvas
        rgbarray = surfarray.array3d(surface)
        factor = np.array((8,), np.int32)
        soften = np.array(rgbarray, np.int32)
        soften[1:, :] += rgbarray[:-1, :] * factor
        soften[:-1, :] += rgbarray[1:, :] * factor
        soften[:, 1:] += rgbarray[:, :-1] * factor
        soften[:, :-1] += rgbarray[:, 1:] * factor
        soften //= 16
        screen = pygame.display.set_mode(soften.
                                         shape[:2], 0, 32)
        surfarray.blit_array(screen, soften)
