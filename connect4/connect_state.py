import numpy as np

class ConnectState:
    ROWS = 6
    COLS = 7
    
    def __init__(self, board=None, player=1):
        if board is None:
            self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        else:
            self.board = board.copy()
        self.player = player

    def get_valid_moves(self):
        return [c for c in range(self.COLS) if self.board[0, c] == 0]

    def transition(self, action: int):
        """Retorna un NUEVO estado después de jugar en 'action'"""
        if action not in self.get_valid_moves():
            raise ValueError(f"Columna {action} llena o inválida")
        
        new_board = self.board.copy()
        # Buscar fila disponible
        for r in range(self.ROWS - 1, -1, -1):
            if new_board[r, action] == 0:
                new_board[r, action] = self.player
                break
        
        return ConnectState(new_board, -self.player)

    def is_final(self):
        return self.get_winner() != 0 or len(self.get_valid_moves()) == 0

    def get_winner(self):
        # 1 si gana Jugador 1, -1 si gana Jugador 2, 0 si nadie ha ganado aún
        # Horizontal
        for r in range(self.ROWS):
            for c in range(self.COLS - 3):
                if self.board[r, c] != 0 and \
                   self.board[r, c] == self.board[r, c+1] == self.board[r, c+2] == self.board[r, c+3]:
                    return self.board[r, c]
        # Vertical
        for r in range(self.ROWS - 3):
            for c in range(self.COLS):
                if self.board[r, c] != 0 and \
                   self.board[r, c] == self.board[r+1, c] == self.board[r+2, c] == self.board[r+3, c]:
                    return self.board[r, c]
        # Diagonal /
        for r in range(3, self.ROWS):
            for c in range(self.COLS - 3):
                if self.board[r, c] != 0 and \
                   self.board[r, c] == self.board[r-1, c+1] == self.board[r-2, c+2] == self.board[r-3, c+3]:
                    return self.board[r, c]
        # Diagonal \
        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                if self.board[r, c] != 0 and \
                   self.board[r, c] == self.board[r+1, c+1] == self.board[r+2, c+2] == self.board[r+3, c+3]:
                    return self.board[r, c]
        return 0