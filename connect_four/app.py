import enum

class GridPosition(enum.Enum):
    EMPTY = 0
    YELLOW = 1
    RED = 2

class Grid:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._grid = None
        self.init_grid()
    
    def init_grid(self):
        self._grid = [[GridPosition.EMPTY for _ in range(self._cols)] for _ in range(self._rows)]
    
    def get_rows(self):
        return self._rows
    
    def get_cols(self):
        return self._cols
    
    def get_position(self, row, col):
        return self._grid[row][col]

    def set_position(self, row, col, color):
        self._grid[row][col] = color

    def check_win(self, row, col, color):
        # Check Horizontal
        count = 0
        for j in range(max(col - 3, 0), min(col + 4, self.get_cols())):
            if self.get_position(row, j) == color:
                count += 1
            else:
                count = 0
            if count == 4:
                return True

        # Check Vertical
        count = 0
        for i in range(max(row - 3, 0), min(row + 4, self.get_rows())):
            if self.get_position(i, col) == color:
                count += 1
            else:
                count = 0
            if count == 4:
                return True
        return False
    
    def reset_grid(self):
        self.init_grid()

    
    

class Game:
    def __init__(self, grid, target_score):
        self._grid = grid
        self._player1 = Player('Player 1', GridPosition.YELLOW)
        self._player2 = Player('Player 2', GridPosition.RED)
        self._scores = {self._player1: 0, self._player2: 0}
        self._target_score = target_score

    def get_target_score(self):
        return self._target_score
    
    def play_round(self):
        curr_player = self._player1
        while True:
            winner = self.play_turn(curr_player)
            if winner:
                break
            curr_player = self._player1 if curr_player == self._player2 else self._player2
        return winner

    
    def play_turn(self, player):
        self.print_grid()
        name = player.get_name()
        color = player.get_color()
        num_cols = self._grid.get_cols()
        num_rows = self._grid.get_rows()
        print(f"It is {name}'s turn. Enter a column between 0 to {num_cols}.")
        col = int(input())
        for i in range(num_rows - 1, -1, -1):
            if self._grid.get_position(i, col) == GridPosition.EMPTY:
                self._grid.set_position(i, col, player.get_color())
                if self._grid.check_win(i, col, color):
                    return player
                break
        return None

    def play(self):
        while self._scores[self._player1] != self._target_score and self._scores[self._player2] != self._target_score:
            if self.play_round() == self._player1:
                self._scores[self._player1] += 1
                print(f"{self._player1.get_name()} wins this round!")
            else:
                self._scores[self._player2] += 1
                print(f"{self._player2.get_name()} wins this round!")
            self._grid.reset_grid()
        if self._scores[self._player1] == self._target_score:
            print(f"{self._player1.get_name()} wins!")
        else:
            print(f"{self._player2.get_name()} wins!")

    def print_grid(self):
        color_map = {GridPosition.EMPTY: "O", GridPosition.YELLOW: "Y", GridPosition.RED: "R"}
        res = "\n"
        for i in range(self._grid.get_rows()):
            for j in range(self._grid.get_cols()):
                res += color_map[self._grid.get_position(i, j)] + " "
            res += "\n"
        print(res)

class Player:
    def __init__(self, name, color):
        self._name = name
        self._color = color
    
    def get_name(self):
        return self._name
    
    def get_color(self):
        return self._color




grid = Grid(10, 10)
game = Game(grid, 2)
game.play()