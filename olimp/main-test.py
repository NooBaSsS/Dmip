import random
import os
import time
import keyboard
import datetime
from tabulate import tabulate

WIDTH = 3
HEIGHT = 20

player_pos = [WIDTH // 2, HEIGHT - 2]  # позиция игрока

# Правила игры
rules = '''
Правила:
вы играете за "P"
вам нужно проехать как можно дальше избегая препятствия "#"
при соприкосновении с препятствием или попытке выезда за поле игра заканчивается
нажмите ENTER чтобы начать
'''
table = [[rules]]
output = tabulate(table, tablefmt='grid')

obstacles = []  # Список для хранения позиций препятствий

score = 0  # Счет игрока

arrow_states = {'left': False, 'right': False}  # Состояние клавиш-стрелок


def draw():
    """
    Функция для отрисовки игрового поля.
    """
    os.system('cls')
    for y in range(HEIGHT):  # Перебор каждой строки и столбца для отрисовки игрового поля
        row = ''
        for x in range(WIDTH):
            if [x, y] == player_pos:
                row += 'P'  # Отрисовка игрока
            elif [x, y] in obstacles:
                row += '#'  # Отрисовка препятствий
            else:
                row += '█'  # Отрисовка пустого пространства
        print('║', row, '║')


def update():
    """
    Функция для обновления состояния игры.
    """
    global score

    # Перемещение препятствий вниз
    for obstacle in obstacles:
        obstacle[1] += 1

    # Удаление препятствий, достигших нижней границы
    obstacles[:] = [obstacle for obstacle in obstacles if obstacle[1] < HEIGHT]

    # Добавление новых препятствий случайным образом
    if random.random() < 0.15:
        obstacles.append([random.randint(0, WIDTH - 1), 0])

    # Проверка на столкновение с препятствиями
    if player_pos in obstacles:
        return False

    # Проверка на столкновение с границами
    if player_pos[0] >= WIDTH or player_pos[0] < 0:
        return False

    # Обновление счета при достижении препятствием нижней границы
    for obstacle in obstacles:
        if obstacle[1] == HEIGHT - 1:
            score += 1

    return True


def bordered(text):
    """
    Функция для добавления рамки к тексту.
    """
    lines = text.splitlines()  # Разделение текста на строки
    width = max(len(s) for s in lines)  # Нахождение максимальной длины строки
    res = ['┌' + '─' * width + '┐']  # Добавление верхней границы
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')  # Добавление текста с левой и правой границами
    res.append('└' + '─' * width + '┘')  # Добавление нижней границы
    return '\n'.join(res)


def read_keyboard():
    """
    Функция для считывания ввода с клавиатуры и обновления позиции игрока.
    """
    global player_pos
    if arrow_states['left']:
        player_pos[0] -= 1  # Перемещение игрока влево
    if arrow_states['right']:
        player_pos[0] += 1  # Перемещение игрока вправо


def handle_key_event(event):
    global arrow_states
    if event.event_type == keyboard.KEY_DOWN:
        if event.name in arrow_states:
            arrow_states[event.name] = True
    elif event.event_type == keyboard.KEY_UP:
        if event.name in arrow_states:
            arrow_states[event.name] = False


def save_score(score):
    # Открываем файл для записи с использованием относительного или абсолютного пути
    with open('scores.txt', 'a') as file:
        global score_path
        score_path = os.path.abspath(file.name)
        # Записываем счет в файл
        file.write(f'Score: {score} \n')


print(output)
input()
keyboard.hook(handle_key_event)

while True:
    draw()
    read_keyboard()

    if not update():  # Обновление состояния игры и проверка на завершение игры
        time.sleep(1)
        os.system('cls')
        save_score(score)  # Сохранение результатов в файл
        print(bordered(f'Игра окончена. \n Счет: {score} \n Файл с результатом сохранен в {score_path}'))  # Отображение сообщения об окончании игры с счетом
        time.sleep(5)
        break
    time.sleep(0.1)  # Задержка для контроля скорости игры

class BlackHole(GameObject):
    def init(self, x=0, y=0, force=1) -> None:
        super().init(x, y)
        self.force = force  # Сила притяжения
        self.image = 'B'    # Обозначение на карте

    def affect_player(self, player):
        # Притягивание игрока к черной дыре
        if player.x > self.x:
            player.x -= self.force
        elif player.x < self.x:
            player.x += self.force

        if player.y > self.y:
            player.y -= self.force
        elif player.y < self.y:
            player.y += self.force


class WhiteHole(GameObject):
    def init(self, x=0, y=0, force=1) -> None:
        super().init(x, y)
        self.force = force  # Сила отталкивания
        self.image = 'W'    # Обозначение на карте

    def affect_player(self, player):
        # Отталкивание игрока от белой дыры
        if player.x > self.x:
            player.x += self.force
        elif player.x < self.x:
            player.x -= self.force

        if player.y > self.y:
            player.y += self.force
        elif player.y < self.y:
            player.y -= self.force