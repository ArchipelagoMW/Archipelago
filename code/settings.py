import pygame, sys, numpy
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
TILE_SIZE = 64
ANIMATION_SPEED = 6

Z_LAYERS = {
    'bg' : 0,
    'bg tiles' : 2,
    'bg details' : 4,
    'main' : 5,
    'fg' : 7
}