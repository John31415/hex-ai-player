from mcts import MCTS
from electrical_heuristic import ElectricalHeuristic

board0 = [[0,0,0,0,0],
           [0,0,0,0,0],
            [0,0,0,0,0],
             [0,0,0,0,0],
              [0,0,0,0,0] ]

# 2
board1 = [[0,1,2,1,1],
           [0,0,2,0,0],
            [1,0,0,0,1],
             [0,2,0,0,0],
              [2,0,0,0,0] ]

# 1
board2 = [[1,1,1,1,0],
           [0,0,0,0,2],
            [0,0,0,0,2],
             [0,0,0,0,2],
              [0,0,0,0,2] ]

board3 = [[0,1,1,0,1],
           [1,0,1,0,0],
            [0,0,0,0,0],
             [0,0,0,0,0],
              [2,2,2,2,0] ]

board4 = [[1,1,2,1,1],
           [2,1,2,0,0],
            [2,1,1,1,0],
             [0,2,0,0,0],
              [2,2,0,0,0] ]

# mcts = MCTS(board2, 1)
# move = mcts.mcts()
# print(move)

elec1 = ElectricalHeuristic(board4, 1, 5)
print(elec1.resistance())

elec2 = ElectricalHeuristic(board4, 2, 5)
print(elec2.resistance())