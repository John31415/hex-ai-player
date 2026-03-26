from board import HexBoard

class Checker:

    def __init__(self, board_size):
        self.board_size = board_size
        self.dad1 = [i for i in range(0, self.board_size ** 2)]
        self.dad2 = [i for i in range(0, self.board_size ** 2)]
        self.size1 = [1 for _ in range(0, self.board_size ** 2)]
        self.size2 = [1 for _ in range(0, self.board_size ** 2)]
        self.history1 = []
        self.history2 = []
        self.U = self.board_size ** 2
        self.dad2.append(self.U)
        self.size2.append(1)
        for i in range(0, self.board_size):
            self.union(self.U, i, 2)
        self.R = self.board_size ** 2
        self.dad1.append(self.R)
        self.size1.append(1)
        for i in range(0, self.board_size):
            self.union(self.R, self.board_size * (i + 1) - 1, 1)
        self.D = self.U + 1
        self.dad2.append(self.D)
        self.size2.append(1)
        for i in range(0, self.board_size):
            self.union(self.D, self.board_size ** 2 - i - 1, 2)
        self.L = self.R + 1
        self.dad1.append(self.L)
        self.size1.append(1)
        for i in range(0, self.board_size):
            self.union(self.L, self.board_size * i, 1)

    def pair_to_int(self, pair) -> int:
        return pair[0] * self.board_size + pair[1]
    
    def find(self, x, player):
        dad = self.dad1 if player == 1 else self.dad2
        while dad[x] != x:
            x = dad[x]
        return x
    
    def union(self, a, b, player):
        history = self.history1 if player == 1 else self.history2
        dad = self.dad1 if player == 1 else self.dad2
        size = self.size1 if player == 1 else self.size2
        a = self.find(a, player)
        b = self.find(b, player)
        if a == b:
            history.append(None)
            return
        if size[a] < size[b]:
            a, b = b, a
        history.append((b, dad[b], a, size[a]))
        dad[b] = a
        size[a] += size[b]

    def rollback(self, player):
        history = self.history1 if player == 1 else self.history2
        dad = self.dad1 if player == 1 else self.dad2
        size = self.size1 if player == 1 else self.size2
        if not history:
            return
        if history[-1] == None:
            history.pop()
            return
        (b, dad_b, a, size_a) = history.pop()
        dad[b] = dad_b
        size[a] = size_a

    def check(self):
        if self.find(self.L, 1) == self.find(self.R, 1):
            return 1
        if self.find(self.U, 2) == self.find(self.D, 2):
            return 2
        return 0