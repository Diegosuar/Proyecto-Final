import numpy as np
import math
import time
import random
from connect4.policy import Policy

class GameLogic:
    """
    Motor lógico optimizado con NumPy.
    """
    ROWS = 6
    COLS = 7
    EMPTY = 0
    
    def __init__(self, board_np, player_turn):
        self.board = board_np.copy()
        self.player_turn = player_turn

    def get_valid_moves(self):
        # Retorna movimientos válidos ordenados por preferencia central
        valid = [c for c in range(self.COLS) if self.board[0, c] == self.EMPTY]
        center_pref = [3, 2, 4, 1, 5, 0, 6]
        valid.sort(key=lambda x: center_pref.index(x) if x in center_pref else 99)
        return valid

    def make_move(self, col):
        if self.board[0, col] != self.EMPTY: return False
        for r in range(self.ROWS - 1, -1, -1):
            if self.board[r, col] == self.EMPTY:
                self.board[r, col] = self.player_turn
                self.player_turn *= -1 
                return True
        return False

    def check_win(self, player_id):
        b = self.board
        # Horizontal
        for r in range(self.ROWS):
            for c in range(self.COLS - 3):
                if np.all(b[r, c:c+4] == player_id): return True
        # Vertical
        for r in range(self.ROWS - 3):
            for c in range(self.COLS):
                if np.all(b[r:r+4, c] == player_id): return True
        # Diagonal /
        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                if np.all(b[r:r+4, c:c+4].diagonal() == player_id): return True
        # Diagonal \
        for r in range(3, self.ROWS): 
            for c in range(self.COLS - 3):
                if np.all(np.fliplr(b[r-3:r+1, c:c+4]).diagonal() == player_id): return True
        return False

    def is_terminal(self):
        return self.check_win(1) or self.check_win(-1) or np.all(self.board[0, :] != 0)

    def clone(self):
        return GameLogic(self.board, self.player_turn)

class Node:
    def __init__(self, state: GameLogic, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_valid_moves()
        self.player_to_move = state.player_turn

    def ucb1(self, c_param=1.5): # C ligeramente agresivo
        if self.visits == 0: return float('inf')
        return (self.wins / self.visits) + c_param * math.sqrt(math.log(self.parent.visits) / self.visits)

    def select_child(self):
        # Desempate favoreciendo centro
        return max(self.children, key=lambda c: (c.ucb1(), -abs(c.move - 3)))

    def expand(self):
        move = self.untried_moves.pop(0) 
        new_state = self.state.clone()
        new_state.make_move(move)
        child = Node(new_state, parent=self, move=move)
        self.children.append(child)
        return child

class MCTSAgent(Policy):
    def __init__(self):
        # Buffer ajustado para permitir el híbrido
        self.time_limit = 0.45 

    def mount(self, *args, **kwargs):
        if args:
            try:
                val = float(args[0])
                if 0 < val < 5.0: self.time_limit = val - 0.05
            except: pass

    def _simulate_hybrid(self, state):
        """
        EL EQUILIBRIO: Smart al principio, Fast al final.
        """
        curr_state = state.clone()
        depth = 0
        max_depth = 30
        
        # Umbral de inteligencia: Solo pensamos "Smart" los primeros 7 pasos
        smart_depth_limit = 7 
        
        while not curr_state.is_terminal() and depth < max_depth:
            valid_moves = curr_state.get_valid_moves()
            if not valid_moves: break
            
            # --- FASE SMART (Solo primeros pasos) ---
            if depth < smart_depth_limit:
                current_player = curr_state.player_turn
                opponent = -current_player
                
                # 1. ¿Gano YA?
                win_found = False
                for m in valid_moves:
                    # Check ligero sin clonar todo el objeto si es posible, 
                    # pero aquí clonamos por seguridad
                    test_state = curr_state.clone()
                    test_state.make_move(m)
                    if test_state.check_win(current_player):
                        curr_state.make_move(m)
                        win_found = True
                        break
                if win_found: break # Ganamos, fin simulación

                # 2. ¿Debo bloquear YA?
                block_found = False
                for m in valid_moves:
                    test_state = curr_state.clone()
                    test_state.player_turn = opponent # Simular oponente
                    test_state.make_move(m)
                    if test_state.check_win(opponent):
                        curr_state.make_move(m) # Bloqueamos
                        block_found = True
                        break
                if block_found: 
                    depth += 1
                    continue
            
            # --- FASE FAST (O si no hay amenazas) ---
            # Elegimos al azar (con ligero sesgo al centro si está disponible)
            chosen = random.choice(valid_moves)
            curr_state.make_move(chosen)
            depth += 1
            
        return curr_state

    def _run_mcts(self, state):
        start_time = time.time()
        
        try: valid_moves = [c for c in range(7) if state[0, c] == 0]
        except: return 0
        if not valid_moves: return 0
        if len(valid_moves) == 1: return int(valid_moves[0])

        try:
            ones = np.sum(state == 1)
            minus_ones = np.sum(state == -1)
            me = -1 if ones > minus_ones else 1
            opp = -me
            
            game = GameLogic(state, me)
            
            # --- RED DE SEGURIDAD (ROOT) ---
            # Siempre activa y completa en la raíz
            for m in valid_moves:
                g = game.clone()
                g.make_move(m)
                if g.check_win(me): return int(m)
            
            opp_game = GameLogic(state, opp)
            for m in valid_moves:
                g = opp_game.clone()
                g.make_move(m)
                if g.check_win(opp): return int(m)

            # --- MCTS LOOP ---
            root = Node(game)
            sims_count = 0
            
            # Loop dinámico: si nos queda poco tiempo, bajamos la calidad
            while (time.time() - start_time) < self.time_limit:
                node = root
                
                # Selection
                while not node.untried_moves and node.children:
                    node = node.select_child()
                    if not node: break
                
                # Expansion
                if node.untried_moves: node = node.expand()
                
                # Simulation (HÍBRIDA)
                final_state = self._simulate_hybrid(node.state)
                
                # Backprop
                if final_state.check_win(me): winner = 1
                elif final_state.check_win(opp): winner = 0
                else: winner = 0.5
                
                while node:
                    node.visits += 1
                    node.wins += winner
                    node = node.parent
                
                sims_count += 1

            if not root.children: return int(random.choice(valid_moves))
            
            # Robust child
            best_child = max(root.children, key=lambda c: c.visits)
            return int(best_child.move)

        except Exception:
            return int(random.choice(valid_moves))

    def get_action(self, state, *args, **kwargs): return self._run_mcts(state)
    def act(self, state, *args, **kwargs): return self._run_mcts(state)