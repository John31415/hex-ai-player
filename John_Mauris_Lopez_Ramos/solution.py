from player import Player
from board import HexBoard
from mcts import MCTS

class SmartPlayer(Player):

    # returns a sufficiently good move based on the smart player's criteria
    def play(self, board: HexBoard) -> tuple:
        mcts = MCTS(board.board, self.player_id)
        move = mcts.mcts()
        return move