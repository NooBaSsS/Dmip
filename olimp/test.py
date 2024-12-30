import random
import math

# Основные константы
GAME_WIDTH = 20
GAME_HEIGHT = 10

# Определяем класс игрового объекта (дыры, обломки, база)
class GameObject:
    def init(self, x, y, type, power=0):
        self.x = x
        self.y = y
        self.type = type  # 'black_hole', 'white_hole', 'debris', 'base'
        self.power = power  # Только для черных и белых дыр

# Класс корабля
class Ship:
    def init(self):
        self.x = 0
        self.y = 0
        self.angle = 0  # Угол ориентации: 0, 45, 90... до 360
        self.speed = 0
        self.is_destroyed = False

    def rotate(self, direction):
        if direction == "left":
            self.angle = (self.angle - 45) % 360
        elif direction == "right":
            self.angle = (self.angle + 45) % 360

    def accelerate(self):
        if self.speed < 3:  # Максимальная скорость
            self.speed += 1

    def move(self):
        if self.speed > 0:
            radians = math.radians(self.angle)
            dx = round(math.cos(radians) * self.speed)
            dy = round(math.sin(radians) * self.speed)
            self.x = (self.x + dx) % GAME_WIDTH
            self.y = (self.y + dy) % GAME_HEIGHT

# Класс игрового поля
class GameField:
    def init(self):
        self.ship = Ship()
        self.objects = [
            GameObject(5, 5, 'black_hole', power=2),
            GameObject(10, 3, 'white_hole', power=2),
            GameObject(15, 7, 'debris'),
            GameObject(18, 9, 'base')
        ]

    def apply_gravity(self):
        for obj in self.objects:
            if obj.type in ['black_hole', 'white_hole']:
                dx = obj.x - self.ship.x
                dy = obj.y - self.ship.y
                distance = math.hypot(dx, dy)
                if distance == 0:
                    continue  # Игнорируем объекты прямо на корабле
                effect = obj.power / distance
                if obj.type == 'black_hole':
                    self.ship.x += round(effect * dx)
                    self.ship.y += round(effect * dy)
                elif obj.type == 'white_hole':
                    self.ship.x -= round(effect * dx)
                    self.ship.y -= round(effect * dy)

    def check_collisions(self):
        for obj in self.objects:
            if self.ship.x == obj.x and self.ship.y == obj.y:
                if obj.type == 'debris':
                    self.ship.is_destroyed = True
                elif obj.type == 'black_hole':
                    self.ship.x, self.ship.y = random.choice(
                        [(o.x, o.y) for o in self.objects if o.type == 'white_hole']
                    )
                elif obj.type == 'white_hole':
                    self.ship.x = (self.ship.x + random.randint(-2, 2)) % GAME_WIDTH
                    self.ship.y = (self.ship.y + random.randint(-2, 2)) % GAME_HEIGHT
                elif obj.type == 'base':
                    print("Миссия выполнена! Корабль достиг базы.")

    def update(self, command):
        if command == "rotate_left":
            self.ship.rotate("left")
        elif command == "rotate_right":
            self.ship.rotate("right")
        elif command == "accelerate":
            self.ship.accelerate()
        self.ship.move()
        self.apply_gravity()
        self.check_collisions()

# Основной игровой цикл
def main():
    field = GameField()
    while not field.ship.is_destroyed:
        command = input("Введите команду (rotate_left, rotate_right, accelerate): ")
        field.update(command)

        # Печатаем состояние корабля
        print(f"Координаты корабля: ({field.ship.x}, {field.ship.y}), угол: {field.ship.angle}, скорость: {field.ship.speed}")
        if any(obj.x == field.ship.x and obj.y == field.ship.y and obj.type == 'base' for obj in field.objects):
            print("Вы достигли базы. Победа!")
            break
        elif field.ship.is_destroyed:
            print("Корабль уничтожен.")
            break


if __name__ == "main":
    main()