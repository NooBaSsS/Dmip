from setup import *
from random import choice, randint


class GameObject:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.x = y
        self.image = ' '
    

class Player(GameObject):
    def __init__(self, speed=0) -> None:
        super().__init__()
        self.x = FRAME_WIDTH // 2
        self.y = FRAME_HEIGHT - 3
        self.max_speed = 10
        self.direcrion = 3
        self.speed = speed
        self.image = 'P'
        self.current_frame = 5
        self.is_alive = True


class BlackHole(GameObject):
    def __init__(self, x, y, frame, force=5) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.current_frame = frame
        self.force = force  # Сила притяжения
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
        '''distance_squared = (self.x - player_x)**2 + (self.y - player_y)**2
        return distance_squared <= self.force**2'''

        '''x_diff = x - self.x
        y_diff = y - self.y
        distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)
        return distance <= self.force
        '''


class WhiteHole(GameObject):
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

    def is_within_force_radius(self, player_x, player_y)-> None:
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
        '''distance_squared = (self.x - player_x)**2 + (self.y - player_y)**2
        return distance_squared <= self.force**2'''

        '''x_diff = x - self.x
        y_diff = y - self.y
        distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)
        return distance <= self.force
        '''


class Field:
    def __init__(self, cols=FRAME_WIDTH, rows=FRAME_HEIGHT, frames=9) -> None:
        self.cols = cols
        self.rows = rows
        self.player = Player()
        self.field = []
        self.frames = frames
        self.holes = self.make_holes(HOLES)
        self.holes_coordinates = {}
        self.last_key = None
        self.pressed_keys = []
        self.warning = 0
        self.show_welcome_screen = 1

    def make_field(self) -> None:
        for frame in range(self.frames):
            frame = []
            for row in range(self.rows):
                row = []
                for col in range(self.cols):
                    row.append([])
                frame.append(row)
            self.field.append(frame)

    def show_rules(self) -> None:
        os.system('cls')
        print('\033[H', end='')
        print(RULES)

    def render(self) -> None:
        current_frame = self.player.current_frame
        output = f'┏{'━' * FRAME_WIDTH}┓ \n'
        for row in range(1, self.rows + 1):
            output += '┃'
            for col in range(1, self.cols + 1):
                if (col, row) == (self.player.x, self.player.y):
                    output += DIRECTION_ARROWS[DIRECTIONS[abs(self.player.direcrion) - 1]]
                    pass
                else:
                    for hole in self.holes:
                        if (col, row) == (hole.x, hole.y) and current_frame == hole.current_frame:
                            output += hole.image
                            break
                    else: output += ' '
            output += '┃\n'
        output += f'┗{'━' * FRAME_WIDTH}┛'
        print('\033[H', end='')  # Перемещаем курсор в начало экрана
        print(output, '\n', self.show_map(), end='')
        #print('\n', self.show_map())
        print('\033[H', end='')
        #print(f'spd: {self.player.speed} cur_frm: {self.player.current_frame}') # !DEBUG!
        if self.warning:
            print('Мне явно не туда')

    def make_holes(self, num) -> list:
        holes = []
        for i in range(num):
            holes.append(
                choice(
                    (
                        BlackHole(randint(0, FRAME_WIDTH), randint(0, FRAME_HEIGHT), randint(8, 15)),
                        WhiteHole(randint(0, FRAME_WIDTH), randint(0, FRAME_HEIGHT), randint(8, 15))
                    )
                )
            )
        return holes


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

    def on_press(self, event) -> None:
        global arrow_states
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
            if not i % 3 and i != 0: output += '\n '
        return output

    def move(self):
        try:
            if time.time() - move_start_time > 1 / self.player.speed:
                move_start_time = time.time()
                self.move_player()
            time.sleep(0.005) # оно как-то помогло
        except:
            зфыы

    def main_game_cycle(self) -> None:
        global arrow_states
        os.system('cls')
        #self.render()
        field.make_field()
        move_start_time = time.time()
        hole_start_time = time.time()
        if self.show_welcome_screen: self.show_rules()
        keyboard.hook(self.on_press)
        while self.player.is_alive:
            self.render()
            self.change_frame()
            try:
                if time.time() - move_start_time > 1 / self.player.speed:
                    move_start_time = time.time()
                    self.move_player()
                time.sleep(0.005) # оно как-то помогло
            except:
                continue
            if time.time() - hole_start_time >= 0.99:
                hole_start_time = time.time()
                for hole in self.holes:
                    if hole.is_within_force_radius(self.player.x, self.player.y) and hole.current_frame == self.player.current_frame:
                        hole.affect_player(self.player)
                        break


if __name__ == '__main__':
    field = Field()
    field.main_game_cycle()
    
keyboard.unhook(field.on_press)