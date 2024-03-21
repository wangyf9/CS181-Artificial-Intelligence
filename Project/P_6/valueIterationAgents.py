# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):#travel all the iterations in order to update
            valuesCopy = self.values.copy() #values in the graph
            for state in self.mdp.getStates():#travel all the states in the mdp to update
                if self.mdp.isTerminal(state):
                    continue
                maxQValue = -10000000
                for action in self.mdp.getPossibleActions(state):
                    qValue = self.computeQValueFromValues(state, action)
                    if qValue > maxQValue: #choose the max action as the policy
                        maxQValue = qValue
                #update one point
                valuesCopy[state] = maxQValue
            #update the whole graph
            self.values = valuesCopy

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0
        #compute this concrete action's q value
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, nextState)
            #formula
            qValue += prob * (reward + self.discount * self.values[nextState])
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        maxQValue = -10000000
        bestAction = None
        #choose the best action as the value of the arc which actually is the policy
        for action in self.mdp.getPossibleActions(state):
            qValue = self.computeQValueFromValues(state, action)
            if qValue > maxQValue:
                maxQValue = qValue
                bestAction = action
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        grid_world = self.mdp.getStates()##Get all the state in the grid world
        cnt = 0
        for i in range(self.iterations):
            state = grid_world[cnt%len(grid_world)]##update one by one in order, in first iteration update the first state
            cnt += 1
            best_action = self.computeActionFromValues(state)
            if best_action:##if self.computeActionFromValues(state) return none that means it is the terminal state, finish
                self.values[state] = self.computeQValueFromValues(state, best_action)

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        adjacent_matrix = []
        #record the order
        index_recorder = util.Counter()
        # initialize a priority queue
        priority_queue = util.PriorityQueue()
        new_values = util.Counter() ##set a data structure to store the update value so that in next part we can use to update
        cnt = 0
        for state_1 in self.mdp.getStates():##travel all the states
            ##To record the predecessor
            index_recorder[state_1] = cnt
            cnt += 1
            adjacent_list = set()
            for state_2 in self.mdp.getStates():##travel again to find the predecessorss of this state
                for action in self.mdp.getPossibleActions(state_2):##travel all the actions
                    state_and_prob = self.mdp.getTransitionStatesAndProbs(state_2, action)
                    for next_state, prob in state_and_prob:
                        if next_state == state_1 and prob > 0:##determine whether taking this action will lead to the state_1
                            adjacent_list.add(state_2)
            adjacent_matrix.append(adjacent_list)
        # find diff of each s, store new value in new_values, push s, -diff
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):##terminal do nothing
                continue
            current_value = self.getValue(state)
            best_action = self.computeActionFromValues(state)
            if best_action:##calculate the newvalue and diff to push into the priority queue
                new_value = self.computeQValueFromValues(state, best_action)
                new_values[state] = new_value

                diff = abs(current_value - new_value)
                priority_queue.push(state, -diff)
            else:
                new_values[state] = current_value
        # do iterations
        for i in range(self.iterations): ##travel all the iteration
            # if p_queue is empty, terminate
            if priority_queue.isEmpty():#finish
                break
            state = priority_queue.pop()
            if not self.mdp.isTerminal(state):
                self.values[state] = new_values[state]
            # precess front's pred
            for adjacent_state in adjacent_matrix[index_recorder[state]]:
                current_value = self.getValue(adjacent_state)
                best_action = self.computeActionFromValues(adjacent_state)
                if best_action:#update
                    new_value = self.computeQValueFromValues(adjacent_state, best_action)
                    diff = abs(current_value - new_value)
                    new_values[adjacent_state] = new_value
                    if diff > self.theta: ##diff > theta will allow to update
                        priority_queue.update(adjacent_state, -diff)

