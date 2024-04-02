from agent import Agent
from utils import Player, Piece
from gameModel import GameState
import random


class RandomAgent(Agent):
    def __init__(self, direction: Player):
        super().__init__(direction)
        # self.kingposx = 4
        # self.kingposy = 0

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        all_pieces = self.game.getSide(self.direction)

        while True:
            whetherking = 0
            gameState = self.game.getGameState()
            myThreat = gameState.getThreatBySide(Player.White)
            kingposx = 0
            kingposy = 0
            for piece in all_pieces:
                x, y = piece
                piecetype = gameState[x][y]
                if len(myThreat[piece]) != 0 and piecetype == Piece.WKing:
                    # print("king")
                    kingposx = x
                    kingposy = y
                    whetherking = 1
                    pos: tuple[int, int] = (x, y)
                    break
                else:
                    pos: tuple[int, int] = random.choice(all_pieces)
            all_valid_move = self.game.getRange(pos)
            if len(all_valid_move) == 0:
                # print("kingmove fail")
                if(whetherking == 1):
                    king_neighbors = [(kingposx + dx, kingposy + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                              if (0 <= kingposx + dx < 8) and (0 <= kingposy + dy < 8) and (dx, dy) != (0, 0)]
                    friendly_neighbors: tuple[int, int] = [pos for pos in king_neighbors if pos in all_pieces]
                    if friendly_neighbors:
                        piece_to_move = random.choice(friendly_neighbors)
                        all_valid_moves = self.game.getRange(piece_to_move)
                        if all_valid_moves:
                            move = random.choice(all_valid_moves)
                            return piece_to_move, move    
                else:
                    continue
            action = random.choice(all_valid_move)

            return pos, action
