import pygame
from pygame.locals import *
import argparse
import sys
from AutomataModel import AutomataModel
from AutomataView import AutomataView
from AutomataController import AutomataController


# initialise PyGame instance
pygame.init()
# initialise clock
fpsClock = pygame.time.Clock()


# parse external arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(description='A cellular automata application')
    parser.add_argument('-r',
                        '--rules',
                        help='automata rule string',
                        required=True,
                        default='game_of_life.json')
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
    return results.rules, results.seed, results.xaxis, results.yaxis, results.scale


def main():

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        controller.update(fpsClock.get_time() / 1000.0, model)

        surface.fill((0, 0, 0))
        view.draw(surface, model)
        pygame.display.update()
        fpsClock.tick(30)


if __name__ == "__main__":

    # ingest external arguments
    rules, seed, xaxis, yaxis, scale = check_arg(sys.argv[1:])
    # inject internal arguments
    speed = 0.1
    # initialise display canvas
    surface = pygame.display.set_mode((xaxis * scale, yaxis * scale))
    # set display caption
    pygame.display.set_caption('automata')

    model = AutomataModel(seed, rules, xaxis, yaxis, speed)
    view = AutomataView(xaxis, yaxis, scale)
    controller = AutomataController()

    main()
