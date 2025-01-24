import shutil, os

class MainMenu():
    def __init__(self):
        self.selected = 0
        self.skipped = 0

    def show(self):
        while True:
            width, height = shutil.get_terminal_size()
            output = f'┏{'━' * (width - 2)}┓ \n'
            for a in range(height - 3):
                output += '┃'
                for i in range((width - 0)):
                    output += ' '
                output += '┃\n'
            output += f'┗{'━' * (width - 2)}┛'
            print('\033[H', end='')
            print(output)


menu = MainMenu()
menu.show()