import random

class Minesweeper:
    def __init__(self, size=9, mines=10):
        self.size = size  # Размер поля (9x9)
        self.mines = mines  # Количество мин
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        self.flags = [[False for _ in range(size)] for _ in range(size)]
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

if __name__ == "__main__":
    game = Minesweeper(size=9, mines=10)
    game.print_board(reveal=True)  # показываем поле с минами и числами