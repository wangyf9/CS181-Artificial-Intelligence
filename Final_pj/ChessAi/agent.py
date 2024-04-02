from abc import ABC, abstractmethod
from typing import Optional

from gameModel import GameModel
from utils import Player


class Agent(ABC):
    def __init__(self, direction: Player):
        self.game: Optional[GameModel] = None
        self.direction: Player = direction

    def setGameModel(self, game: GameModel):
        self.game = game

    def update(self, action):
        pass

    @abstractmethod
    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        raise NotImplementedError
