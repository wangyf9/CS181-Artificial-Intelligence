# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    ##print("Start:", problem.getStartState()) ##Let me know what is the starter point
    ##print("Is the start a goal?", problem.isGoalState(problem.getStartState()))##Let me check the test
    ##print("Start's successors:", problem.getSuccessors(problem.getStartState()))##Let me know what I should do about stack (chilenode, direction, step)
    my_Stack = util.Stack()
    my_Stack.push([problem.getStartState(),0,[]]) ###[state,cost,path]
    expanded = set()
    while my_Stack.isEmpty() == False:
        [current_state,current_cost,current_path] = my_Stack.pop()
        if problem.isGoalState(current_state):
            ##print(current_path)
            return current_path
        if current_state not in expanded:
            expanded.add(current_state)
            for childstate,direction,cost in problem.getSuccessors(current_state): ##direction thatis action
                newpath = current_path+[direction]                            ##this is two list + become a new list in nature
                newcost = current_cost + cost
                my_Stack.push([childstate,newcost,newpath])

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    ##print("Start:", problem.getStartState()) ##Let me know what is the starter point
    ##print("Is the start a goal?", problem.isGoalState(problem.getStartState()))##Let me check the test
    ##print("Start's successors:", problem.getSuccessors(problem.getStartState()))##Let me know what I should do about stack (chilenode, direction, step)
    my_Queue = util.Queue()
    my_Queue.push([problem.getStartState(),0,[]]) ###[state,cost,path]
    expanded = set()
    while my_Queue.isEmpty() == False:
        [current_state,current_cost,current_path] = my_Queue.pop()
        if problem.isGoalState(current_state):
            return current_path
        if current_state not in expanded:
            expanded.add(current_state)
            for childstate,direction,cost in problem.getSuccessors(current_state): ##direction thatis action
                newpath = current_path+[direction]                            ##this is two list + become a new list in nature
                newcost = current_cost + cost
                my_Queue.push([childstate,newcost,newpath])


def uniformCostSearch(problem: SearchProblem): ##for the data structure we have, namely priority queue is a min heap top. AND THE main parameter is the min cost!!
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    ##print("Start:", problem.getStartState()) ##Let me know what is the starter point
    ##print("Is the start a goal?", problem.isGoalState(problem.getStartState()))##Let me check the test
    ##print("Start's successors:", problem.getSuccessors(problem.getStartState()))##Let me know what I should do about stack (chilenode, direction, step)
    my_PQueue = util.PriorityQueue()
    my_PQueue.push([problem.getStartState(),0,[]],0) ###[state,cost,path]
    expanded = set()
    while my_PQueue.isEmpty() == False:
        [current_state,current_cost,current_path] = my_PQueue.pop()
        if problem.isGoalState(current_state):
            return current_path
        if current_state not in expanded:
            expanded.add(current_state)
            for childstate,direction,cost in problem.getSuccessors(current_state): ##direction thatis action
                newpath = current_path+[direction]                            ##this is two list + become a new list in nature
                newcost = current_cost + cost
                my_PQueue.push([childstate,newcost,newpath],newcost)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ##print("Start:", problem.getStartState()) ##Let me know what is the starter point
   ## print("Is the start a goal?", problem.isGoalState(problem.getStartState()))##Let me check the test
    ##print("Start's successors:", problem.getSuccessors(problem.getStartState()))##Let me know what I should do about stack (chilenode, direction, step)
    expanded = set()
    my_PQueue = util.PriorityQueue()
    current_state = problem.getStartState()
    my_PQueue.push([current_state,0,[]],heuristic(current_state,problem)) ###[state,cost,path] 
    while my_PQueue.isEmpty() == False:
        [current_state,current_cost,current_path] = my_PQueue.pop()
        if problem.isGoalState(current_state):
            return current_path
        if current_state not in expanded:
            expanded.add(current_state)
            for childstate,direction,cost in problem.getSuccessors(current_state): ##direction thatis action
                newpath = current_path+[direction]                            ##this is two list + become a new list in nature
                newcost = current_cost + cost
                my_PQueue.push([childstate,newcost,newpath],heuristic(childstate,problem)+newcost)   ##That is the def of A*, the min c+h
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
