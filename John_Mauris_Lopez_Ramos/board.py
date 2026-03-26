import copy
from collections import deque

class HexBoard:
    def __init__(self, size: int):
        self.size = size
        # 0 = vacío, 1 = Jugador 1, 2 = Jugador 2
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def clone(self) -> 'HexBoard':
        """Devuelve una copia profunda del tablero actual."""
        new_board = HexBoard(self.size)
        new_board.board = copy.deepcopy(self.board)
        return new_board

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        """Coloca una ficha si la casilla está vacía."""
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col] == 0:
                self.board[row][col] = player_id
                return True
        return False

    def get_neighbors(self, r: int, c: int):
        adj = [(r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c)]
        return [(nr, nc) for nr, nc in adj if 0 <= nr < self.size and 0 <= nc < self.size]

    def check_connection(self, player_id: int) -> bool:
        """
        Verifica si el jugador ha conectado sus dos lados (BFS).
        - Jugador 1 (🔴): conecta col  0 (Izquierda) con col  size-1 (Derecha)
        - Jugador 2 (🔵): conecta fila 0 (Superior)  con fila size-1 (Inferior)
        """
        visited = set()
        queue = deque()

        # Sembrar BFS desde el borde inicial del jugador
        for i in range(self.size):
            r, c = (i, 0) if player_id == 1 else (0, i)
            if self.board[r][c] == player_id:
                queue.append((r, c))
                visited.add((r, c))

        while queue:
            curr_r, curr_c = queue.popleft()

            # Condición de victoria: llegó al borde opuesto
            if player_id == 1 and curr_c == self.size - 1:
                return True
            if player_id == 2 and curr_r == self.size - 1:
                return True

            for nr, nc in self.get_neighbors(curr_r, curr_c):
                if (nr, nc) not in visited and self.board[nr][nc] == player_id:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return False