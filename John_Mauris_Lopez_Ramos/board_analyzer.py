from board import HexBoard

class BoardAnalyzer:

    def __init__(self, board: HexBoard):
        self.board = board.board
        self.board_length = len(self.board)
    
    def get_empty_cells(self):
        return [(i,j) for i in range(self.board_length) for j in range(self.board_length) if self.board[i][j] == 0]
    
    def get_occupied_cells(self):
        return [(i,j) for i in range(self.board_length) for j in range(self.board_length) if self.board[i][j] != 0]
    
    def is_inside(self, cell):
        (i, j) = cell
        return (0 <= i) & (i < self.board_length) & (0 <= j) & (j < self.board_length)
    
    def get_neighbors(self, cell):
        (i, j) = cell
        neighbors = [(i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j)]
        return [neighbor for neighbor in neighbors if self.is_inside(neighbor)]

    def draw(self, board):
        size = len(board)
        for r in range(size):
            print(" " * r, end="")
            for c in range(size):
                v = board[r][c]
                print(". " if v == 0 else ("1 " if v == 1 else "2 "), end="")
            print()