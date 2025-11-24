from abc import ABC, abstractmethod
import numpy as np

class Policy(ABC):
    @abstractmethod
    def act(self, state: np.ndarray) -> int:
        """Returns the column to play."""
        pass

    def mount(self):
        """Called before a game starts."""
        pass