import os
from random import randint
import keyboard
import time
from random import randint

RULES = ''

PLAYER_MAX_SPEED = 5
FRAME_WIDTH = 40
FRAME_HEIGHT = 20
HOLES = 15
PLAYER_START_X = FRAME_WIDTH - int(FRAME_WIDTH * 0.3)
PLAYER_START_Y = FRAME_HEIGHT - int(FRAME_HEIGHT * 0.3)
PLAYER_START_FRAME = 9
arrow_states = {'left': False, 'right': False, 'up': False, 'down': False}

DIRECTION_ARROWS = {
    'Left': '←',
    'Up': '↑',
    'Right': '→',
    'Down': '↓',
    'UpperLeft': '↖',
    'UpperRight': '↗',
    'LowerRight': '↘',
    'LowerLeft': '↙',
}
DIRECTIONS = [
    'Left',
    'UpperLeft',
    'Up',
    'UpperRight',
    'Right',
    'LowerRight',
    'Down',
    'LowerLeft',
]