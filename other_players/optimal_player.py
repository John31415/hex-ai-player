from player import Player
from board import HexBoard
from board_analyzer import BoardAnalyzer
from xor_hashing import XorHashing
from checker import Checker

from player import RandomPlayer

class OptimalPlayer(Player):

    def __init__(self, player_id):
        super().__init__(player_id)

    def occupy(self, i, player):
        (x, y) = self.cells[i]
        self.board[x][y] = player
        a = self.checker.pair_to_int(self.cells[i])
        self.unions.append(0)
        for neighbor in self.board_analyzer.get_neighbors(self.cells[i]):
            (xn, yn) = neighbor
            b = self.checker.pair_to_int(neighbor)
            if self.board[x][y] == self.board[xn][yn]:
                self.checker.union(a, b, player)
                self.unions[-1] += 1
        self.cells[self.occupied_cells_length], self.cells[i] = self.cells[i], self.cells[self.occupied_cells_length]
        self.occupied_cells_length += 1
        self.matrix_hash ^= self.xor_hashing.cell_hash(x, y, player)

    def vacate(self, i, player):
        self.occupied_cells_length -= 1
        self.cells[self.occupied_cells_length], self.cells[i] = self.cells[i], self.cells[self.occupied_cells_length]
        (x, y) = self.cells[i]
        self.matrix_hash ^= self.xor_hashing.cell_hash(x, y, player)
        self.board[x][y] = 0
        for _ in range(self.unions.pop()):
            self.checker.rollback(player)

    def dfs(self, state, player):
        checked = self.checker.check()
        if checked:
            self.win.append(checked == 3 - player)
        else:
            self.win.append(True)
            for i in range(self.occupied_cells_length, len(self.cells)):
                self.occupy(i, player)
                child_node = self.total_states
                if self.matrix_hash in self.transposition_table:
                    child_node = self.transposition_table[self.matrix_hash]
                else:
                    self.total_states += 1
                    self.state_to_cell[child_node] = self.cells[self.occupied_cells_length - 1]
                    self.dfs(child_node, 3 - player)
                self.win[state] &= not self.win[child_node]
                if (not state) & self.win[child_node]:
                    self.child_root = self.state_to_cell[child_node]
                self.vacate(i, player)
        self.transposition_table[self.matrix_hash] = state

    def play(self, board: HexBoard) -> tuple:
        self.board = board.board
        self.board_analyzer = BoardAnalyzer(board)
        self.cells = self.board_analyzer.get_empty_cells()
        self.occupied_cells_length = 0
        self.xor_hashing = XorHashing(board.size)
        self.matrix_hash = self.xor_hashing.matrix_hash(board.board)
        self.transposition_table = {}
        self.state_to_cell = {0: (-1, -1)}
        self.win = []
        self.total_states = 1
        self.checker = Checker(board.size)
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y]:
                    a = self.checker.pair_to_int((x, y))
                    for neighbor in self.board_analyzer.get_neighbors((x,y)):
                        (xn, yn) = neighbor
                        b = self.checker.pair_to_int(neighbor)
                        if self.board[x][y] == self.board[xn][yn]:
                            self.checker.union(a, b, self.board[x][y])
        self.unions = []
        self.child_root = (None, None)
        self.dfs(0, self.player_id)
        return self.child_root
        