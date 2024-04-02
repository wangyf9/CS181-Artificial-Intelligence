from agent import Agent
from data import EvaluationMatrix
from utils import Player, Piece
import math
from gameModel import GameState
import random

class ExpectimaxAgent(Agent, EvaluationMatrix):

    def __init__(self, direction: Player, depth=2):
        Agent.__init__(self, direction)
        EvaluationMatrix.__init__(self)
        self.index = 0
        self.depth = depth
        self.playerSide = direction

    def evaluationFunction(self, gameState: GameState) -> float:
        winner = gameState.getWinner()
        # Game End
        if winner is not None:
            if winner == self.playerSide:
                return 1000000.0
            elif winner == self.playerSide:
                return -1000000.0
        # Evaluate
        # Give more weight to protecting my pieces than threating others to play more conservative
        mypieces = gameState.getSide(self.playerSide)
        enemypieces = gameState.getSide(Player.reverse(self.playerSide))
        myThreat = gameState.getThreatBySide(self.playerSide)
        score = 0.0
        for piecePos in mypieces:
            x, y = piecePos
            pieceType = gameState[x][y]
            score += self.pieceValue[pieceType] * self.pieceScore[pieceType][x][y]
            # Deal with threat to my side (give more weight to being threat)
            score -= (2 * self.pieceValue[pieceType] * len(myThreat[piecePos]))
            protector = gameState.getProtectorBySide(self.playerSide,  piecePos)
            score += self.pieceValue[pieceType] * len(protector)
            # Deal with attack to opponent
            attackPosition = gameState.getRange(piecePos)
            for pos_x,pos_y in attackPosition:
                type = gameState[pos_x][pos_y]
                if pieceType != Piece.NoneType:
                    score += self.pieceValue[type]
        # Deal with enemy count
        for x,y in enemypieces:
            type = gameState[x][y]
            score -= self.pieceValue[type] * self.pieceScore[type][x][y]
        return score

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
            
        def maxValue(state, depth, playerSide):
            v = -math.inf
            if state.isMatchOver():
                return self.evaluationFunction(state)
            if depth == self.depth:
                return self.evaluationFunction(state)
            legalActions = state.getLegalActionsBySide(playerSide)
            for action in legalActions:
                v = max(v, minValue(state.getNextState(action), depth + 1, Player.reverse(playerSide)))
            return v
        
        def minValue(state, depth, playerSide):
            v = math.inf
            if state.isMatchOver():
                return self.evaluationFunction(state)
            if depth == self.depth:
                return self.evaluationFunction(state)
            value_sum = 0
            legalActions = state.getLegalActionsBySide(playerSide)
            for action in legalActions:
                v = min(v, maxValue(state.getNextState(action), depth + 1, Player.reverse(playerSide)))
                value_sum += v
            return value_sum/len(legalActions)
        
        print("———Expectimax begin———")
        gameState = self.game.getGameState()
        totalPieces = len(gameState.getSide(self.playerSide)) + len(gameState.getSide(Player.reverse(self.playerSide)))
        self.depth = int((32 - totalPieces) / 8) + 2
        legalMoves = gameState.getLegalActionsBySide(self.playerSide)
        tmp_state = None
        for move in legalMoves:
            tmp_state = gameState.getNextState(move)
            if tmp_state.isMatchOver():
                return move
        bestMove = None
        bestValue = -math.inf
        # shuffledMoves = random.shuffle(list(legalMoves))
        for move in legalMoves:
            depth = 1
            score = minValue(gameState.getNextState(move), depth, Player.reverse(self.playerSide))
            if score > bestValue:
                bestValue = score
                bestMove = move
            print("score == ", score)
        print("———Expectimax end———")
        return bestMove
