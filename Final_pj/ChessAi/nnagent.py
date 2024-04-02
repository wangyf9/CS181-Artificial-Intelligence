from agent import Agent
from utils import Player, Piece
from gameModel import GameState
import random
import torch
from nn import ChessModel
import numpy as np
class NNagent(Agent):
    def __init__(self, direction: Player, x, configs: dict = {}):
        super().__init__(direction)
        self.model = ChessModel(configs = configs)
        checkpoint = torch.load('model.ckpt')
        self.model.load_state_dict(checkpoint)
        self.probs = (self.model(x)).detach().numpy()

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        all_pieces = self.game.getSide(self.direction)

        while True:
            whetherking = 0
            gameState = self.game.getGameState()
            myThreat = gameState.getThreatBySide(Player.Black)
            pawnpiece = self.game.findPiece(Piece.BPawn)
            queenpiece = self.game.findPiece(Piece.BQueen)
            kingpiece = self.game.findPiece(Piece.BKing)
            knightpiece = self.game.findPiece(Piece.BKnight)
            rookpiece = self.game.findPiece(Piece.BRook)
            bishoppiece = self.game.findPiece(Piece.BBishop)
            kingposx = 0
            kingposy = 0
            pos: tuple[int, int] = (kingposx, kingposy)
            for piece in all_pieces:
                x, y = piece
                piecetype = gameState[x][y]
                if len(myThreat[piece]) != 0 and piecetype == Piece.BKing:
                   ## print("king")
                    kingposx = x
                    kingposy = y
                    whetherking = 1
                    pos: tuple[int, int] = (x, y)
                    break
                else:
                    choose = np.random.choice(len(self.probs), p=self.probs)
                    if(choose == 0 and knightpiece != []):
                       ##print("kinght",knightpiece)
                        pos: tuple[int, int] = random.choice(knightpiece)
                    elif(choose == 1 and pawnpiece != []):
                       ## print("pawnpiece",pawnpiece)
                        pos: tuple[int, int] = random.choice(pawnpiece)
                    elif(choose == 2 and kingpiece != []):
                       ## print("kingpiece",kingpiece)
                        pos: tuple[int, int] = random.choice(kingpiece)
                    elif(choose == 3 and queenpiece != []):
                       ## print("queenpiece",queenpiece)
                        pos: tuple[int, int] = random.choice(queenpiece)
                    elif(choose == 4 and bishoppiece != []):
                       ## print("bishoppiece",bishoppiece)
                        pos: tuple[int, int] = random.choice(bishoppiece)
                    elif(choose == 5 and rookpiece != []):    
                       ## print("rookpiece",rookpiece)        
                        pos: tuple[int, int] = random.choice(rookpiece)                    
            all_valid_move = self.game.getRange(pos)
            if len(all_valid_move) == 0:
                if(whetherking == 1):
                   ## print("kingmove fail")
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