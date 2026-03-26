import random

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id # Tu identificador (1 o 2)

    def play(self, board) -> tuple:
        raise NotImplementedError("¡Implementa este método!")

class RandomPlayer(Player):
    def play(self, board) -> tuple:
        """Simplemente elige una casilla vacía al azar."""
        empty_cells = [(r, c) for r in range(board.size) 
                       for c in range(board.size) if board.board[r][c] == 0]
        return random.choice(empty_cells) if empty_cells else None