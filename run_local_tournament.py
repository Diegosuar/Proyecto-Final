from tournament import run_tournament
from policy import MCTSAgent
import sys
import os

# Agrega el directorio actual al path de Python para que encuentre 'connect4'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- TUS IMPORTS NORMALES ---
from tournament import run_tournament
from policy import MCTSAgent
# Necesitamos envolver la clase para cumplir con la firma de 'Participant'
# Participant es una tupla: (Nombre, Clase)

players = [
    ("MCTS_Final", MCTSAgent),
    ("MCTS_Clon_1", MCTSAgent),
    ("MCTS_Clon_2", MCTSAgent),
    ("MCTS_Clon_3", MCTSAgent)
]

# Función lambda para instanciar y jugar (adaptada de tournament.py)
# tournament.py espera una función 'play', pero ya tiene una interna.
# Lo más fácil es usar su función run_tournament si tienes el entorno configurado.

if __name__ == "__main__":
    # Nota: Esto requiere que tengas importado 'play' correctamente de tournament.py
    from tournament import play
    
    winner = run_tournament(
        players=players,
        play=play,
        best_of=3,
        shuffle=True
    )
    print(f"El ganador del torneo local es: {winner[0]}")