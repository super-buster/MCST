# import the pygame module, so you can use it
import pygame
from pygame.locals import *
import sys


class Config(object):
    HEIGHT = 450
    WIDTH = 450
    WHITECOLOR = pygame.Color(254, 254, 254)
    BLACKCOLOR = pygame.Color(1, 1, 1)
    BLUECOLOR = pygame.Color(25, 25, 200)


conf = Config()
screen = pygame.display.set_mode((conf.HEIGHT, conf.WIDTH))


def puiinit():
    if not pygame.font:
        print('Warning, fonts disabled')
    if not pygame.mixer:
        print('Warning, sound disabled')

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("minimal program")
    pygame.mouse.set_visible(1)
    screen.fill(conf.WHITECOLOR)
    pygame.draw.line(screen, conf.BLUECOLOR, [
        conf.WIDTH/3, 0], [conf.WIDTH/3, conf.HEIGHT], 5)
    pygame.draw.line(screen, conf.BLUECOLOR, [
        2*conf.WIDTH/3, 0], [2*conf.WIDTH/3, conf.HEIGHT], 5)
    pygame.draw.line(screen, conf.BLUECOLOR, [
        0, conf.HEIGHT/3], [conf.WIDTH, conf.HEIGHT/3], 5)
    pygame.draw.line(screen, conf.BLUECOLOR, [
        0, 2*conf.HEIGHT/3], [conf.WIDTH, 2*conf.HEIGHT/3], 5)


def Draw(corx, cory, shape):
    if shape == "o":
        pygame.draw.circle(screen, conf.BLACKCOLOR,
                           [corx*150+75, cory*150+75], 50, 5)
    if shape == "x":
        pygame.draw.line(screen, conf.BLACKCOLOR,  [
                         corx*150+20, cory*150+20], [corx*150+130, cory*150+130], 5)
        pygame.draw.line(screen, conf.BLACKCOLOR,  [
            corx*150+130, cory*150+20], [corx*150+20, cory*150+130], 5)


def main():

    # main loop
    while True:
        pygame.display.update()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                corx, cory = pygame.mouse.get_pos()
                Draw(3*corx//conf.WIDTH, 3*cory//conf.HEIGHT, "x")
