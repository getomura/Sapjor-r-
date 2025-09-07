import random
import json

class Minesweeper:
    def __init__(self, size=9, mines=10):
        self.size = size  # Размер поля (9x9)
        self.mines = mines  # Количество мин
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        self.flags = [[False for _ in range(size)] for _ in range(size)]
        self.game_over = False
        self.initialize_board()

    def initialize_board(self):
        # Размещение мин случайным образом
        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.board[x][y] != 'M':
                self.board[x][y] = 'M'
                mines_placed += 1
        # Заполнение чисел
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != 'M':
                    self.board[x][y] = self.count_mines(x, y)

    def count_mines(self, x, y):
        count = 0
        for i in range(max(0, x - 1), min(self.size, x + 2)):
            for j in range(max(0, y - 1), min(self.size, y + 2)):
                if self.board[i][j] == 'M':
                    count += 1
        return str(count)

    def print_board(self, reveal=False):
        # Вывод игрового поля
        print("   " + " ".join([str(i) for i in range(self.size)]))
        print("  +" + "--" * self.size + "+")
        for idx, row in enumerate(self.board):
            display_row = []
            for jdx, cell in enumerate(row):
                if reveal:
                    display_row.append(cell)
                elif self.revealed[idx][jdx]:
                    display_row.append(cell)
                elif self.flags[idx][jdx]:
                    display_row.append('F')
                else:
                    display_row.append('.')
            print(f"{idx} |" + " ".join(display_row) + "|")
        print("  +" + "--" * self.size + "+")

    def reveal_cell(self, x, y):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            print("Некорректные координаты!")
            return
        if self.revealed[x][y]:
            print("Клетка уже открыта.")
            return
        if self.flags[x][y]:
            print("Клетка помечена флажком. Снимите флажок перед открытием.")
            return

        self.revealed[x][y] = True
        if self.board[x][y] == 'M':
            self.game_over = True
            print("Вы наткнулись на мину! Игра окончена.")
            self.print_board(reveal=True)
            return
        if self.board[x][y] == '0':
            # Рекурсивное открытие соседних клеток
            for i in range(max(0, x - 1), min(self.size, x + 2)):
                for j in range(max(0, y - 1), min(self.size, y + 2)):
                    if not self.revealed[i][j]:
                        self.reveal_cell(i, j)

    def toggle_flag(self, x, y):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            print("Некорректные координаты!")
            return
        if self.revealed[x][y]:
            print("Клетка уже открыта, флажок нельзя поставить.")
            return
        self.flags[x][y] = not self.flags[x][y]
        print(f"Флажок {'установлен' if self.flags[x][y] else 'снят'} на клетке ({x}, {y}).")

    def check_win(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != 'M' and not self.revealed[x][y]:
                    return False
        return True

    def save_game(self, filename="savegame.json"):
        game_state = {
            'size': self.size,
            'mines': self.mines,
            'board': self.board,
            'revealed': self.revealed,
            'flags': self.flags,
            'game_over': self.game_over
        }
        with open(filename, 'w') as f:
            json.dump(game_state, f)
        print(f"Игра сохранена в файл {filename}.")

    def load_game(self, filename="savegame.json"):
        try:
            with open(filename, 'r') as f:
                game_state = json.load(f)
                self.size = game_state['size']
                self.mines = game_state['mines']
                self.board = game_state['board']
                self.revealed = game_state['revealed']
                self.flags = game_state['flags']
                self.game_over = game_state['game_over']
            print(f"Игра загружена из файла {filename}.")
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")

    def play(self):
        while not self.game_over:
            self.print_board()
            try:
                user_input = input("Введите команду ('r x y' для открытия, 'f x y' для флажка, 's' для сохранения, 'q' для выхода): ")
                if user_input.lower() == 'q':
                    print("Игра завершена пользователем.")
                    break
                if user_input.lower() == 's':
                    self.save_game()
                    continue
                command, x, y = user_input.strip().split()
                x, y = int(x), int(y)
                if command.lower() == 'r':
                    self.reveal_cell(x, y)
                elif command.lower() == 'f':
                    self.toggle_flag(x, y)
                else:
                    print("Неизвестная команда. Используйте 'r', 'f' или 's'.")

                if self.check_win():
                    print("Поздравляем! Вы выиграли!")
                    self.print_board(reveal=True)
                    break
            except ValueError:
                print("Неверный ввод. Пожалуйста, следуйте формату команды.")

if __name__ == "__main__":
    size = 9
    mines = 10
    game = Minesweeper(size, mines)

    load_choice = input("Загрузить сохранённую игру? (y/n): ").lower()
    if load_choice == 'y':
        game.load_game()

    game.play()