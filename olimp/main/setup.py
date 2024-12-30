import os
from random import randint
import keyboard
import time
from random import randint
import math

RULES = ''

FRAME_WIDTH = 20
FRAME_HEIGHT = 10
DEFAULT_ARROW_STATES = {'left': False, 'right': False, 'up': False, 'down': False}
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