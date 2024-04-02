from queue import Queue
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import skorch
import sklearn
from RandomAgent import RandomAgent

from agent import Agent
from gameModel import GameModel
from gameView import GameView, NoGraphic
from utils import Player, Counter, Piece
from MCTS.MCTSAgent import MCTSAgent
import numpy as np
from nn import ChessModel
import json
import pandas as pd
import optparse
import sys

def readCommand(argv):
    parser = optparse.OptionParser(
        description='Agents P.K.')
    parser.set_defaults(White="RandomAgent", Black="MCTSAgent", noGraphics=False, res=False)
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


def initAgent(side: Player, choice: str, relate_view: GameView, q_value=None) -> Agent:
    if choice == "RandomAgent":
        agent = RandomAgent(side)
    elif choice == "MCTSAgent":
        agent = MCTSAgent(side)
    else:
        assert False, "No such agent!"
    return agent

class SelfTrainer:
    def __init__(self, config, train_data, label):
        self.net = ChessModel(configs = config)
        self.train_data = np.array(train_data)
        self.label = np.array(label)

    def train(self, train_data,train_data_label):
        model = skorch.NeuralNetClassifier(self.net, criterion=torch.nn.CrossEntropyLoss,
                                   device="cuda",
                                   optimizer= torch.optim.Adam,
                                   lr=0.01,
                                   max_epochs=10,
                                   callbacks=[skorch.callbacks.EarlyStopping(lower_is_better=True)])
        model.fit(self.train_data, self.label)##
        torch.save(model.module_.state_dict(), 'model.ckpt')
        


if __name__ == "__main__":
    options = readCommand(sys.argv)
    print(options)
    print("Start training")
    print("Training episode starts..." )
    view = NoGraphic()
    # view = GameView(2)
    white_agent = initAgent(Player.White, options.White, view)
    black_agent = initAgent(Player.Black, options.Black, view)
    model = GameModel(view, white_agent, black_agent)
    _ , _ , train_data, label, new_config = model.startApp()
    print("Length of train_data:", len(train_data))
    print("Length of label:", len(label))
    
    trainer = SelfTrainer(new_config, train_data, label)
    torch.save(trainer.net.state_dict(),'model.ckpt')
    print("Training episode finishes!")

