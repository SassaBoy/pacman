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
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

         # Value iteration algorithm
        for i in range(iterations):
        # Make a copy of the current values to use in the updates
          new_values = self.values.copy()
        
        # For each state in the MDP, calculate its new value using the Bellman update
          for state in self.mdp.getStates():
             if not self.mdp.isTerminal(state):
                # Initialize the value of this state to be negative infinity
                new_value = float("-inf")
                
                # For each action available from this state, calculate the expected value
                for action in self.mdp.getPossibleActions(state):
                    # Calculate the expected value of taking this action
                    value = 0
                    for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        reward = self.mdp.getReward(state, action, next_state)
                        value += prob * (reward + self.discount * self.values[next_state])
                    
                    # Update the new value to be the maximum of all the expected values
                    new_value = max(new_value, value)
                
                # Set the new value for this state
                new_values[state] = new_value
        
        # Update the values with the new values for the next iteration
          self.values = new_values
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
        qValue = 0.0
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        # Iterate over possible next states and their probabilities
        for nextState, prob in transitions:
          # Get the reward for transitioning to the next state from the current state with the given action
          reward = self.mdp.getReward(state, action, nextState)
              # Get the value of the next state
          value = self.values[nextState]
          qValue += prob * (reward + self.discount * value)
          #return the qValue
        return qValue
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
        if self.mdp.isTerminal(state):
            return None

        best_action = None
        best_value = float("-inf")

    # Iterate over all possible actions
        for action in self.mdp.getPossibleActions(state):
        # Compute the Q-value of this action
           q_value = self.computeQValueFromValues(state, action)

        # If this action has a higher Q-value than the current best action, update the best action
           if q_value > best_value:
             best_action = action
             best_value = q_value

        return best_action
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
