import numpy as np
import random
from connect4.policy import Policy

class GameLogic:
    ROWS = 6
    COLS = 7
    EMPTY = 0
    
    def _init_(self, board_np, player_turn):
        self.board = board_np.copy()
        self.player_turn = player_turn

    def get_valid_moves(self):
        return [c for c in range(self.COLS) if self.board[0, c] == self.EMPTY]

    def make_move(self, col):
        if self.board[0, col] != self.EMPTY: return False
        for r in range(self.ROWS - 1, -1, -1):
            if self.board[r, col] == self.EMPTY:
                self.board[r, col] = self.player_turn
                self.player_turn *= -1 
                return True
        return False

    def check_win(self, player_id):
        # Implementación iterativa lenta (naive loop)
        # Esto es lo que John optimizará después
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.board[r][c] == player_id:
                    # Check horizontal, vertical, diagonal... (Lento)
                    pass 
        return False

    def is_terminal(self):
        return self.check_win(1) or self.check_win(-1) or len(self.get_valid_moves()) == 0

    def clone(self):
        return GameLogic(self.board, self.player_turn)

class Node:
    def _init_(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_valid_moves()

    def ucb1(self, c_param=1.414):
        if self.visits == 0: return float('inf')
        return (self.wins / self.visits) + c_param * np.sqrt(np.log(self.parent.visits) / self.visits)

    def select_child(self):
        return max(self.children, key=lambda c: c.ucb1())

    def expand(self):
        if not self.untried_moves: return None
        move = self.untried_moves.pop(0)
        new_state = self.state.clone()
        new_state.make_move(move)
        child = Node(new_state, parent=self, move=move)
        self.children.append(child)
        return child

class MCTSAgent(Policy):
    def _init_(self):
        self.simulations = 100 # Bucle fijo (El problema de Diego)

    def act(self, state):
        root = Node(GameLogic(state, 1))
        # Bucle fijo susceptible a timeouts
        for _ in range(self.simulations):
            node = root
            # Selection, Expansion, Simulation, Backprop...
            pass
        return random.choice(root.untried_moves if root.untried_moves else [0])
