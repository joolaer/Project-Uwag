import pygame, enums, pygame.freetype
from helpers import Helper_Dialog
from state import State
from os.path import join 
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FRAME_RATE = 60
PLAYER_RUN_SPEED = 10
TILE_SIZE = 32
TEXT_SPEED = 50

helper_dialog = Helper_Dialog()
state = State()