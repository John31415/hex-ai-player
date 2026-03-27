from board import HexBoard
from collections import deque

class BoardAnalyzer:

    def __init__(self, board):
        self.board = board
        self.board_length = len(self.board)
    
    def get_empty_cells(self):
        return [(i,j) for i in range(self.board_length) for j in range(self.board_length) if self.board[i][j] == 0]
    
    def get_player_cells(self, player):
        return [(i,j) for i in range(self.board_length) for j in range(self.board_length) if self.board[i][j] == player]
    
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

    def check_connection(self, player_id: int) -> bool:
        """
        Verifica si el jugador ha conectado sus dos lados (BFS).
        - Jugador 1 (🔴): conecta col  0 (Izquierda) con col  size-1 (Derecha)
        - Jugador 2 (🔵): conecta fila 0 (Superior)  con fila size-1 (Inferior)
        """
        visited = set()
        queue = deque()

        # Sembrar BFS desde el borde inicial del jugador
        for i in range(self.board_length):
            r, c = (i, 0) if player_id == 1 else (0, i)
            if self.board[r][c] == player_id:
                queue.append((r, c))
                visited.add((r, c))

        while queue:
            curr_r, curr_c = queue.popleft()

            # Condición de victoria: llegó al borde opuesto
            if player_id == 1 and curr_c == self.board_length - 1:
                return True
            if player_id == 2 and curr_r == self.board_length - 1:
                return True

            for nr, nc in self.get_neighbors((curr_r, curr_c)):
                if (nr, nc) not in visited and self.board[nr][nc] == player_id:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return False