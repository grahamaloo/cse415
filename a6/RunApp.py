'''RunApp.py

This program imports Grid.py and MDP.py and runs certain algorithms to
demonstrate aspects of reinforcement learning.

CSE 415  Students: Fill in the missing code where indicated.
modified by GRAHAM KELLY grahamtk 5/22/2017
'''

import MDP, Grid, TowersOfHumptulips as Towers

def GW_Values_string(V_dict):
    out = '\nVALUES ITER RESULT:\n'
    rows = [2, 1, 0]
    cols = [0, 1, 2, 3]
    for r in rows:
        for c in cols:
            state = (c,r)
            value = V_dict[state]
            cell = "  %04.3f " % value if value >= 0 else " %04.3f " % value
            # if V_dict[state] >= 0:
            #     formatted = " "+formatted
            out += cell
        out += '\n'
    return out

def get_single_value(d, key):
    value = "%04.3f" % d[key]
    if d[key] >= 0:
        value = " " + value
    return value

def GW_QValues_string(Q_dict):
    out = 'Q LEARNING RESULT:'
    small_gap = ' '
    gap = small_gap * 4
    rows = [2, 1, 0]
    cols = [0, 1, 2, 3]

    for r in rows:
        out += '\n'
        for c in cols:
            out += gap
            state = (c,r)
            state = (state, 'North')
            out += get_single_value(Q_dict,state)
            out += gap
        out += '\n'

        for c in cols:
            state = (c,r)
            state = (state, 'West')
            out += get_single_value(Q_dict,state)
            out += small_gap
            state = (c,r)
            state = (state, 'East')
            out += get_single_value(Q_dict,state)
            out += small_gap
        out += '\n'

        for c in cols:
            out += gap
            state = (c,r)
            state = (state, 'South')
            out += get_single_value(Q_dict,state)
            out += gap
        out += '\n'
    return out

def GW_Policystring(policy):
    out = 'OPT POLICY\n'
    rows = [2, 1, 0]
    cols = [0, 1, 2, 3]
    for r in rows:
        for c in cols:
            state = (c,r)
            cell = str(policy[state]) if state in policy else 'NONE'
            while len(cell) < 7:
                cell += ' '
            out += cell
        out += '\n'
    return out

def TH_Values_string(V_dict):
    out = 'VALUES ITER RESULT:\n'
    keys = sorted([k for k in V_dict.keys() if k != 'DEAD'])

    for k in keys:
        out += str(k) + ' : ' + str(V_dict[k]) + '\n'
    out += 'DEAD : ' + str(V_dict['DEAD']) + '\n'
    return out

def TH_QValues_string(Q_dict):
    out = 'Q LEARNING RESULT:\n'
    keys = sorted([k for k in Q_dict.keys() if k[0] != 'DEAD'])
    dead_keys = sorted([k for k in Q_dict.keys() if k[0] == 'DEAD'])
    for k in keys:
        out += str(k) + ' : ' + str(Q_dict[k]) + '\n'
    for k in dead_keys:
        out += str(k) + ' : ' + str(Q_dict[k]) + '\n'
    return out

def TH_Policystring(policy):
    out = 'OPT POLICY\n'
    keys = sorted([k for k in policy.keys() if k != 'DEAD'])

    for k in keys:
        out += str(k) + ' : ' + str(policy[k]) + '\n'
    out += 'DEAD : ' + str(policy['DEAD']) + '\n'
    return out


def test():
    '''Create the MDP, then run an episode of random actions for 10 steps.'''
    grid_MDP = MDP.MDP()
    grid_MDP.register_start_state((0,0))
    grid_MDP.register_actions(Grid.ACTIONS)
    grid_MDP.register_operators(Grid.OPERATORS)
    grid_MDP.register_transition_function(Grid.T)
    grid_MDP.register_reward_function(Grid.R)
    # grid_MDP.random_episode(100)

    # Uncomment the following, when you are ready...

    grid_MDP.valueIteration(0.6, 15)
    print(GW_Values_string(grid_MDP.V))

    grid_MDP.QLearning(0.6, 6000, 0.4)
    print(GW_QValues_string(grid_MDP.Q))

    policy = grid_MDP.extractPolicy()
    print(GW_Policystring(policy))

    towers_MDP = MDP.MDP()
    towers_MDP.register_start_state(Towers.INITIAL_STATE)
    towers_MDP.register_actions(Towers.ACTIONS)
    towers_MDP.register_operators(Towers.OPERATORS)
    towers_MDP.register_transition_function(Towers.T)
    towers_MDP.register_reward_function(Towers.R)

    towers_MDP.valueIteration(0.75, 100)
    print(TH_Values_string(towers_MDP.V))

    towers_MDP.QLearning(0.75, 6000, 0.4)
    print(TH_QValues_string(towers_MDP.Q))

    policy = towers_MDP.extractPolicy()
    print(TH_Policystring(policy))

    towers_MDP.follow_policy()


test()