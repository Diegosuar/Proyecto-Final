from pydantic import BaseModel
from typing import List, Tuple, Optional, Any, Type
from ..policy import Policy

# Participant es (Nombre, Clase del Agente)
Participant = Tuple[str, Type[Policy]]
Versus = List[Tuple[Optional[Participant], Optional[Participant]]]
Game = List[Tuple[List[List[int]], int]] # Historia del juego

class Match(BaseModel):
    player_a: str
    player_b: str
    player_a_wins: int
    player_b_wins: int
    draws: int
    games: List[Game]