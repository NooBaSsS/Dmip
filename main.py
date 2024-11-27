import os
from random import randint
import keyboard
import time
from random import randint

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

class GameObject:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.x = y
        self.image = ' '

    def __str__(self) -> str:
        return self.image
    

class Player(GameObject):
    def __init__(self, speed=0) -> None:
        super().__init__()
        self.x = FRAME_WIDTH // 2
        self.y = FRAME_HEIGHT // 2
        self.max_speed = 10
        self.direcrion = 3
        self.speed = speed
        self.image = 'P'
        self.current_frame = 5
        self.is_alive = True

    def __str__(self):
        return self.image


class BlackHole(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.current_frame = randint(0, 8)
        self.force = 1


class WhiteHole(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.current_frame = randint(0, 8)
        self.force = 1


class Field:
    def __init__(self, cols=FRAME_WIDTH, rows=FRAME_HEIGHT, frames=9) -> None:
        self.cols = cols
        self.rows = rows
        self.player = Player()
        self.field = []
        self.frames = frames
        self.holes = []
        self.holes_coordinates = []
        self.last_key = None
        self.pressed_keys = []
        self.warning = 0
        self.show_welcome_screen = 1

    def get_holes_coordinates(self):
        # идет по списку дыр и записывает их координаты в список координат дыр как (col, row)
        pass

    def make_field(self):
        for frame in range(self.frames):
            frame = []
            for row in range(self.rows):
                row = []
                for col in range(self.cols):
                    row.append([])
                frame.append(row)
            self.field.append(frame)

    def show_rules(self):
        os.system('cls')
        print('\033[H', end='')
        print(RULES)

    def show_map(self):
        for i in range(self.frames):
            output = ''
            if self.player.current_frame == i: output += 'P'
            else: output += '·'
            if not i % 3: output += '\n'

    def render(self):
        current_frame = self.player.current_frame
        output = f'┏{'━' * FRAME_WIDTH}┓ \n'
        for row in range(1, self.rows + 1):
            output += '┃'
            for col in range(1, self.cols + 1):
                if (col, row) == (self.player.x, self.player.y):
                    output += DIRECTION_ARROWS[DIRECTIONS[abs(self.player.direcrion) - 1]]
                else:
                    output += ' '
            output += '┃\n'
        output += f'┗{'━' * FRAME_WIDTH}┛'
        print('\033[H', end='')  # Перемещаем курсор в начало экрана
        print(output, end='')
        print('\033[H', end='')
        print(f'spd: {self.player.speed} cur_frm: {self.player.current_frame}') # !DEBUG!
        if self.warning:
            print('Мне явно не туда')

    def move_player(self):
        if self.player.direcrion == 1:
            self.player.x -= 1
        elif self.player.direcrion == 2:
            self.player.x -= 1
            self.player.y -= 1
        elif self.player.direcrion == 3:
            self.player.y -= 1
        elif self.player.direcrion == 4:
            self.player.y -= 1
            self.player.x += 1
        elif self.player.direcrion == 5:
            self.player.x += 1
        elif self.player.direcrion == 6:
            self.player.x += 1
            self.player.y += 1
        elif self.player.direcrion == 7:
            self.player.y += 1
        elif self.player.direcrion == 8:
            self.player.x -= 1
            self.player.y += 1

    def change_frame(self):
        if self.player.x == 0: # Перемещение налево
            if (self.player.current_frame - 1) % 3:
                self.warning = 0
                self.player.current_frame -= 1
                self.player.x = FRAME_WIDTH 
            else:
                self.player.x = 1
                self.player.speed = 0
                #self.warning = 1
        elif self.player.x == FRAME_WIDTH + 1: # Перемещение направо
            if self.player.current_frame % 3:
                self.warning = 0
                self.player.current_frame += 1
                self.player.x = 1
            else:
                self.player.x = FRAME_WIDTH
                self.player.speed = 0
                #self.warning = 1
        elif self.player.y == 0: # Перемещение направо
            if self.player.current_frame - 3 > 0:
                self.warning = 0
                self.player.current_frame -= 3
                self.player.y = FRAME_HEIGHT
            else:
                self.player.y = 1
                self.player.speed = 0
                #self.warning = 1
        elif self.player.y == FRAME_HEIGHT + 1: # Перемещение направо
            if self.player.current_frame + 3 <= self.frames:
                self.warning = 0
                self.player.current_frame += 3
                self.player.y = 1
            else:
                self.player.y = FRAME_HEIGHT
                self.player.speed = 0
                #self.warning = 1

    def change_player_direction(self):
        if arrow_states['left']: 
            self.player.direcrion = self.player.direcrion - 1
            if self.player.direcrion - 1 < 0: self.player.direcrion = len(DIRECTIONS)
        elif arrow_states['right']: 
            self.player.direcrion = self.player.direcrion + 1
            if self.player.direcrion > len(DIRECTIONS) - 1: self.player.direcrion = 0
        elif arrow_states['up']:
            self.player.speed += 1
            if self.player.speed > self.player.max_speed:
                self.player.speed = self.player.max_speed
        elif arrow_states['down']:
            self.player.speed -= 1
            if self.player.speed < 0:
                self.player.speed = 0

    def on_press(self, event):
        global arrow_states
        if event.event_type == keyboard.KEY_DOWN:
            if event.name in arrow_states:
                arrow_states[event.name] = True
        elif event.event_type == keyboard.KEY_UP:
            if event.name in arrow_states:
                self.change_player_direction()
                arrow_states[event.name] = False

    def main_game_cycle(self):
        global arrow_states
        os.system('cls')
        #self.render()
        field.make_field()
        start_time = time.time()
        if self.show_welcome_screen: self.show_rules()
        keyboard.hook(self.on_press)
        while self.player.is_alive:
            self.render()
            self.show_map()
            self.change_frame()
            try:
                if time.time() - start_time > 1 / self.player.speed:
                    start_time = time.time()
                    self.move_player()
            except:
                continue



if __name__ == '__main__':
    field = Field()
    field.main_game_cycle()
    
keyboard.unhook(field.on_press)