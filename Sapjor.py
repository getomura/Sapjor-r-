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

        # Заполняем числа вокруг мин
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != 'M':
                    count = self.count_mines(x, y)
                    self.board[x][y] = str(count) if count > 0 else ' '

    def count_mines(self, x, y):
        """Подсчёт мин вокруг клетки (x, y)"""
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.board[nx][ny] == 'M':
                        count += 1
        return count

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
        print(f"Флажков осталось: {self.mines - self.count_flags()}")

    def reveal_cell(self, x, y):
        """Открытие клетки и рекурсивное открытие пустых соседей"""
        if not (0 <= x < self.size and 0 <= y < self.size):
            return  # Выход за границы
        if self.revealed[x][y] or self.flags[x][y]:
            return  # Уже открыта или помечена флажком

        self.revealed[x][y] = True

        if self.board[x][y] == 'M':
            self.game_over = True
            print("Бум! Вы подорвались на мине! Игра окончена.")
            self.print_board(reveal=True)
            return

        if self.board[x][y] == ' ':
            # Рекурсивно открываем соседние клетки
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        self.reveal_cell(x + dx, y + dy)

        # Проверка победы после каждого хода
        if self.check_win():
            self.game_over = True
            print("🏆 Поздравляем! Вы выиграли!")
            self.print_board(reveal=True)

    def toggle_flag(self, x, y):
        """Установка или снятие флажка"""
        if not (0 <= x < self.size and 0 <= y < self.size):
            return
        if self.revealed[x][y]:
            return  # Нельзя ставить флажок на открытую клетку
        self.flags[x][y] = not self.flags[x][y]

    def count_flags(self):
        """Подсчёт установленных флажков"""
        return sum(sum(1 for cell in row if cell) for row in self.flags)

    def check_win(self):
        """Проверка, выиграл ли игрок"""
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != 'M' and not self.revealed[x][y]:
                    return False
        return True

    # Сохранение игры
    def save_game(self, filename="save.json"):
        state = {
            "size": self.size,
            "mines": self.mines,
            "board": self.board,
            "revealed": self.revealed,
            "flags": self.flags,
            "game_over": self.game_over,
        }
        with open(filename, "w") as f:
            json.dump(state, f)
        print(f"Игра сохранена в {filename}")

    # Загрузка игры
    def load_game(self, filename="save.json"):
        try:
            with open(filename, "r") as f:
                state = json.load(f)
            self.size = state["size"]
            self.mines = state["mines"]
            self.board = state["board"]
            self.revealed = state["revealed"]
            self.flags = state["flags"]
            self.game_over = state["game_over"]
            print(f"Игра загружена из {filename}")
        except FileNotFoundError:
            print("Сохранение не найдено.")


if __name__ == "__main__":
    print("=== САПЁР ===")
    choice = input("Загрузить сохранённую игру? (y/n): ").lower()
    if choice == "y":
        game = Minesweeper()
        game.load_game()
    else:
        game = Minesweeper(size=9, mines=10)

    game.print_board()

    while not game.game_over:
        try:
            action = input("Ход (r x y - открыть, f x y - флаг, s - сохранить, q - выйти): ").split()
            if not action:
                continue
            cmd = action[0]

            if cmd == 'r' and len(action) == 3:
                x, y = int(action[1]), int(action[2])
                game.reveal_cell(x, y)
            elif cmd == 'f' and len(action) == 3:
                x, y = int(action[1]), int(action[2])
                game.toggle_flag(x, y)
            elif cmd == 's':
                game.save_game()
            elif cmd == 'q':
                print("Выход из игры.")
                break
            else:
                print("Неизвестная команда.")

            if not game.game_over:
                game.print_board()

        except ValueError:
            print("Неверный ввод, попробуйте снова.")