class Minesweeper:
    def __init__(self, size=9):
        self.size = size  # Размер поля (9x9)
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        self.flags = [[False for _ in range(size)] for _ in range(size)]

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
    game = Minesweeper(size=9)
    game.print_board()