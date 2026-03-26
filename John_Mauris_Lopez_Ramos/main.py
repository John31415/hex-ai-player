from board import HexBoard
from player import RandomPlayer
from solution import SmartPlayer

def draw(board_obj):
    size = board_obj.size
    for r in range(size):
        print(" " * r, end="")
        for c in range(size):
            v = board_obj.board[r][c]
            print(". " if v == 0 else ("1 " if v == 1 else "2 "), end="")
        print()

def game_loop():
    size = 5 # Puedes probar con 11 que es el estándar
    board = HexBoard(size)
    p1 = RandomPlayer(1)
    p2 = SmartPlayer(2) # Tu IA
    
    current = p1
    while True:
        draw(board)
        print(f"Turno del Jugador {current.player_id}")
        
        move = current.play(board)
        if move is None or not board.place_piece(*move, current.player_id):
            print(f"Jugador {current.player_id} hizo un movimiento inválido o el tablero está lleno.")
            break
            
        if board.check_connection(current.player_id):
            draw(board)
            print(f"¡Victoria para el Jugador {current.player_id}!")
            break
            
        current = p2 if current == p1 else p1

if __name__ == "__main__":
    game_loop()