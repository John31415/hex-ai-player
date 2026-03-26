class DSU:

    def __init__(self, N):
        self.N = N
        self.dad = [range(self.N)]
        self.group = []
        self.color = []

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

    def coordinate_compression(self):
        groups = 0
        for i in range(self.N):
            if i == self.find(i):
                self.group[i] = groups
                groups += 1
            else:
                self.group[i] = self.group[self.find(i)]
        self.color = [0 for _ in range(groups)]

    def set_color(self, i, player):
        self.color[self.group[i]] = player