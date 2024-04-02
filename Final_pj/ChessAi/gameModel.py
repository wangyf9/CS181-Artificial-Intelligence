from __future__ import annotations
from threading import Thread
import time
from typing import Optional

from utils import Piece, Player
from gameView import GameView, NoGraphic
import numpy as np 
import copy

class GameState:
    def __init__(self):
        self.board: Optional[list[list[Piece]]] = None
        self.myself = Player.White
        self.whetherfirsttime = np.zeros((8,8))#pawn pos x = 0 - 7; pos y = 6, 1
        for x in range(8):
            self.whetherfirsttime[x][6] = 1
            self.whetherfirsttime[x][1] = 1

    def __getitem__(self, item):
        return self.board[item]

    def getBoard(self):
        return self.board

    @property
    def opponent(self) -> Player:
        return Player.reverse(self.myself)

    def swapDirection(self):
        self.myself = Player.reverse(self.myself)

    def getNextState(self, action: tuple[tuple[int, int], tuple[int, int]]) -> GameState:
        src, dst = action
        newState = copy.deepcopy(self)
        # newState.myself = self.myself
        # newState.board = copy.deepcopy(self.board)
        newState.board[dst[0]][dst[1]] = newState.board[src[0]][src[1]]
        newState.board[src[0]][src[1]] = Piece.NoneType
        newState.swapDirection()
        return newState

    # Note that this function do not care which side you are
    def isValidMove(self, src: tuple[int, int], dst: tuple[int, int]) -> bool:
        src_x, src_y = src
        piece = self.board[src_x][src_y]
        if piece == Piece.NoneType:
            return False
        return dst in self.getRange(src)

    # Don't try to modify this function: it is strange and ugly but fully tested in CS132!
    def getRange(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = position
        pieceType = self.board[x][y]
        result: list[tuple[int, int]] = []
        if pieceType == Piece.NoneType:
            return result

        def checkEmpty(loc_x, loc_y):
            return self.board[loc_x][loc_y] == Piece.NoneType

        def inRangeAndEmpty(loc_x, loc_y):
            if inRange(loc_x, loc_y):
                return self.board[loc_x][loc_y] == Piece.NoneType
            return False

        def inRange(loc_x, loc_y):
            return 0 <= loc_x < 8 and 0 <= loc_y < 8

        def checkForBlack(loc_x, loc_y):
            if Piece.getSide(self.board[loc_x][loc_y]) != Player.Black:
                result.append((loc_x, loc_y))

        def checkForWhite(loc_x, loc_y):
            if Piece.getSide(self.board[loc_x][loc_y]) != Player.White:
                result.append((loc_x, loc_y))

        def safeCheckForBlack(loc_x, loc_y):
            if inRange(loc_x, loc_y):
                checkForBlack(loc_x, loc_y)

        def safeCheckForWhite(loc_x, loc_y):
            if inRange(loc_x, loc_y):
                checkForWhite(loc_x, loc_y)

        if pieceType == Piece.BKing:  # up down right left one step each time
            safeCheckForBlack(x, y + 1)
            safeCheckForBlack(x, y - 1)
            safeCheckForBlack(x - 1, y)
            safeCheckForBlack(x - 1, y - 1)
            safeCheckForBlack(x - 1, y + 1)
            safeCheckForBlack(x + 1, y - 1)
            safeCheckForBlack(x + 1, y + 1)
            safeCheckForBlack(x + 1, y)


        elif pieceType == Piece.BKnight:  # 4
            safeCheckForBlack(x + 2, y - 1)
            safeCheckForBlack(x + 2, y + 1)
            safeCheckForBlack(x + 1, y + 2)
            safeCheckForBlack(x - 1, y + 2)
            safeCheckForBlack(x - 2, y + 1)
            safeCheckForBlack(x - 2, y - 1)
            safeCheckForBlack(x - 1, y - 2)
            safeCheckForBlack(x + 1, y - 2)

        elif pieceType == Piece.BQueen:  # 5
            # Direction: right
            for i in range(1, 8):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForBlack(x + i, y)
                break
            # Direction: left
            for i in range(1, 8):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForBlack(x - i, y)
                break
            # Direction: up
            for i in range(1, 8):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForBlack(x, y - i)
                break
            # Direction: down
            for i in range(1, 8):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForBlack(x, y + i)
                break
            # Direction: right up
            for i in range(1, 8):
                if not inRange(x + i, y - i):
                    break
                if checkEmpty(x + i, y - i):
                    result.append((x + i, y - i))
                    continue
                checkForBlack(x + i, y - i)
                break
            # Direction: left up
            for i in range(1, 8):
                if not inRange(x - i, y - i):
                    break
                if checkEmpty(x - i, y - i):
                    result.append((x - i, y - i))
                    continue
                checkForBlack(x - i, y - i)
                break
            # Direction: right down
            for i in range(1, 8):
                if not inRange(x + i, y + i):
                    break
                if checkEmpty(x + i, y + i):
                    result.append((x + i, y + i))
                    continue
                checkForBlack(x + i, y + i)
                break
            # Direction: left down
            for i in range(1, 8):
                if not inRange(x - i, y + i):
                    break
                if checkEmpty(x - i, y + i):
                    result.append((x - i, y + i))
                    continue
                checkForBlack(x - i, y + i)
                break

        elif pieceType == Piece.BPawn:  # 7
            if(self.whetherfirsttime[x][y] == 1):
                if inRange(x, y + 2):
                    if checkEmpty(x, y + 2) and checkEmpty(x, y + 1):
                        result.append((x, y + 2))
            if inRange(x, y + 1):
                if checkEmpty(x, y + 1):
                    result.append((x, y + 1))
            if inRange(x + 1, y + 1):
                if not checkEmpty(x + 1, y + 1): ##eat
                    safeCheckForBlack(x + 1, y + 1)
            if inRange(x - 1, y + 1):
                if not checkEmpty(x - 1, y + 1):
                    safeCheckForBlack(x - 1, y + 1)
                    
                    
        elif pieceType == Piece.BBishop:  # 5
            # Direction: right up
            for i in range(1, 8):
                if not inRange(x + i, y - i):
                    break
                if checkEmpty(x + i, y - i):
                    result.append((x + i, y - i))
                    continue
                checkForBlack(x + i, y - i)
                break
            # Direction: left up
            for i in range(1, 8):
                if not inRange(x - i, y - i):
                    break
                if checkEmpty(x - i, y - i):
                    result.append((x - i, y - i))
                    continue
                checkForBlack(x - i, y - i)
                break
            # Direction: right down
            for i in range(1, 8):
                if not inRange(x + i, y + i):
                    break
                if checkEmpty(x + i, y + i):
                    result.append((x + i, y + i))
                    continue
                checkForBlack(x + i, y + i)
                break
            # Direction: left down
            for i in range(1, 8):
                if not inRange(x - i, y + i):
                    break
                if checkEmpty(x - i, y + i):
                    result.append((x - i, y + i))
                    continue
                checkForBlack(x - i, y + i)
                break
        elif pieceType == Piece.BRook:  # 5
            # Direction: right
            for i in range(1, 8):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForBlack(x + i, y)
                break
            # Direction: left
            for i in range(1, 8):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForBlack(x - i, y)
                break
            # Direction: up
            for i in range(1, 8):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForBlack(x, y - i)
                break
            # Direction: down
            for i in range(1, 8):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForBlack(x, y + i)
                break
        elif pieceType == Piece.WKing:  # 8
            safeCheckForWhite(x, y + 1)
            safeCheckForWhite(x, y - 1)
            safeCheckForWhite(x - 1, y)
            safeCheckForWhite(x - 1, y - 1)
            safeCheckForWhite(x - 1, y + 1)
            safeCheckForWhite(x + 1, y - 1)
            safeCheckForWhite(x + 1, y + 1)
            safeCheckForWhite(x + 1, y)


        elif pieceType == Piece.WQueen:  # 5
            # Direction: right
            for i in range(1, 8):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForWhite(x + i, y)
                break
            # Direction: left
            for i in range(1, 8):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForWhite(x - i, y)
                break
            # Direction: up
            for i in range(1, 8):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForWhite(x, y - i)
                break
            # Direction: down
            for i in range(1, 8):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForWhite(x, y + i)
                break
            # Direction: right up
            for i in range(1, 8):
                if not inRange(x + i, y - i):
                    break
                if checkEmpty(x + i, y - i):
                    result.append((x + i, y - i))
                    continue
                checkForWhite(x + i, y - i)
                break
            # Direction: left up
            for i in range(1, 8):
                if not inRange(x - i, y - i):
                    break
                if checkEmpty(x - i, y - i):
                    result.append((x - i, y - i))
                    continue
                checkForWhite(x - i, y - i)
                break
            # Direction: right down
            for i in range(1, 8):
                if not inRange(x + i, y + i):
                    break
                if checkEmpty(x + i, y + i):
                    result.append((x + i, y + i))
                    continue
                checkForWhite(x + i, y + i)
                break
            # Direction: left down
            for i in range(1, 8):
                if not inRange(x - i, y + i):
                    break
                if checkEmpty(x - i, y + i):
                    result.append((x - i, y + i))
                    continue
                checkForWhite(x - i, y + i)
                break    
        

            
        elif pieceType == Piece.WBishop:  # 5
            # Direction: right up
            for i in range(1, 8):
                if not inRange(x + i, y - i):
                    break
                if checkEmpty(x + i, y - i):
                    result.append((x + i, y - i))
                    continue
                checkForWhite(x + i, y - i)
                break
            # Direction: left up
            for i in range(1, 8):
                if not inRange(x - i, y - i):
                    break
                if checkEmpty(x - i, y - i):
                    result.append((x - i, y - i))
                    continue
                checkForWhite(x - i, y - i)
                break
            # Direction: right down
            for i in range(1, 8):
                if not inRange(x + i, y + i):
                    break
                if checkEmpty(x + i, y + i):
                    result.append((x + i, y + i))
                    continue
                checkForWhite(x + i, y + i)
                break
            # Direction: left down
            for i in range(1, 8):
                if not inRange(x - i, y + i):
                    break
                if checkEmpty(x - i, y + i):
                    result.append((x - i, y + i))
                    continue
                checkForWhite(x - i, y + i)
                break    
        

            
        elif pieceType == Piece.WRook:  # 12
            # Direction: right
            for i in range(1, 8):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForWhite(x + i, y)
                break
            # Direction: left
            for i in range(1, 8):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForWhite(x - i, y)
                break
            # Direction: up
            for i in range(1, 8):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForWhite(x, y - i)
                break
            # Direction: down
            for i in range(1, 8):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForWhite(x, y + i)
                break

        elif pieceType == Piece.WKnight:  # 11
            safeCheckForWhite(x + 2, y - 1)
            safeCheckForWhite(x + 2, y + 1)

            safeCheckForWhite(x + 1, y + 2)
            safeCheckForWhite(x - 1, y + 2)

            safeCheckForWhite(x - 2, y + 1)
            safeCheckForWhite(x - 2, y - 1)

            safeCheckForWhite(x - 1, y - 2)
            safeCheckForWhite(x + 1, y - 2)


        elif pieceType == Piece.WPawn:  # 14
            if(self.whetherfirsttime[x][y] == 1):
                if inRange(x, y - 2):
                    if checkEmpty(x, y - 2) and checkEmpty(x, y - 1):
                        result.append((x, y - 2))

            if inRange(x, y - 1):
                if checkEmpty(x, y - 1):
                    result.append((x, y - 1))
            if inRange(x + 1, y - 1):
                if not checkEmpty(x + 1, y - 1): ##eat
                    safeCheckForWhite(x + 1, y - 1)
            if inRange(x - 1, y - 1):
                if not checkEmpty(x - 1, y - 1):
                    safeCheckForWhite(x - 1, y - 1)
        return result

    # Returns a dict with {position1: [threat1, threat2], position2: [threat1, threat2, threat3]}
    def getThreatBySide(self, side: Player) -> dict[tuple[int, int], list[tuple[int, int]]]:
        # This is a very naive implementation
        result: dict[tuple[int, int], list[tuple[int, int]]] = {x: [] for x in self.getSide(side)}
        for piece in self.getSide(Player.reverse(side)):
            for position in self.getRange(piece):
                if position in result:
                    result[position].append(piece)
        return result

    def getProtectorBySide(self, side: Player, position: tuple[int, int]) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for piece in self.getSide(side):
            if position in self.getRange(piece):
                result.append(piece)
        return result

    def getWinner(self) -> Player:
        if not any(Piece.BKing in i for i in self.board):
            return Player.White  # BlackGeneral captured, White wins
        elif not any(Piece.WKing in i for i in self.board):
            return Player.Black  # WhiteGeneral captured, Black wins

        whiteG_x, whiteG_y = self.findPiece(Piece.WKing)[0]
        blackG_x, blackG_y = self.findPiece(Piece.BKing)[0]

        whiteLose = True
        all_white = self.getSide(Player.White)
        for whitePiece in all_white:
            if self.getRange(whitePiece):
                whiteLose = False
                break
        if whiteLose:
            return Player.Black

        blackLose = True
        all_black = self.getSide(Player.Black)
        for blackPiece in all_black:
            if self.getRange(blackPiece):
                blackLose = False
                break
        if blackLose:
            return Player.White

        # TODO: if draw, return Player.Draw
        # No pieces captured in 60 steps
        # Three identical moves

        return Player.NoneType

    def isMatchOver(self):
        return self.getWinner() != Player.NoneType

    def init_with_start_game(self):
        self.board = [
            [Piece.BRook, Piece.BPawn, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.WPawn,  Piece.WRook],
            [Piece.BKnight, Piece.BPawn, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.WPawn, Piece.WKnight],
            [Piece.BBishop, Piece.BPawn, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.WPawn, Piece.WBishop],
            [Piece.BQueen, Piece.BPawn, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.WPawn,  Piece.WQueen],
            [Piece.BKing, Piece.BPawn, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.WPawn, Piece.WKing],
            [Piece.BBishop, Piece.BPawn, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.WPawn,  Piece.WBishop],
            [Piece.BKnight, Piece.BPawn, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.WPawn,  Piece.WKnight],
            [Piece.BRook, Piece.BPawn, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.WPawn,Piece.WRook]
        ]

    def getSide(self, side: Player) -> list[tuple[int, int]]:
        return self._find_all_position_that_satisfies(lambda a: Piece.getSide(a) == side)

    # Return all locations of this kind of piece
    def findPiece(self, piece: Piece) -> list[tuple[int, int]]:
        return self._find_all_position_that_satisfies(lambda a: a == piece)

    def getLegalActionsBySide(self, direction: Player) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        actions = []
        for piece in self.getSide(direction):
            actions += [(piece, position) for position in self.getRange(piece)]
        return actions

    def getLegalActionsByPiece(self, piece) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        actions = []
        actions += [(piece, position) for position in self.getRange(piece)]
        return actions
    
    def _find_all_position_that_satisfies(self, condition: callable) -> list[tuple[int, int]]:
        result = []
        for i, x in enumerate(self.board):
            result += [(i, j) for j, y in enumerate(x) if condition(y)]
        return result

    def __eq__(self, other):
        # Allows two states to be compared.
        return hasattr(other, 'board') and self.board == other.board

    def __hash__(self):
        # Allows gameModel to be keys of dictionaries.
        return hash(tuple(tuple(x) for x in self.board))


class GameModel:

    def __init__(self, canvas: GameView, WhiteAgent, BlackAgent):
        self._board = GameState()
        self._board.init_with_start_game()
        self._canvas: GameView = canvas
        self._canvas.setModel(self)
        self._white_agent = WhiteAgent
        self._white_agent.setGameModel(self)
        self._black_agent = BlackAgent
        self._black_agent.setGameModel(self)
        self._draw()
        self._gameThread: Optional[Thread] = None
        self._self_play_data = []
        self.label = []
        self.piecevalue ={
            Piece.BKing: 50, Piece.WKing: 50,#王
            Piece.BQueen: 100, Piece.WQueen: 100,#后
            Piece.BRook: 40, Piece.WRook: 40,#车
            Piece.BBishop: 30, Piece.WBishop: 30,#象
            Piece.BKnight: 25, Piece.WKnight: 25,#马
            Piece.BPawn: 5, Piece.WPawn: 5,#兵
            Piece.NoneType: 0
        }
        self.config = {}

    # Note that this function do not care which side you are
    def isValidMove(self, src: tuple[int, int], dst: tuple[int, int]) -> bool:
        return self._board.isValidMove(src, dst)

    # Make attribute board read-only to agent
    @property
    def board(self):
        return self._board

    def getGameState(self):
        return copy.deepcopy(self._board)

    def getRange(self, position: tuple[int, int]):
        return self._board.getRange(position)

    def getSide(self, side: Player) -> list[tuple[int, int]]:
        return self.board.getSide(side)

    # Return all locations of this kind of piece
    def findPiece(self, piece: Piece) -> list[tuple[int, int]]:
        return self.board.findPiece(piece)

    def getLegalActionsBySide(self, direction: Player) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        return self.board.getLegalActionsBySide(direction)

    def startGame(self):
        time.sleep(1)  # Always sleep one second before initiating
        step = 0
        newpiecevalue = [self.piecevalue[Piece.WQueen]* 1, 
                 self.piecevalue[Piece.WRook] *2 ,
                 self.piecevalue[Piece.WBishop]* 2,
                 self.piecevalue[Piece.WKing]*1,
                 self.piecevalue[Piece.WKnight]*2,
                 self.piecevalue[Piece.WPawn]*8]
        prior = {"prior":newpiecevalue}
        while True:
            thisturn_data = []
            print("len traindata", len(self._self_play_data))
            print("len label", len(self.label))
            if self._board.myself == Player.White:
                src, dst = self._white_agent.step()
                self._black_agent.update((src, dst))
                thisturn_data += [GameState.getBoard(self),Player.White,None]
            elif self._board.myself == Player.Black:
                src, dst = self._black_agent.step()
                self._white_agent.update((src, dst))
                thisturn_data += [GameState.getBoard(self),Player.Black,None]
            else:
                raise  # Robustness
            if Piece.getSide(self._board[src[0]][src[1]]) != self._board.myself:
                assert False, "You should only move your own piece!"
            else:
                self._board[dst[0]][dst[1]] = self._board[src[0]][src[1]]
            self._board[src[0]][src[1]] = Piece.NoneType

            self._draw()
            step +=1
            result = self._board.getWinner()

            self._board.swapDirection()
            if result == Player.NoneType:
                thisturn_data[-1] = 0.0 
                input, label = data_process(self, prior, thisturn_data)
                self._self_play_data.append(input)
                self.label.append(0.0)
                # self._self_play_data.append(thisturn_data) 
                continue
            elif result == Player.White:
                print("White win!") 
                thisturn_data[-1] = 1.0
                input, label = data_process(self, prior, thisturn_data)
                self._self_play_data.append(input)
                self.label.append(1.0)
                return Player.White, step, self._self_play_data, self.label, self.config
                # White wins
            elif result == Player.Black:
                print("Black win!")
                thisturn_data[-1] = -1.0
                input, label = data_process(self, prior, thisturn_data)
                self._self_play_data.append(input)
                self.label.append(label)
                return Player.Black, step, self._self_play_data, self.label, self.config
                # Black wins
            elif result == Player.Draw:
                print("Draw!")
                return Player.Draw, step, self._self_play_data, self.label, self.config

    def _draw(self) -> None:
        self._canvas.draw(self._board)

    def startApp(self) -> Optional[Player]:
        if type(self._canvas) == NoGraphic:
            return self.startGame()
        else:
            self._gameThread = Thread(target=self.startGame, daemon=True)
            self._gameThread.start()
            self._canvas.startApp()

def data_process(self, prior, data):
    ##max_probs_length = max(len(data[1]) for data in origindata)
    newinput = [None] * 16
    for i in range(16):##create 16 * 8 * 8 input 
        newinput[i] = [None] * 8
        for j in range(8):
            newinput[i][j] = [None] * 8
    board = data[0]
    currentplayer = data[1]
    result = data[2]
    ##process board
    for i in range(8):
        for j in range(8):
            piecetype = board[i][j]
            if piecetype == Piece.BKing:
                newinput[0][i][j] = 1
            else:
                newinput[0][i][j] = 0
            if piecetype == Piece.BQueen:
                newinput[1][i][j] = 1
            else:
                newinput[1][i][j] = 0
            if piecetype == Piece.BRook:
                newinput[2][i][j] = 1
            else:
                newinput[2][i][j] = 0   
            if piecetype == Piece.BBishop:
                newinput[3][i][j] = 1
            else:
                newinput[3][i][j] = 0        
            if piecetype == Piece.BKnight:
                newinput[4][i][j] = 1
            else:
                newinput[4][i][j] = 0        
            if piecetype == Piece.BPawn:
                newinput[5][i][j] = 1
            else:
                newinput[5][i][j] = 0 
            if piecetype == Piece.WKing:
                newinput[6][i][j] = 1
            else:
                newinput[6][i][j] = 0
            if piecetype == Piece.WQueen:
                newinput[7][i][j] = 1
            else:
                newinput[7][i][j] = 0
            if piecetype == Piece.WRook:
                newinput[8][i][j] = 1
            else:
                newinput[8][i][j] = 0
            if piecetype == Piece.WBishop:
                newinput[9][i][j] = 1
            else:
                newinput[9][i][j] = 0
            if piecetype == Piece.WKnight:
                newinput[10][i][j] = 1
            else:
                newinput[10][i][j] = 0
            if piecetype == Piece.WPawn:
                newinput[11][i][j] = 1
            else:
                newinput[11][i][j] = 0
            # Generate our side's piece layout
            if piecetype == Piece.WKing or piecetype == Piece.WQueen or piecetype == Piece.WRook or piecetype == Piece.WBishop or piecetype == Piece.WKnight or piecetype == Piece.WPawn:
                newinput[12][i][j] = 1
            else:
                newinput[12][i][j] = 0
            # Generate opponent's piece layout
            if piecetype == Piece.BKing or piecetype == Piece.BQueen or piecetype == Piece.BRook or piecetype == Piece.BBishop or piecetype == Piece.BKnight or piecetype == Piece.BPawn:
                newinput[13][i][j] = 1
            else:
                newinput[13][i][j] = 0
    self.config = prior
    for i in range(8):
        for j in range(8):
            newinput[14][i][j] = 0
            newinput[15][i][j] = 0
    if currentplayer == Player.Black:
        newinput[14][0][0] = -1
    else:
        newinput[14][0][0] = 1
    newinput[15][0][0] = 0#white first

    newinput = np.array(newinput)
    flattened_data = newinput.reshape((16, -1))
    total = (flattened_data, result)
    return total