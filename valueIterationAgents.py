

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
              pi(s) = computeActionFromValues(self,state)
              sum[s',r] P(s',r|s,a)*[r+gamma*V(s)] = computeQValueFromValues(self, s, a)
              V(s) = self.values[s]
              r = mdp.GetReward(s, a, s')
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations #number of iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = mdp.getStates()
        for iteration in range(self.iterations):
            #print("inisde interation loop ", self.values)
            update = util.Counter()
            for state in states:
                #print("inisde state loop ", self.values)
                if(mdp.isTerminal(state)):
                    update[state] = 0
                else:
                    maxSum = float("-inf")
                    for action in mdp.getPossibleActions(state): #max
                        #print("inisde action loop ", self.values)
                        #maxReward = max(maxReward,
                        theSum = 0.0
                        for (nextState, nextProbability) in mdp.getTransitionStatesAndProbs(state, action): #sum
                            theSum += nextProbability*(mdp.getReward(state,action,nextState) + (self.discount*self.values[nextState]))
                            #print("inisde trans. and probs. loop", self.values)
                            #sum over probabilities*(mdp.getReward + (discount*self.values[state]))
                        maxSum = max(maxSum, theSum)
                        update[state] = maxSum
            self.values = update
           # print("last self.values ", self.values)            

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
        #print("in computeQValue ", self.values)
        #print("HELLO")
        
        #sum[s',r] P(s',r|s,a)*[r+gamma*V(s)] = computeQValueFromValues(self, s, a)
        #self.discount = discount
        theSum = 0.0
        for (nextState, nextProbability) in self.mdp.getTransitionStatesAndProbs(state, action): #sum
            theSum += nextProbability*(self.mdp.getReward(state,action,nextState) + (self.discount*self.values[nextState]))
        return theSum
        #print("in computeQValue ", self.values)
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #pi(s) = computeActionFromValues(self,state)
        bestAction = None
        maxValue = float("-inf")
        for action in self.mdp.getPossibleActions(state):
            currentValue = self.computeQValueFromValues(state, action)
            if(currentValue > maxValue):
                maxValue = currentValue
                bestAction = action
        return bestAction
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
