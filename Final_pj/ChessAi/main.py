from multiprocessing import Pool
from queue import Queue
from typing import Optional

from RandomAgent import RandomAgent
from MinimaxAgent.MinimaxAgent import MinimaxAgent
from ExpectimaxAgent.ExpectimaxAgent import ExpectimaxAgent
from agent import Agent
from gameModel import GameModel
from gameView import GameView, NoGraphic
from utils import Player, Counter, Piece
from MCTS.MCTSAgent import MCTSAgent
from Alpha_Beta_Agent.Alpha_Beta_Agent import Alpha_Beta_Agent
from nnagent import NNagent
import json
import optparse
import sys
import torch
def readCommand(argv):
    parser = optparse.OptionParser(
        description='Agents P.K.')
    parser.set_defaults(White="MinimaxAgent", Black="NNAgent", noGraphics=False, res=False)
    parser.add_option('-w',
                      dest='White',
                      action='store',
                      help='The player of white side.')
    parser.add_option('-b',
                      dest='Black',
                      action='store',
                      help='The player of black side.')
    parser.add_option('-n',
                      dest='noGraphics',
                      action='store_true',
                      help='No graphics display.')
    parser.add_option('-r',
                      dest='res',
                      action='store_true',
                      help='Open with graphic display.')
    (options, args) = parser.parse_args(argv)
    return options


def initAgent(side: Player, choice: str, relate_view: GameView, x, q_value=None) -> Agent:
    if choice == "RandomAgent":
        agent = RandomAgent(side)
    elif choice == "MinimaxAgent":
        agent = MinimaxAgent(side)
    elif choice == "MCTSAgent":
        agent = MCTSAgent(side)
    elif choice == "ExpectimaxAgent":
        agent = ExpectimaxAgent(side)
    elif choice == "Alpha_Beta_Agent":
        agent = Alpha_Beta_Agent(side)
    elif choice == "NNAgent":
        agent = NNagent(side, x)
    else:
        assert False, "No such agent!"
    return agent


def singleGame(options) -> Optional[Player]:
    if options.noGraphics:
        view = NoGraphic()
    elif options.res:
        view = GameView(1)
    x = torch.zeros(16*64)
    white_agent = initAgent(Player.White, options.White, view, x)
    black_agent = initAgent(Player.Black, options.Black, view, x)
    model = GameModel(view, white_agent, black_agent)
    return model.startApp()

def multiGame(options, num):
    White_Win_Time = 0
    Black_Win_Time = 0
    step = 0
    x = torch.zeros(16*64)
    if options.noGraphics:
        view = NoGraphic()
    elif options.res:
        view = GameView(1)
    for _ in range(num):
        white_agent = initAgent(Player.White, options.White, view, x)
        black_agent = initAgent(Player.Black, options.Black, view, x)
        model = GameModel(view, white_agent, black_agent)
        result = model.startApp()
        if result[0] == Player.White:
            White_Win_Time += 1
        elif result[0] == Player.Black:
            Black_Win_Time += 1
        step += result[1]
    return White_Win_Time, Black_Win_Time, float(step/num)
    

if __name__ == "__main__":
    options = readCommand(sys.argv)
    print(options)
    result = multiGame(options, 25)
    if options.noGraphics:
        print("White", options.White, "win for ", result[0], " times.")
        print("Black", options.Black, "win for ", result[1], " times.")
        print("Expecti_step = ", result[2])