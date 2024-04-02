from tkinter import Frame, Canvas, Tk, Event, PhotoImage
from typing import Optional
from queue import Queue, Full

from utils import Piece, Player


class Texture:
    def __init__(self, scale: int):
        self._textures = {
            "NoneType": PhotoImage(file="img/piece_0.png"),
            "BKing": PhotoImage(file="img/b_k.png"),
            "BQueen": PhotoImage(file="img/b_q.png"),
            "BRook": PhotoImage(file="img/b_r.png"),
            "BPawn": PhotoImage(file="img/b_p.png"),
            "BBishop": PhotoImage(file="img/b_b.png"),
            "BKnight": PhotoImage(file="img/b_n.png"),
            "WKing": PhotoImage(file="img/w_k.png"),
            "WQueen": PhotoImage(file="img/w_q.png"),
            "WRook": PhotoImage(file="img/w_r.png"),
            "WBishop": PhotoImage(file="img/w_b.png"),
            "WKnight": PhotoImage(file="img/w_n.png"),
            "WPawn": PhotoImage(file="img/w_p.png"),
            "ChoiceBox": PhotoImage(file="img/ChoiceBox.png")
        }
        self.size = 25
        if scale == 4:
            self.size *= 4
            for i, j in self._textures.items():
                self._textures[i] = j.zoom(4, 4)
        elif scale == 2:
            self.size *= 2
            for i, j in self._textures.items():
                self._textures[i] = j.zoom(2, 2)

    def choiceBox(self):
        return self._textures["ChoiceBox"]

    def __getitem__(self, item: Piece):
        return self._textures[item.name]


class NoGraphic:
    def __init__(self):
        pass

    def draw(self, grid):
        pass

    def setModel(self, model):
        pass


class GameView:
    def __init__(self, scale: int):
        self.root = Tk(className="International Chess")
        self.root.resizable(False, False)
        self.root.bind("<Escape>", lambda _: self.root.destroy())
        self.frame = Frame(self.root)
        self.frame.pack()
        self.model = None  # GameModel
        self.root.geometry("550x550")
        self.canvas = Canvas(self.frame, bg="black", width=550, height=550)
        self.background = PhotoImage(file="img/Board.png")
        self.canvas.create_image(550 / 2, 550 / 2, image=self.background, tags="bg")
        self.x_index = (70, 130, 185, 245, 305, 365, 420, 480)
        self.y_index = (70, 130, 185, 245, 310, 370, 425, 485)

        self.canvas.bind_all("<Button-1>", self.clickCallbackFunc)
        self.canvas.pack()

        self.texture = Texture(scale)
        for i, x in enumerate(self.x_index):
            for j, y in enumerate(self.y_index):
                self.canvas.create_image(x, y, image=self.texture[Piece.NoneType], tags=f"{i}-{j}")
        self.canvas.create_image(-1000, -1000, image=self.texture.choiceBox(), tags="ChoiceBox")

        # Mouse control
        self.clickData: Optional[tuple[int, int]] = None
        self.white_queue: Optional[Queue] = None
        self.black_queue: Optional[Queue] = None

    def draw(self, grid):
        self.canvas.moveto(self.canvas.gettags("ChoiceBox")[0], -1000, -1000)
        for i in range(8):
            for j in range(8):
                self.canvas.itemconfigure(self.canvas.find_closest(self.x_index[i], self.y_index[j])[0], image=self.texture[grid[i][j]])
        self._update_choice_and_draw()

    def _update_choice_and_draw(self):
        if self.clickData is None:
            self.canvas.moveto(self.canvas.gettags("ChoiceBox")[0], -1000, -1000)
        else:
            self.canvas.moveto(self.canvas.gettags("ChoiceBox")[0], self.x_index[self.clickData[0]] - self.texture.size, self.y_index[self.clickData[1]] - self.texture.size)
        self.canvas.update()

    def clickCallbackFunc(self, event: Event):
        itemId = self.canvas.find_closest(event.x, event.y)
        if len(itemId) == 0:
            return
        itemTag = self.canvas.gettags(itemId[0])[0].split("-")
        if itemTag[0] == "bg":
            return
        elif itemTag[0] == "ChoiceBox":
            self.clickData = None
        else:
            x = int(itemTag[0])
            y = int(itemTag[1])
            if self.clickData is None:
                self.clickData = (x, y)
            elif self.clickData == (x, y):
                self.clickData = None
            else:
                try:
                    if self.white_queue is not None:
                        self.white_queue.put((self.clickData, (x, y)), block=False)
                except Full:
                    pass
                try:
                    if self.black_queue is not None:
                        self.black_queue.put((self.clickData, (x, y)), block=False)
                except Full:
                    pass
                self.clickData = None
        self._update_choice_and_draw()

    def enableMouse(self, side: Player, tunnel: Queue):
        if side == Player.NoneType:
            print("Invalid side!")
        elif side == Player.White:
            self.white_queue = tunnel
        else:
            self.black_queue = tunnel

    def setModel(self, model):
        self.model = model

    def startApp(self):
        self.root.mainloop()
