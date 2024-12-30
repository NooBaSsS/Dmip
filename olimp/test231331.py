import math

class Object:
    def __init__(self, x, y, force):
        self.x = x
        self.y = y
        self.force = force

    def is_within_force_radius(self, x, y):
        # Вычисляем расстояние между проверяемой точкой и объектом
        x_diff = x - self.x
        y_diff = y - self.y
        distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)
        return distance <= self.force

# Создаем объект и задаем его координаты и радиус действия
obj = Object(5, 5, 3)  # Координаты x и y, радиус действия 3

while True:
    print(obj.is_within_force_radius(int(input()), int(input())))