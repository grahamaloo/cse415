'''RunApp.py

This program imports Grid.py and MDP.py and runs certain algorithms to
demonstrate aspects of reinforcement learning.

CSE 415  Students: Fill in the missing code where indicated.

'''

import MDP, Grid

def GW_Values_string(V_dict):
    # IMPLEMENT THIS
    pass

def GW_QValues_string(Q_dict):
    # IMPLEMENT THIS
    pass

def GW_Policy_string():
    # IMPLEMENT THIS
    pass


def test():
    '''Create the MDP, then run an episode of random actions for 10 steps.'''
    grid_MDP = MDP.MDP()
    grid_MDP.register_start_state((0,0))
    grid_MDP.register_actions(Grid.ACTIONS)
    grid_MDP.register_operators(Grid.OPERATORS)
    grid_MDP.register_transition_function(Grid.T)
    grid_MDP.register_reward_function(Grid.R)
    grid_MDP.random_episode(100)

    # Uncomment the following, when you are ready...

    # Grid_MDP.valueIteration( 0.5, 10)
    # print(GW_Values_string(Grid_MDP.V)

    # Grid_MDP.QLearning( 0.5, 50, 0.5)
    # print(GW_QValues_string(Grid_MDP.Q)

    # print(GW_Policystring())

test()