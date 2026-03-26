class DSU:

    def __init__(self, N):
        self.N = N
        self.dad = [i for i in range(self.N)]
        self.color = [0 for _ in range(self.N)]

    def find(self, x):
        if x == self.dad[x]:
            return x
        self.dad[x] = self.find(self.dad[x])
        return self.dad[x]
    
    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a > b:
            a, b = b, a
        self.dad[b] = a

    def set_color(self, i, player):
        self.color[i] = player