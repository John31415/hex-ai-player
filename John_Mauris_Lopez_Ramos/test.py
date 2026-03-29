from mcts import MCTS
from electrical_heuristic import ElectricalHeuristic
from board_analyzer import BoardAnalyzer
from other_players.electrical_player import ElectricalPlayer
from board import HexBoard

board = [0 for _ in range(10)]
player = [0 for _ in range(10)]

# 1
player[0] = 1
board[0] = [[0,0,0,0,0],
           [0,0,0,0,0],
            [0,0,0,0,0],
             [0,0,0,0,0],
              [0,0,0,0,0] ]

# 2
player[1] = 2
board[1] = [[0,1,2,1,1],
           [0,0,2,0,0],
            [1,0,0,0,1],
             [0,2,0,0,0],
              [2,0,0,0,0] ]

# 1
player[2] = 1
board[2] = [[1,1,1,1,0],
           [0,0,0,0,2],
            [0,0,0,0,2],
             [0,0,0,0,2],
              [0,0,0,0,2] ]

# 2
player[3] = 2
board[3] = [[0,1,1,0,1],
           [1,0,1,0,0],
            [0,0,0,0,0],
             [0,0,0,0,0],
              [2,2,2,2,0] ]

# 2
player[4] = 2
board[4] = [[1,1,2,1,1],
           [2,1,2,0,0],
            [2,1,1,1,0],
             [0,2,0,0,0],
              [2,2,0,0,0] ]

# 2
player[5] = 2
board[5] = [[0,1,0,1,1],
           [0,2,1,2,0],
            [1,2,1,1,2],
             [2,1,0,1,0],
              [2,2,1,2,2] ]

# 1
player[6] = 1
board[6] = [[0,1,0,1,1],
           [0,2,1,2,0],
            [1,2,1,1,2],
             [2,1,0,1,0],
              [2,2,0,2,2] ]

# 2
player[7] = 2
board[7] = [[0,1,0,1,1],
           [0,2,1,2,0],
            [1,0,1,1,2],
             [2,1,0,1,0],
              [2,2,0,2,2] ]

# 1
player[8] = 1
board[8] = [[0,1,0,0,1],
           [0,2,1,2,0],
            [1,0,1,1,2],
             [2,1,0,1,0],
              [2,2,0,2,2] ]

# 2
player[9] = 2
board[9] = [[0,1,0,0,1],
           [0,2,1,0,0],
            [1,0,1,1,2],
             [2,1,0,1,0],
              [2,2,0,2,2] ]

# mcts = MCTS(board2, 1)
# move = mcts.mcts()
# print(move)

def tester(current_board, current_player):
    electrical_player = ElectricalPlayer(current_player)
    hex_board = HexBoard(len(current_board))
    for i in range(len(current_board)):
        for j in range(len(current_board)):
            if current_board[i][j] != 0:
                hex_board.place_piece(i, j, current_board[i][j])
    (i, j) = electrical_player.play(hex_board)
    print("Player ", current_player)
    BoardAnalyzer(current_board).draw(current_board)
    print()
    current_board[i][j] = current_player
    BoardAnalyzer(current_board).draw(current_board)

for i in range(10):
    tester(board[i], player[i])
    print("\n\n")

# simulation_time_limit = 5
# empty_cells = BoardAnalyzer(board).get_empty_cells()
# simulation_time_limit /= (len(empty_cells) + 1)
# oponents_heuristic = ElectricalHeuristic(board, 3 - current_player, simulation_time_limit)
# oponents_resistance = oponents_heuristic.resistance()
# my_resistance = 1e18
# for (i, j) in empty_cells:
#     board[i][j] = current_player
#     my_heuristic = ElectricalHeuristic(board, current_player, simulation_time_limit)
#     my_resistance = min(my_resistance, my_heuristic.resistance())
#     board[i][j] = 0

# print("player ", current_player, ": ", my_resistance)
# print("player ", 3 - current_player, ": ", oponents_resistance)