import time
import keyboard
import os
from random import randint

WIDTH = 3
HEIGHT = 10
PLAYER_START_POS = (2, HEIGHT - 1)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = '█'  # символ для клетки

    def __str__(self):
        return self.image


class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.image = 'P'

    def __str__(self) -> str:
        return self.image


class Obstacle:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.image = '#'

    def __str__(self) -> str:
        return self.image


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = {(x, y): Cell(x, y) for x in range(1, width + 1) for y in range(1, height + 1)}
        self.last_update_time = time.time()
        self.player = Player(PLAYER_START_POS[0], PLAYER_START_POS[1])
        self.obstacles = dict()
        self.game = 1

    def get_cell(self, x, y):
        return self.cells[(x, y)]

    def handle_keys(self, event):
        # Обработка нажатых клавиш
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        if time.time() - delta_time > 0.5:
            if keyboard.is_pressed('esc'):
                self.game = 0
            if keyboard.is_pressed('left'):
                self.player.x -= 1
            if keyboard.is_pressed('right'):
                self.player.x += 1
            if keyboard.is_pressed('up'):
                self.player.y -= 1
            if keyboard.is_pressed('down'):
                self.player.y += 1

    def update(self):
        # Обновление состояния игры
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        if self.player.x <= 0 or self.player.x >= 4:
            self.game = 0
        if time.time() - delta_time > float(randint(2, 4)):
            x = (randint(1, 3))
            y = 1
            self.obstacles[(x, y)] = Obstacle(x, y)
        for obstacle in self.obstacles:
            obstacle.y -= 1  # !!!!!!!!!!!!!!!!!!!!!!

    def render(self):
        # Отрисовка игры
        output = ''
        for y in range(1, self.height + 1):
            output += '║'
            for x in range(1, self.width + 1):
                if (x, y) == (self.player.x, self.player.y):
                    output += self.player.image
                elif (x, y) in self.obstacles:
                    print(self.obstacles(x, y))
                else:
                    cell = self.get_cell(x, y)
                    output += cell.image
            output += '║ \n'
        print('\033[H', end='')  # Перемещаем курсор в начало экрана
        print(output, end='')

    def run(self):
        os.system('cls')
        while self.game:
            current_time = time.time()
            delta_time = current_time - self.last_update_time

            self.handle_keys(keyboard.read_event())

            if delta_time >= 0.1:  # Ограничение на частоту обновления экрана
                self.update()
                self.render()
                self.last_update_time = current_time


if __name__ == "__main__":
    field = Field(WIDTH, HEIGHT)
    field.run()
