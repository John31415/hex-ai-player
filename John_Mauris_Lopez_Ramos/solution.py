from player import Player
from board import HexBoard
from board_analyzer import BoardAnalyzer
from optimal_player import OptimalPlayer
from mcts import MCTS
import time

class SmartPlayer(Player):

    # returns a sufficiently good move based on the smart player's criteria
    def play(self, board: HexBoard) -> tuple:

        start_time = time.time()

        analyzer = BoardAnalyzer(board)
        empty_cells = analyzer.get_empty_cells()

        # returns the optimal move for a small search space
        if len(empty_cells) < 13 :
            optimal_player = OptimalPlayer(self.player_id)
            move = optimal_player.play(board)
            print("optimal move", move)
            print(time.time() - start_time)
            if move != (None, None):
                return move
        
        mcts = MCTS(board, self.player_id)

        move = mcts.mcts()

        print(time.time() - start_time)

        # print("move", move)
        # print(board.board)

        return move