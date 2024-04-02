import enum


class Player(enum.Enum):
    NoneType = 0
    White = 1
    Black = -1
    Draw = 10  # For getWinner()

    @staticmethod
    def reverse(side):
        if side == Player.NoneType:
            return Player.NoneType
        elif side == Player.White:
            return Player.Black
        elif side == Player.Black:
            return Player.White
        else:
            assert False, "Player.reverse is called upon Player.Draw"  # Theoretically not possible


class Piece(enum.Enum):
    # Black/White
    # General, Advisor, Elephant, Horse, Chariot, Cannon, Soldier
    NoneType = 0
    BKing = 1
    BQueen = 2
    BRook = 3
    BBishop = 4
    BKnight = 5
    BPawn = 6
    WKing = 7
    WQueen = 8
    WRook = 9
    WBishop = 10
    WKnight = 11
    WPawn = 12

    @staticmethod
    def getSide(piece) -> Player:
        if piece == Piece.NoneType:
            return Player.NoneType
        elif "W" == piece.name[0]:
            return Player.White
        else:
            return Player.Black

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value


class Counter(dict):

    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

