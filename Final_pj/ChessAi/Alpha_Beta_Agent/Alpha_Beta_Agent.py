from agent import Agent
from data import EvaluationMatrix
from utils import Player, Piece
import math
from gameModel import GameState
import random

class Alpha_Beta_Agent(Agent, EvaluationMatrix):

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

        def maxValue(state, depth, playerSide, a, b):
            if depth == self.depth * 2 or state.isMatchOver():
                return self.evaluationFunction(state)
            maximum = -math.inf
            legalActions = state.getLegalActionsBySide(playerSide)
            for action in legalActions:
                maximum = max(maximum,
                              minValue(state.getNextState(action), depth + 1, Player.reverse(playerSide), a, b))
                if maximum > b:
                    return maximum
                a = max(a, maximum)
            return maximum

        def minValue(state, depth, playerSide, a, b):
            if depth == self.depth * 2 or state.isMatchOver():
                return self.evaluationFunction(state)
            minimum = math.inf
            legalActions = state.getLegalActionsBySide(playerSide)
            for action in legalActions:
                minimum = min(minimum,
                              maxValue(state.getNextState(action), depth + 1, Player.reverse(playerSide), a, b))
                if minimum < a:
                    return minimum
                b = min(b, minimum)
            return minimum

        print("———Alpha_Beta begin———")
        gameState = self.game.getGameState()
        totalPieces = len(gameState.getSide(self.playerSide)) + len(gameState.getSide(Player.reverse(self.playerSide)))
        self.depth = int((32 - totalPieces) / 8) + 2
        legalMoves = gameState.getLegalActionsBySide(self.playerSide)
        bestMove = None
        bestValue = -math.inf
        alpha = -math.inf
        beta = math.inf
        for move in legalMoves:
            value = minValue(gameState.getNextState(move), 1, Player.reverse(self.playerSide), alpha, beta)
            if value > bestValue:
                bestValue = value
                bestMove = move
            if value > beta:
                break
            alpha = max(alpha, value)
            print("alpha == ",alpha)
        print("———Alpha_Beta end———")
        return bestMove
