# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        ##print("childgamestate11",childGameState)
        newPos = childGameState.getPacmanPosition()
        ##print("newPos22",newPos)
        newFood = childGameState.getFood()
        ##print("newFood33",newFood)
        newGhostStates = childGameState.getGhostStates()
        ##print("newGhostStates44",newGhostStates)
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ##print("newScaredTimes55",newScaredTimes)
        "*** YOUR CODE HERE ***"
        final_score = 0##childGameState.getScore()
        whether_scared = 0              ##record whether scared
        if(newScaredTimes[0] > 0):      
            whether_scared = 1 
        ##Process position and distance   
        foods_pos = newFood.asList()    ##record food position  ##food.list can update automatically
        foods_dis = []                  ##record food distance between food and pacman
        for i in range(len(foods_pos)):
            foods_dis.append(manhattanDistance(newPos,foods_pos[i]))  ##update the distance list
        ghosts_pos = []                  ## record ghost position
        ghost_dis = []                  ## record ghost dis
        for ghost in newGhostStates:
            ghost_pos = ghost.getPosition()
            ghosts_pos.append(ghost_pos)
            ghost_dis.append(manhattanDistance(ghost_pos,newPos))
        foods_dis.sort()
        ghost_dis.sort()
        ##Process extreme condition
        if ((whether_scared == 0) and (newPos in ghosts_pos)):
            ##print("1")
            return float(-1)
        if (newPos in currentGameState.getFood().asList()):
            ##print("2")
            return float(1)
        #Process total score
        final_score = 1/foods_dis[0] - 1/ghost_dis[0]
       ## print(final_score)
        return final_score
 
def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #In this part, it can be seen that all agents are stored in a list and will be executed in sequence 
        #0 is player, and 1 to -1 are ghost agents
        Ghost_index = [index for index in range(1,gameState.getNumAgents())] #Because agentIndex = 0 means Pacman, ghosts are >= 1
        
        def min_layer(state, d, ghost_index):        #Find the top line
            if (state.isWin() or state.isLose() or d == self.depth) == 1:  #check whether the game is finished
                return self.evaluationFunction(state)
            
            score = 1e10 ##Infinite
            for action in state.getLegalActions(ghost_index): #Recursive to find the min_value for current layer(including all layers under it)
                if ghost_index == Ghost_index[-1]:            #We need to go to the next layer that is max_layer, because we have checked all ghost in this layer. And then we need to recursive to calculate next layer for player
                    score = min(score, max_layer(state.getNextState(ghost_index, action), d + 1))               ##random find path for ghost
                else:                                         #We find the min_value in current layer for ghosts.
                    score = min(score, min_layer(state.getNextState(ghost_index, action), d, ghost_index + 1)) ##random find path for ghost
            return score

        def max_layer(state, d):                     #Find the bottom line
            if (state.isWin() or state.isLose() or d == self.depth) == 1:  #check whether the game is finished
                return self.evaluationFunction(state)
            score = -1e10 ##-Infinite
            for action in state.getLegalActions(0):
                score = max(score, min_layer(state.getNextState(0, action), d, 1))  ##We need to go to the next layer for ghosts to find the max_Value for current layer for player
            return score 
        ##Then we can to generate our minimaxAgent from the root(player)
        Total_score = [(action, min_layer(gameState.getNextState(0, action), 0, 1)) for action in gameState.getLegalActions(0)]
        Total_score = sorted(Total_score, key = lambda y: y[1]) ##y is function parameter, total_score is incoming parameter, y[1] is the concrete the function
        return Total_score[-1][0] ##remember this is the minimax agent, we need find the max score for player
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ##The core of AlphaBetaAgent is adding the purning operation to cut down unnecessary step when the bottom line alpha is bigger than the top line beta
         
        Ghost_index = [index for index in range(1,gameState.getNumAgents())] #Because agentIndex = 0 means Pacman, ghosts are >= 1
        
        def min_layer(state, d, ghost_index, A, B):        #Find the top line
            if (state.isWin() or state.isLose() or d == self.depth) == 1:  #check whether the game is finished
                return self.evaluationFunction(state)
            
            score = 1e10 ##Infinite
            for action in state.getLegalActions(ghost_index): #Recursive to find the min_value for current layer(including all layers under it)
                if ghost_index == Ghost_index[-1]:            #We need to go to the next layer that is max_layer, because we have checked all ghost in this layer. And then we need to recursive to calculate next layer for player
                    score = min(score, max_layer(state.getNextState(ghost_index, action), d + 1, A, B))               ##random find path for ghost
                else:                                         #We find the min_value in current layer for ghosts.
                    score = min(score, min_layer(state.getNextState(ghost_index, action), d, ghost_index + 1, A, B)) ##random find path for ghost
                if score < A:           ##top line < bottom line
                    return score        ##purne directly
                B = min(B, score)     
            return score

        def max_layer(state, d, A, B):                     #Find the bottom line
            if (state.isWin() or state.isLose() or d == self.depth) == 1:  #check whether the game is finished
                return self.evaluationFunction(state)
            score = -1e10 ##-Infinite
            for action in state.getLegalActions(0):
                score = max(score, min_layer(state.getNextState(0, action), d, 1, A, B))  ##We need to go to the next layer for ghosts to find the max_Value for current layer for player
                if score > B:           ##top line < bottom line
                    return score        ##purne directly
                A = max(A, score)  
            return score 
        
        alpha = -1e10                                  ##set up the parameter and in this step it's similar with the max_layer, because the root is the player which we need to find the maximum
        beta = 1e10
        return_act = None
        score = -1e10
        for action in gameState.getLegalActions(0):    ##start the alpha beta agent 
            cur_score = min_layer(gameState.getNextState(0, action), 0, 1, alpha, beta)
            if score < cur_score:
                score = cur_score
                return_act = action
            if score > beta: ##purne
                return return_act
            alpha = max(alpha, cur_score)
        return return_act


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        ##In this part, actually it is also similar with the minimax agent, and all we need to do is to multiply probability to next layer when in min layer

        Ghost_index = [index for index in range(1,gameState.getNumAgents())] #Because agentIndex = 0 means Pacman, ghosts are >= 1
        
        def min_layer(state, d, ghost_index):        #Find the top line
            if (state.isWin() or state.isLose() or d == self.depth) == 1:  #check whether the game is finished
                return self.evaluationFunction(state)
            p = 1 / len(state.getLegalActions(ghost_index))
            score = 0 
            for action in state.getLegalActions(ghost_index): #Recursive to find the min_value for current layer(including all layers under it)
                if ghost_index == Ghost_index[-1]:            #We need to go to the next layer that is max_layer, because we have checked all ghost in this layer. And then we need to recursive to calculate next layer for player
                    score += p * max_layer(state.getNextState(ghost_index, action), d + 1)              ##random find path for ghost
                else:                                         #We find the min_value in current layer for ghosts.
                    score += p * min_layer(state.getNextState(ghost_index, action), d, ghost_index + 1) ##random find path for ghost
            return score

        def max_layer(state, d):                     #Find the bottom line
            if (state.isWin() or state.isLose() or d == self.depth) == 1:  #check whether the game is finished
                return self.evaluationFunction(state)
            score = -1e10 ##-Infinite
            for action in state.getLegalActions(0):
                score = max(score, min_layer(state.getNextState(0, action), d, 1))  ##We need to go to the next layer for ghosts to find the max_Value for current layer for player
            return score 
        ##Then we can to generate our minimaxAgent from the root(player)
        Total_score = [(action, min_layer(gameState.getNextState(0, action), 0, 1)) for action in gameState.getLegalActions(0)]
        Total_score = sorted(Total_score, key = lambda y: y[1]) ##y is function parameter, total_score is incoming parameter, y[1] is the concrete the function
        return Total_score[-1][0] ##remember this is the minimax agent, we need find the max score for player

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    ##print("newPos22",newPos)
    newFood = currentGameState.getFood()
    ##print("newFood33",newFood)
    newGhostStates = currentGameState.getGhostStates()
    ##print("newGhostStates44",newGhostStates)
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ##print("newScaredTimes55",newScaredTimes)

    final_score = 0
    whether_scared = (min(newScaredTimes) > 0)
    ##Process food
    foods_pos = newFood.asList()    ##record food position  ##food.list can update automatically
    foods_dis = []                  ##record food distance between food and pacman
    for i in range(len(foods_pos)):
        foods_dis.append(manhattanDistance(newPos,foods_pos[i]))  ##update the distance list
    foods_dis.sort()

    ##Process ghost
    ghosts_pos = []                  ## record ghost position
    ghost_dis = []                  ## record ghost dis
    for ghost in newGhostStates:
        ghost_pos = ghost.getPosition()
        ghosts_pos.append(ghost_pos)
        ghost_dis.append(manhattanDistance(ghost.getPosition(),newPos))
    ghost_dis.sort()

    #Process extreme condition
    if (currentGameState.isLose()):
        return float(-1)
    if ((whether_scared == 0) and (newPos in ghosts_pos)):
        return float(-1)
    if (newPos in currentGameState.getFood().asList()):
        return float(1)
    
    ##Process capsule, which can help us get a higher grade and correct action
    if (len(currentGameState.getCapsules()) < 2):
        final_score += 500
    if ((len(foods_dis) == 0) or len(ghost_dis) == 0) :
        final_score += scoreEvaluationFunction(currentGameState)
    else:
        final_score += scoreEvaluationFunction(currentGameState) + 1/foods_dis[0] - 1/ghost_dis[0] - 1/ghost_dis[-1]
    return final_score
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState: GameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()