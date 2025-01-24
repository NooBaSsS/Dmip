from random import choice, randint, shuffle
import shutil
from setup import *


class GameObject:
    '''
    заготовка для других классов
    '''
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.x = y
        self.image = ' '


class Player(GameObject):
    '''
    класс игрока
    '''
    def __init__(self, speed=0) -> None:
        super().__init__()
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.max_speed = PLAYER_MAX_SPEED
        self.direcrion = 3
        self.speed = speed
        self.image = 'P'
        self.current_frame = PLAYER_START_FRAME
        self.is_alive = True


class BlackHole(GameObject):
    '''
    класс черной дыры
    кроме данных о самой дыре имеет методы для проверки нахождения
    игрока в своем радиусе и воздействия на игрока
    '''
    def __init__(self, x, y, frame, force=5) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.current_frame = frame
        self.force = force  # Радиус притяжения
        self.image = 'B'    # Обозначение на карте

    def affect_player(self, player) -> None:
        # Притягивание игрока к черной дыре
        if player.x > self.x:
            player.x -= 1
        elif player.x < self.x:
            player.x += 1

        if player.y > self.y:
            player.y -= 1
        elif player.y < self.y:
            player.y += 1

    def is_within_force_radius(self, player_x, player_y) -> bool:
        # Вычисляем расстояние между проверяемой точкой и объектом
        x_left = self.x - self.force
        x_right = self.x + self.force
        y_top = self.y - self.force
        y_bottom = self.y + self.force
        coordinates = []
        for y in range(y_top, y_bottom):
            for x in range(x_left, x_right):
                coordinates.append((x, y))

        for coordinate in coordinates:
            if coordinate == (player_x, player_y):
                return True
        return False


class WhiteHole(GameObject):
    '''
    класс белой дыры
    кроме данных о самой дыре имеет методы для проверки нахождения
    игрока в своем радиусе и воздействия на игрока
    '''
    def __init__(self, x, y, frame, force=5) -> None:
        super().__init__()
        self.current_frame = frame
        self.force = force
        self.image = 'W'
        self.x = x
        self.y = y

    def affect_player(self, player) -> None:
        # Притягивание игрока к черной дыре
        if player.x > self.x:
            player.x += 1
        elif player.x < self.x:
            player.x -= 1

        if player.y > self.y:
            player.y += 1
        elif player.y < self.y:
            player.y -= 1

    def is_within_force_radius(self, player_x, player_y) -> bool:
        # Вычисляем расстояние между проверяемой точкой и объектом
        x_left = self.x - self.force
        x_right = self.x + self.force
        y_top = self.y - self.force
        y_bottom = self.y + self.force
        coordinates = []
        for y in range(y_top, y_bottom):
            for x in range(x_left, x_right):
                coordinates.append((x, y))

        for coordinate in coordinates:
            if coordinate == (player_x, player_y):
                return True
        return False


class MatterFragment(GameObject):
    '''
    класс для обломков материи
    '''
    def __init__(self, x, y, frame):
        super().__init__()
        self.x = x
        self.y = y
        self.current_frame = frame
        self.image = '\u2604'


class Field:
    '''
    класс поля
    основной класс
    в нем находится не только поле, но и методы для правильной работы игры, в том числе и основной цикл игры
    '''
    def __init__(self, cols=FRAME_WIDTH, rows=FRAME_HEIGHT, frames=9) -> None:
        self.cols = cols
        self.rows = rows
        self.player = Player()
        self.frames = frames
        self.field = self.make_field()
        self.holes = self.make_holes(HOLES)
        self.black_holes_coordinates, self.white_holes_coordinates = self.get_holes_coordiates()
        self.matter_fragments = self.make_matter_fragments()
        self.show_welcome_screen = 1

    def make_field(self) -> None:
        result = []
        for frame in range(self.frames):
            frame = []
            for row in range(self.rows):
                row = []
                for col in range(self.cols):
                    row.append([])
                frame.append(row)
            result.append(frame)
        return result

    def show_rules(self) -> None:
        os.system('cls')
        print('\033[H', end='')
        print(RULES)

    def render(self) -> None:
        current_frame = self.player.current_frame
        output = f'┏{'━' * FRAME_WIDTH}┓ \n'
        for row in range(1, self.rows + 1):
            output += '┃'
            output += '\033[44m'
            for col in range(1, self.cols + 1):
                if (col, row) == (self.player.x, self.player.y):
                    output += f'\033[31m{DIRECTION_ARROWS[DIRECTIONS[abs(self.player.direcrion) - 1]]}\033[37m'
                else:
                    for hole in self.holes:
                        if (col, row, current_frame) == (hole.x, hole.y, hole.current_frame):
                            if isinstance(hole, BlackHole):
                                output += f'\033[37;40m{hole.force}\033[37;44m'
                                break
                            output += f'\033[30;47m{hole.force}\033[37;44m'
                            break
                        #elif (col, row, current_frame) in self.matter_fragments:
                        #    output += '\u2604'
                    else: output += ' '
            output += '\033[40m'
            output += '┃\n'
        output += f'┗{'━' * FRAME_WIDTH}┛'
        print('\033[H', end='')  # Перемещаем курсор в начало экрана
        print(output, f'\n {self.show_map()}spd: {self.player.speed}\n{self.player.x, self.player.y}', end='')
        print('\033[H ', end='')

    def make_holes(self, num) -> list:
        holes = []
        for frame in range(1, self.frames):
            holes.append(
                choice(
                    (
                        BlackHole(randint(1, FRAME_WIDTH), randint(1, FRAME_HEIGHT), frame, randint(3, 5)),
                        WhiteHole(randint(1, FRAME_WIDTH), randint(1, FRAME_HEIGHT), frame, randint(3, 5)),
                    )
                )
            )

        for i in range(num - self.frames):
            holes.append(
                choice(
                    (
                        BlackHole(randint(1, FRAME_WIDTH), randint(1, FRAME_HEIGHT), randint(1, 9), randint(3, 5)),
                        WhiteHole(randint(1, FRAME_WIDTH), randint(1, FRAME_HEIGHT), randint(1, 9), randint(3, 5)),
                    )
                )
            )
        return holes

    def make_matter_fragments(self): #todo вообще не рабоает, переписать с нуля
        all_fragments = []
        available_coordinates = [] # * список должен быть заполнен координатами по типу [[1, 1, 0], [2, 1, 0]]

        for row_idx, row in enumerate(self.field): # * идет по каждой сторке
            #input(f'{len(row), len(self.field)}')
            for col_idx, col in enumerate(row): # * идет по каждой координате в строке(колонне)
                #input(len(col))
                #input(f'coords: {col_idx + 1, row_idx + 1}')
                pass
        '''
        for frame, row in enumerate(self.field): # делает список со всеми клетками
            matter_on_frame = []
            for col in row:
                if col != PLAYER_START_X and frame != PLAYER_START_FRAME:
                    matter_on_frame += [col, row, frame]
                    input(f'{[row.index(col), self.field.index(row), frame]}')
            available_coordinates += matter_on_frame
        for coordinate in available_coordinates:
            if coordinate in (*self.black_holes_coordinates,
                              *self.white_holes_coordinates,
                              (PLAYER_START_X, PLAYER_START_Y, PLAYER_START_FRAME)):
                available_coordinates.remove(coordinate)
        for frame in available_coordinates:
            #all_fragments.append(shuffle(frame)[:choice(range(FRAME_WIDTH * 2, FRAME_WIDTH * 3)):])
            shuffled_frame = shuffle(frame)
            for i in range(0, choice(range(FRAME_WIDTH * 2, FRAME_WIDTH * 3))):
                input((i, type(i), shuffled_frame, frame))
                all_fragments.append(shuffled_frame[i])
        return all_fragments
    '''

    def get_holes_coordiates(self) -> list:
        bh_coordinates = []
        wh_coordinates = []
        for hole in self.holes:
            if isinstance(hole, BlackHole):
                bh_coordinates.append((hole.x, hole.y, hole.current_frame))
            else:
                wh_coordinates.append((hole.x, hole.y, hole.current_frame))
        return bh_coordinates, wh_coordinates

    def move_player(self) -> None:
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

    def change_frame(self) -> None:
        if self.player.x == 0: # Перемещение налево
            if (self.player.current_frame - 1) % 3:
                self.player.current_frame -= 1
                self.player.x = FRAME_WIDTH
            else:
                self.player.x = 1
                self.player.speed = 0
        elif self.player.x == FRAME_WIDTH + 1: # Перемещение направо
            if self.player.current_frame % 3:
                self.player.current_frame += 1
                self.player.x = 1
            else:
                self.player.x = FRAME_WIDTH
                self.player.speed = 0
        elif self.player.y == 0: # Перемещение направо
            if self.player.current_frame - 3 > 0:
                self.player.current_frame -= 3
                self.player.y = FRAME_HEIGHT
            else:
                self.player.y = 1
                self.player.speed = 0
        elif self.player.y == FRAME_HEIGHT + 1: # Перемещение направо
            if self.player.current_frame + 3 <= self.frames:
                self.player.current_frame += 3
                self.player.y = 1
            else:
                self.player.y = FRAME_HEIGHT
                self.player.speed = 0

    def change_player_direction(self) -> None:
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

    def check_player_collision(self) -> None:
        for hole_coords in self.black_holes_coordinates:
            if (self.player.x, self.player.y, self.player.current_frame) == hole_coords:
                self.player.x, self.player.y, self.player.current_frame = choice(self.white_holes_coordinates)


    def on_press(self, event) -> None:
        if event.event_type == keyboard.KEY_DOWN:
            if event.name in arrow_states:
                arrow_states[event.name] = True
        elif event.event_type == keyboard.KEY_UP:
            if event.name in arrow_states:
                self.change_player_direction()
                arrow_states[event.name] = False

    def show_map(self) -> str:
        output = ''
        for i in range(1, self.frames + 1):
            if self.player.current_frame == i: output += 'P'
            else: output += '.'
            if not i % 3 and i != 0: output += '   \n '
        return output

    def main_game_cycle(self) -> None:
        os.system('cls')
        #self.render()
        move_start_time = time.time()
        hole_start_time = time.time()
        if self.show_welcome_screen: self.show_rules()
        keyboard.hook(self.on_press)
        while self.player.is_alive:
            self.check_player_collision()
            self.render()
            self.change_frame()
            try:
                if time.time() - move_start_time > 1 / self.player.speed:
                    move_start_time = time.time()
                    self.move_player()
                time.sleep(0.005) # оно как-то помогло
            except ZeroDivisionError:
                continue
            if time.time() - hole_start_time >= 0.98:
                hole_start_time = time.time()
                for hole in self.holes:
                    if hole.is_within_force_radius(self.player.x, self.player.y) and hole.current_frame == self.player.current_frame:
                        hole.affect_player(self.player)
                        break


class MainMenu():
    def __init__(self) -> None:
        self.selected = 0
        self.skipped = 0

    def show(self) -> None:
        pass


if __name__ == '__main__':
    field = Field()
    field.main_game_cycle()

keyboard.unhook(field.on_press)