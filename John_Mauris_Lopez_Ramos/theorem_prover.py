from board import HexBoard
from dsu import DSU
from board_analyzer import BoardAnalyzer
from intbitset import intbitset
from collections import defaultdict
from collections import deque
import time

class TheoremProver():

    BOARD_SIZE = 0

    def __init__(self, board, player):
        self.board = board
        self.BOARD_SIZE = len(self.board)
        self.player = player
        self.dsu = DSU(self.BOARD_SIZE * self.BOARD_SIZE)
        self.board_analyzer = BoardAnalyzer(board)
        self.sc_endpoint = [set() for _ in range(self.BOARD_SIZE * self.BOARD_SIZE)]
        self.sc_carriers = [[set() for _ in range(self.BOARD_SIZE * self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE * self.BOARD_SIZE)]
        self.vc_endpoint = [set() for _ in range(self.BOARD_SIZE * self.BOARD_SIZE)]
        self.vc_carriers = [[set() for _ in range(self.BOARD_SIZE * self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE * self.BOARD_SIZE)]
        self.vc_deque = deque()

    def cell_to_id(self, cell):
        (x, y) = cell
        return x * self.BOARD_SIZE + y
    
    def create_components(self):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] != self.player:
                    continue
                a = self.cell_to_id((i, j))
                for (x, y) in self.board_analyzer.get_neighbors((i, j)):
                    if self.board[x][y] != self.player:
                        continue
                    b = self.cell_to_id((x, y))
                    self.dsu.union(a, b)
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == self.player:
                    self.dsu.set_color(self.cell_to_id((i, j)), self.player)

    def add_vc(self, x, y, carrier: intbitset):
        if x == y:
            return
        if x > y:
            x, y = y, x
        if carrier in self.vc_carriers[x][y]:
            return
        to_pop = [c for c in self.vc_carriers[x][y] if carrier <= c]
        for i in to_pop:
            self.vc_carriers[x][y].discard(i)
            self.vc_carriers[y][x].discard(i)
        self.vc_deque.append((x, y, carrier))

    def add_sc(self, x, y, carrier: intbitset):
        if x == y:
            return
        if x > y:
            x, y= y, x
        if len(self.vc_carriers[x][y]):
            self.sc_carriers[x][y].clear()
            return
        if carrier in self.sc_carriers[x][y]:
            return
        to_pop = [c for c in self.sc_carriers[x][y] if carrier <= c]
        for i in to_pop:
            self.sc_carriers[x][y].discard(i)
        self.sc_carriers[x][y].add(carrier)
        self.sc_carriers[y][x].add(carrier)
        self.sc_endpoint[x].add(y)
        self.sc_endpoint[y].add(x)

    def base_knowledge(self):
        for empty_cell in self.board_analyzer.get_empty_cells():
            x = self.cell_to_id(empty_cell)
            neighbors = self.board_analyzer.get_neighbors(empty_cell)
            for i in range(len(neighbors)):
                y = self.dsu.find(i)
                self.add_vc(x, y, intbitset([]))

    def AND(self, x, A, B, y):
        if (x in B) or (y in A) or (A & B):
            return 
        self.add_vc(x, y, A | B)

    def OR(self, x, A, u, B, y):
        if (x in B) or (y in A) or (A & B):
            return 
        C = A | B
        if u != None:
            C |= intbitset([u])
        for C_ in self.sc_carriers[x][y]:
            if not (C & C_):
                self.sc_carriers[x][y].clear()
                self.add_vc(x, y, C | C_)
                return
        self.add_sc(x, y, C)

    def infer_new_rules(self, x, y, carrier):
        if self.dsu.color[x]:
            for q in self.vc_endpoint[x]:
                # VC - color - VC
                for s in self.vc_carriers[x][q]:
                    self.AND(y, carrier, s, q)
            for q in self.sc_endpoint[x]:
                # VC - color - SC
                for s in self.sc_carriers[x][q]:
                    self.OR(y, carrier, None, s, q)
        else:
            for q in self.vc_endpoint[x]:
                # VC - empty - VC
                for s in self.vc_carriers[x][q]:
                    self.OR(y, carrier, x, s, q)

    def main(self, time_limit):
        start_time = time.time()
        self.create_components()
        self.base_knowledge()
        eps = 0.1
        while time.time() - start_time < time_limit - eps:
            if len(self.vc_deque) == 0:
                break
            (x, y, carrier) = self.vc_deque.popleft()
            self.infer_new_rules(x, y, carrier)
            self.infer_new_rules(y, x, carrier)
            self.vc_carriers[x][y].add(carrier)
            self.vc_carriers[y][x].add(carrier)
            self.vc_endpoint[x].add(y)
            self.vc_endpoint[y].add(x)
        edges = []
        for i in range(len(self.vc_carriers)):
            for j in range(i+1, len(self.vc_carriers)):
                edges.append((i, j))
        return edges