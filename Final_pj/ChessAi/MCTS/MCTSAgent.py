from __future__ import annotations

import math
import random

import numpy as np

from agent import Agent
from data import EvaluationMatrix
from gameModel import GameState
from utils import Player, Piece

# Game finishes as tie in 200 round
MAX_ROUND = 200
MAX_DEPTH = 200

class MCTSnode:
    def __init__(self):
        self.num_all_valid_actions = None
        self.parent = None
        self.state = None
        self.all_valid_actions = None
        self.children: dict[GameState: tuple[MCTSnode, tuple[tuple[int, int], tuple[int, int]]]] = {}
        self.visit_time: int = 0
        self.current_depth: int = 0
        self.quality_value: float = 0.0

    def setState(self, state: GameState):
        self.state = state

    def setParent(self, parent: MCTSnode):
        self.parent = parent

    def setVisitTime(self, visit_time: int):
        self.visit_time = visit_time

    def setQualityValue(self, quality_value: float):
        self.quality_value = quality_value

    def is_terminal(self):
        return self.current_depth == MAX_DEPTH
    
    def get_current_depth(self):
        return self.current_depth

    def is_all_expand(self) -> bool:
       ## print("len(self.childen) ==", len(self.children))
        ##print("selfnumallvalidact == ", self.num_all_valid_actions)
        return len(self.children) == self.num_all_valid_actions

    def find_all_valid_actions(self):
        self.all_valid_actions = self.state.getLegalActionsBySide(self.state.myself)
        if self.state.myself == Player.White:
            my_general = Piece.WKing
            other_general = Piece.BKing
            my_bishop = Piece.WBishop
            my_horse = Piece.WKnight
            my_rook = Piece.WRook
        elif self.state.myself == Player.Black:
            my_general = Piece.BKing
            other_general = Piece.WKing
            my_bishop = Piece.BBishop
            my_horse = Piece.BKnight
            my_rook = Piece.BRook

        my_piece_pos = self.state.findPiece(my_general)
        if not my_piece_pos:
            self.all_valid_actions = []
            self.num_all_valid_actions = 0
            return
        # move rules function in a board game. 
        # Based on the type and current position of the game piece, 
        # it calculates all the legal positions that the game piece 
        # can move to on the board
        my_general_neighbor = self.state.getRange(my_piece_pos[0])

        # checkmate opponent
        attack = self.state.getThreatBySide(Player.reverse(self.state.myself))
        other_piece_pos = self.state.findPiece(other_general)
        if other_piece_pos != [] and attack[other_piece_pos[0]] != []:
            actions = []
            for my_piece_pos in attack[other_piece_pos[0]]:
                actions.append((my_piece_pos, other_piece_pos[0]))
            self.all_valid_actions = actions
            self.num_all_valid_actions = len(self.all_valid_actions)
            return
        # avoid action lead to checkmate,
        for action in self.all_valid_actions:
            state = self.state.getNextState(action=action)
            new_threats = state.getThreatBySide(self.state.myself)
            if action[0] == my_piece_pos[0]:
                my_new_piece_pos = action[1]
            else:
                my_new_piece_pos = my_piece_pos[0]
            if new_threats[my_new_piece_pos]:
                self.all_valid_actions.remove(action)
        self.num_all_valid_actions = len(self.all_valid_actions)

        # avoid direct checkmate
        threats = self.state.getThreatBySide(self.state.myself)
        if threats[my_piece_pos[0]]:
            actions = []
            for action in self.all_valid_actions:
                state = self.state.getNextState(action=action)
                new_threats = state.getThreatBySide(self.state.myself)
                if action[0] == my_piece_pos[0]:
                    my_new_piece_pos = action[1]
                else:
                    my_new_piece_pos = my_piece_pos[0]
                if not new_threats[my_new_piece_pos]:
                    actions.append(action)
            if actions:
                self.all_valid_actions = actions
        tmp_all_valid_actions = self.all_valid_actions.copy()
        for action in tmp_all_valid_actions:
            pre_pos = action[0]
            next_pos = action[1]
            if self.state.board[pre_pos[0]][pre_pos[1]] not in (my_bishop, my_rook, my_horse) or pre_pos == my_piece_pos[0]:
                continue
            state = self.state.getNextState(action=action)
            new_threats = state.getThreatBySide(self.state.myself)
            if new_threats[next_pos] and next_pos not in my_general_neighbor:
                tmp_all_valid_actions.remove(action)
        if len(tmp_all_valid_actions) > 0:
            self.all_valid_actions = tmp_all_valid_actions
            self.num_all_valid_actions = len(self.all_valid_actions)

        # assert self.num_all_valid_actions != 0, "get you !"

    def quality_evaluation(self, matrix: EvaluationMatrix) -> None:
        if Player.reverse(self.state.myself) == Player.White:
            my_counter = {Piece.WKing: 1, Piece.WRook: 2, Piece.WKnight: 2, Piece.WBishop: 2, Piece.WQueen: 1, Piece.WPawn: 8}
            enemy_counter = {Piece.BKing: 1, Piece.BRook: 2, Piece.BKnight: 2, Piece.BBishop: 2, Piece.BQueen: 1, Piece.BPawn: 8}
        else:
            my_counter = {Piece.BKing: 1, Piece.BRook: 2, Piece.BKnight: 2, Piece.BBishop: 2, Piece.BQueen: 1, Piece.BPawn: 8}
            enemy_counter = {Piece.WKing: 1, Piece.WRook: 2, Piece.WKnight: 2, Piece.WBishop: 2, Piece.WQueen: 1, Piece.WPawn: 8}
        myPieceLocations = self.state.getSide(Player.reverse(self.state.myself))
        enemyPieceLocations = self.state.getSide(self.state.myself)
        threat_my = self.state.getThreatBySide(Player.reverse(self.state.myself))
        score = 0
        for piece in myPieceLocations:
            pieceType = self.state[piece[0]][piece[1]]
            my_counter[pieceType] -= 1
            score += matrix.pieceValue[pieceType] * matrix.pieceScore[pieceType][piece[0]][piece[1]]
            attack_pos = self.state.getRange(piece)
            for threat in threat_my[piece]:
                score -= matrix.pieceValue[pieceType]
            for position in attack_pos:
                x, y = position
                pieceType = self.state[x][y]
                score += matrix.pieceValue[pieceType]
        for piece in enemyPieceLocations:
            pieceType = self.state[piece[0]][piece[1]]
            enemy_counter[pieceType] -= 1
            score -= matrix.pieceValue[pieceType] * matrix.pieceScore[pieceType][piece[0]][piece[1]]
        for piece in my_counter.keys():
            score -= my_counter[piece] * matrix.pieceValue[piece]
        for piece in enemy_counter.keys():
            score += enemy_counter[piece] * matrix.pieceValue[piece]
        self.quality_value = score

    def expand(self) -> MCTSnode:
        next_state, action = self.randomChooseNextState()
        next_node = MCTSnode()
        next_node.setState(next_state)
        next_node.find_all_valid_actions()
        self.children[next_state] = (next_node, action)
        next_node.parent = self
        return next_node

    def randomExpand(self, matrix: EvaluationMatrix) -> MCTSnode:
        action = random.choice(self.all_valid_actions)
        next_state = self.state.getNextState(action)
        if next_state not in self.children.keys():
            next_node = MCTSnode()
            next_node.setState(next_state)
            next_node.find_all_valid_actions()
            next_node.quality_evaluation(matrix)
            self.children[next_state] = (next_node, action)
            next_node.parent = self
        else:
            next_node = self.children[next_state][0]
        return next_node

    def randomChooseNextState(self) -> tuple[GameState, tuple[tuple[int, int], tuple[int, int]]]:
        choice = None
        if len(self.all_valid_actions) == 0:
            print("Error: all_valid_actions has already been an empty list but still get access to randomChooseNextState function!")
        # elif len(self.all_valid_actions) == 1:
        #     choice = self.all_valid_actions[0]
        else:
            choice = random.choice(self.all_valid_actions)
        self.all_valid_actions.remove(choice)
        next_state = self.state.getNextState(choice)
        return next_state, choice

    def bestChild(self, is_exploration: bool) -> tuple[MCTSnode, tuple[tuple[int, int], tuple[int, int]]]:
        c = 0.707 if is_exploration else 0.0
        UCB_list = np.array([self.calUCB(c, child) for child, _ in self.children.values()])
        best_score = np.amax(UCB_list)
        best_idx = np.argwhere(np.isclose(UCB_list, best_score)).squeeze()
        if best_idx.size > 1:
            best_choice = np.random.choice(best_idx)
        else:
            best_choice = np.argmax(UCB_list)
        best_child, best_action = list(self.children.values())[best_choice]
        return best_child, best_action

    def calRewardFromState(self, direction: Player) -> float:
        winner = self.state.getWinner()
        # if self.state.findPiece(Piece.RGeneral) is not [] and self.state.findPiece(Piece.BGeneral) is not []:
        if winner == direction:
            return 1
        elif winner == Player.reverse(direction):
            return -1
        return 0

    def calUCB(self, c: float, child: MCTSnode) -> float:
        # UCB = quality_value / visit_time + c * sqrt(2 * ln(parent_visit_time) / visit_time)
        if child.visit_time == 0:
            return 0.0
        UCB = child.quality_value / child.visit_time + c * math.sqrt(2 * math.log(self.visit_time) / child.visit_time)
        return UCB


class MCTSAgent(Agent):
    def __init__(self, direction: Player, computation_budget: int = 100):
        super().__init__(direction)
        self.root = MCTSnode()
        self.evaluate_matrix = EvaluationMatrix()
        self.computation_budget = computation_budget
        self.tie = 0
        for key in self.evaluate_matrix.pieceValue.keys():
            self.evaluate_matrix.pieceValue[key] /= 10000
        # self.evaluate_matrix.pieceValue["compensate"] = self.evaluate_matrix.pieceValue[Piece.RChariot]

    # Selection and Expansion
    # 1. selecting the best node to expand based on UCB
    # The input to these phases is the current node from which the search is to be started (for example, the root node). 
    # If the node is already a leaf node, it is returned directly.

    # The basic strategy is to first look for child nodes 
    # that have not been selected yet. If there are multiple 
    # such nodes, one of them is randomly selected. 
    # If all child nodes have been selected at least once, the algorithm selects the child node with the highest UCB value, which balances exploration and exploitation, for expansion. If multiple child nodes have the same UCB value, one of them is randomly selected.
    def select_and_expand(self, node: MCTSnode) -> MCTSnode:
        while not node.state.isMatchOver():
            if node.is_all_expand():
                node, _ = node.bestChild(True)
            else:
                node = node.expand()
                node.quality_evaluation(self.evaluate_matrix)
                return node
        return node
    
    def get_probs(self):
        visit_counts = np.array([child.visit_time for child, _ in self.root.children.values()])
        actions = [action for _, action in self.root.children.values()]
        action_probs = visit_counts / np.sum(visit_counts)
        
        return action_probs
    
    # The Simulation phase
    # 1. perform a random action from a given node to create a new node 
    # 2. return the reward obtained from this simulation. 
    # Input is a node that needs to be expanded (not leaf node)
    def simulation(self, node: MCTSnode) -> tuple[MCTSnode, float]:
        current_round = 0
        while not node.state.isMatchOver():
            # randomly select an action from the available unexecuted actions of the given node.
            node = node.randomExpand(self.evaluate_matrix)
            current_round += 1
            if current_round > MAX_ROUND:
                self.tie += 1
                return node, 0
        node.state.swapDirection()
        reward = node.calRewardFromState(self.direction)
        node.state.swapDirection()
        return node, reward

# In the backpropagation phase of Monte Carlo Tree Search, 
# the reward obtained from executing a new action is propagated back to 
# the nodes that need to be expanded and all the upstream nodes. 
# This helps update the corresponding data in these nodes.
    def backpropagation(self, node: MCTSnode, reward: float):
        while node.parent is not None:
            node.visit_time += 1
            parent = node.parent
            _, action = parent.children[node.state]
            attacker = parent.state[action[0][0]][action[0][1]]
            captured = parent.state[action[1][0]][action[1][1]]
            if captured == Piece.NoneType:
                attacker = Piece.NoneType
            if node.state.myself == self.direction:
                node.quality_value -= reward
            else:
                node.quality_value += reward
            node = node.parent
        node.visit_time += 1

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        print("———MCTS begin———")
        new_state = self.game.getGameState()
        if new_state in self.root.children.keys():
            self.root, _ = self.root.children[new_state]
            self.root.parent = None
        else:
            self.root = MCTSnode()
            self.root.setState(new_state)
            self.root.quality_evaluation(self.evaluate_matrix)
            self.root.state.myself = self.direction
        self.root.find_all_valid_actions()
        self.tie = 0
        for i in range(self.computation_budget):
            # 1. Find the best node to expand
            expand_node = self.select_and_expand(self.root)
            # 2. Random run to add node and get reward
            expand_node, reward = self.simulation(expand_node)
            # 3. Update all passing nodes with reward
            self.backpropagation(expand_node, reward)
        for child, _ in self.root.children.values():
            print(f"{child.visit_time}: {child.quality_value / child.visit_time}")
        # print(*[f"{child.visit_time}: {child.quality_value}" for child, _ in self.root.children.values()])
        self.root, action = self.root.bestChild(False)
        print(action)
        print("———MCTS end———")
        return action
    

