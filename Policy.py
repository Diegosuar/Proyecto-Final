import numpy as np
import time
import random
from connect4.policy import Policy

# ... (Clases GameLogic y Node se mantienen) ...

class MCTSAgent(Policy):
    def _init_(self):
        self.time_limit = 0.45 # Límite seguro

    # Highlight 2: Buffer de seguridad implementado
    def mount(self, *args, **kwargs):
        if args:
            try:
                val = float(args[0])
                if 0 < val < 5.0: self.time_limit = val - 0.05
            except: pass

    def act(self, state):
        start_time = time.time()
        # ... setup ...
        
        # Highlight 2: Bucle controlado por tiempo
        while (time.time() - start_time) < self.time_limit:
            # ... MCTS logic ...
            pass
        return 0
