from player import Player
from board import HexBoard
from board_analyzer import BoardAnalyzer
from electrical_heuristic import ElectricalHeuristic
import time

class ElectricalPlayer(Player):

    def __init__(self, player_id):
        super().__init__(player_id)

    def play(self, board: HexBoard) -> tuple:
        self.BOARD_SIZE = board.size
        self.board_analyzer = BoardAnalyzer(board.board)
        start_time = time.time()
        board_analyzer = BoardAnalyzer(board.board)
        empty_cells = board_analyzer.get_empty_cells()
        electrical_heuristic_me = ElectricalHeuristic(board.board, self.player_id, 2.5)
        R_me = electrical_heuristic_me.resistance()
        electrical_heuristic_opponent = ElectricalHeuristic(board.board, 3 - self.player_id, 2.5)
        R_opponent = electrical_heuristic_opponent.resistance()
        alpha = R_me / (R_me + R_opponent)
        empty_cells = electrical_heuristic_me.get_empty_cells()
        best_score = -1e18
        best_move = None
        for i in range(len(empty_cells)):
            # I_me = electrical_heuristic_me.cell_current(i)
            # I_opponent = electrical_heuristic_opponent.cell_current(i)
            I_me = electrical_heuristic_me.x[i]
            I_opponent = electrical_heuristic_opponent.x[i]
            score = alpha * I_me + (1 - alpha) * I_opponent
            if score > best_score:
                best_score = score
                best_move = empty_cells[i]
        return best_move