import random

class XorHashing:

    def __init__(self, size):
        self.size = size
        self.matrix1 = [ [int(random.random() * 2**64) for _ in range(size)] for _ in range(size) ]
        self.matrix2 = [ [int(random.random() * 2**64) for _ in range(size)] for _ in range(size) ]

    def cell_hash(self, row, column, type):
        if type == 0:
            return 0
        if type == 1:
            return self.matrix1[row][column]
        if type == 2:
            return self.matrix2[row][column]
    
    def matrix_hash(self, matrix):
        xor = 0
        for i in range(self.size):
            for j in range(self.size):
                xor ^= self.cell_hash(i, j, matrix[i][j])
        return xor