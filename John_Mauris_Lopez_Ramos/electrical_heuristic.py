from player import Player 
from board import HexBoard
from theorem_prover import TheoremProver
from board_analyzer import BoardAnalyzer
import numpy as np

class ElectricalHeuristic():

    def __init__(self, board, player_id, time_limit):
        self.board = board
        self.BOARD_SIZE = len(board)
        self.player_id = player_id
        self.time_limit = time_limit
        self.N = self.BOARD_SIZE * self.BOARD_SIZE + 2

    def cell_to_id(self, cell):
        (x, y) = cell
        return x * self.BOARD_SIZE + y
    
    def get_border(self, border_id): 
        border = []
        if self.player_id == 1:
            j = 0 if border_id == 0 else self.BOARD_SIZE - 1
            border = [(i, j) for i in range(0, self.BOARD_SIZE)]
        else:
            i = 0 if border_id == 0 else self.BOARD_SIZE - 1
            border = [(i, j) for j in range(0, self.BOARD_SIZE)]
        return border

    def build_G(self):
        self.G = [[0 for _ in range(self.N)] for _ in range(self.N)]
        for (x, y) in self.edges:
            self.G[x][y] = self.G[y][x] = 1000
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == 3 - self.player_id:
                    continue
                a = self.cell_to_id((i, j))
                for (x, y) in self.board_analyzer.get_neighbors((i, j)):
                    if self.board[x][y] == 3 - self.player_id:
                        continue
                    b = self.cell_to_id((x, y))
                    self.G[a][b] = self.G[b][a] = 10000 if (self.board[i][j] & self.board[x][y]) else 1
        def assign(a, b, board):
            self.G[a][b] = self.G[b][a] = 10000 if board else 1
        for (i, j) in self.get_border(0):
            if self.board[i][j] != 3 - self.player_id:
                assign(self.N - 2, self.cell_to_id((i, j)), self.board[i][j])
        for (i, j) in self.get_border(1):
            if self.board[i][j] != 3 - self.player_id:
                assign(self.N - 1, self.cell_to_id((i, j)), self.board[i][j])

    def dfs(self, node_cell):
        self.visit[node_cell] = True
        for i in self.board_analyzer.get_neighbors(node_cell):
            if i not in self.visit:
                self.dfs(i)

    def build_A(self):
        self.visit = {}
        for (i, j) in self.get_border(0):
            if self.board[i][j] != 3 - self.player_id:
                self.dfs((i, j))
        cells = []
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if (i, j) in self.visit:
                    cells.append((i, j))                    
        all_north_border = set(self.get_border(0))
        self.north_border = []
        for i in range(len(cells)):
            if cells[i] in all_north_border:
                self.north_border.append(i)
        self.A = [[0 for _ in range(len(cells))] for _ in range(len(cells))]
        for i_ in range(len(cells)):
            for j_ in range(len(cells)):
                i = self.cell_to_id(cells[i_])
                j = self.cell_to_id(cells[j_])
                if i == j:
                    self.A[i_][j_] = sum(self.G[i])
                else:
                    self.A[i_][j_] = -self.G[i][j]
        self.b = []
        for (i, j) in cells:
            self.b.append(self.G[self.cell_to_id((i, j))][self.N - 2])

    def solver(self):
        A = np.asarray(self.A, np.float64)
        b = np.asarray(self.b, np.float64).reshape(-1)
        try:
            self.x = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            print("Matrix A is probably broken")
            self.x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

    def resistance(self):
        theorem_prover = TheoremProver(self.board, self.player_id)
        self.edges = theorem_prover.main(self.time_limit)
        self.board_analyzer = BoardAnalyzer(self.board)
        self.build_G()
        self.build_A()
        self.solver()
        self.I = 0
        for i in self.north_border:
            self.I += self.G[self.N - 2][i] * (1 - self.x[i])
        self.R =  1e18 if self.I == 0 else 1 / self.I
        return self.R