from board import HexBoard
from dsu import DSU
from board_analyzer import BoardAnalyzer
from intbitset import intbitset
from collections import defaultdict
from collections import deque

class TheoremProver():

    BOARD_SIZE = 0

    def __init__(self, board: HexBoard, player):
        self.board = board.board
        self.BOARD_SIZE = board.size
        self.player = player
        self.dsu = DSU(self.BOARD_SIZE * self.BOARD_SIZE)
        self.board_analyzer = BoardAnalyzer(board)
        self.sc = defaultdict(set)
        self.vc = defaultdict(set)
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
        self.dsu.coordinate_compression()
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == self.player:
                    self.dsu.set_color(self.cell_to_id((i, j)), self.player)

    def add_vc(self, x, y, carrier: intbitset):
        if x > y:
            x, y = y, x
        if carrier in self.vc[(x, y)]:
            return
        to_pop = [c for c in self.vc[(x, y)] if carrier <= c]
        for i in to_pop:
            self.vc[(x, y)].discard(i)
        self.vc_deque.append((x, y, carrier))

    def add_sc(self, x, y, carrier: intbitset):
        if x > y:
            x, y= y, x
        if (x, y) in self.vc:
            self.sc.pop((x, y))
            return
        if carrier in self.sc[(x, y)]:
            return
        to_pop = [c for c in self.sc[(x, y)] if carrier <= c]
        for i in to_pop:
            self.sc[(x, y)].discard(i)
        self.sc[(x, y)].add(carrier)

    def base_knowledge(self):
        for empty_cell in self.board_analyzer.get_empty_cells():
            a = self.cell_to_id(empty_cell)
            neighbors_player = [self.cell_to_id((i, j)) for (i, j) in self.board_analyzer.get_neighbors(empty_cell) if self.board[i][j] == self.player]
            for i in range(len(neighbors_player)):
                x = self.dsu.group[neighbors_player[i]]
                self.add_vc(x, a, intbitset([]))

    def AND(self, x, A, u, B, y):
        if self.dsu.color[self.dsu.group[u]] != self.player:
            return 
        if (x in B) or (y in A) or (A & B):
            return 
        self.add_vc(x, y, A | B)

    def OR(self, x, A, u, B, y):
        if self.dsu.color[self.dsu.group[u]]:
            return 
        if (x in B) or (y in A) or (A & B):
            return 
        self.add_sc(x, y, A | B | intbitset([u]))
        if len(self.sc[(x, y)]) == 1:
            return 
        sc_list = list(self.sc[(x, y)])
        for i in range(len(sc_list)):
            for j in range(i+1, len(sc_list)):
                c1 = sc_list[i]
                c2 = sc_list[j]
                if not (c1 & c2):
                    self.sc.pop((x, y))
                    self.add_vc(x, y, c1 | c2)
                    return

    def infer(self, x, y, carrier):
        for ((p, q), s) in self.vc.items():
            
            pass
        pass

    def main(self):
        self.create_components()
        self.base_knowledge()
        pass