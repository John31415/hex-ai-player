from board_analyzer import BoardAnalyzer
import random

def random_sampling(board, player_id) -> bool:
    board_analyzer = BoardAnalyzer(board)
    empty_cells = board_analyzer.get_empty_cells()
    new_board = [row.copy() for row in board]
    check_board = BoardAnalyzer(new_board)
    if check_board.check_connection(player_id):
        return True
    if check_board.check_connection(3 - player_id):
        return False
    player_turn = player_id
    while True:
        cell = random.choice(empty_cells)
        empty_cells.remove(cell)
        (i, j) = cell
        new_board[i][j] = player_turn
        player_turn = 3 - player_turn
        check_board = BoardAnalyzer(new_board)
        if check_board.check_connection(player_id):
            return True
        if check_board.check_connection(3 - player_id):
            return False