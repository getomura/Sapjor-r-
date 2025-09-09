import random

class Minesweeper:
    def __init__(self, size=9, mines=10):
        self.size = size
        self.mines = mines
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

        # Заполнение числами
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != 'M':
                    count = self.count_mines(x, y)
                    self.board[x][y] = str(count) if count > 0 else ' '

    def count_mines(self, x, y):
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
        if self.revealed[x][y]:
            return

        self.revealed[x][y] = True

        if self.board[x][y] == 'M':
            self.game_over = True
            print("Бум! Вы подорвались на мине!")
            self.print_board(reveal=True)
            return

        if self.board[x][y] == ' ':
            # Рекурсивное открытие соседних клеток
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if not self.revealed[nx][ny]:
                            self.reveal_cell(nx, ny)


if __name__ == "__main__":
    game = Minesweeper(size=9, mines=10)
    game.print_board()

    while not game.game_over:
        try:
            x, y = map(int, input("Введите координаты (x y): ").split())
            game.reveal_cell(x, y)
            if not game.game_over:
                game.print_board()
        except ValueError:
            print("Неверный ввод, попробуйте снова.")