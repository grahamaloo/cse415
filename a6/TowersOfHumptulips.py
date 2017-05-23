'''TowersOfHumptulips.py

Graham Kelly, May 22, 2016.

Tower of Humptulips problem as defined by S. Tanimoto
EC
'''

ACTIONS = ['A1-2', 'A1-3', 'A2-1', 'A2-3', 'A3-1', 'A3-2', 'End']
# Note that an action is NOT the same thing as an operator, because
# in an MDP, the action indicates only an intended operator, and
# the actual operator that is used is random, according to the
# probability in the transition table.

INITIAL_STATE = ((4,3,2,1),(),())

# Operators are the actual state-space search operators as used
# in classical algorithms such as A* search.

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


A12Op = Operator("Move Disk From Peg 1 to Peg 2 if Possible",\
                   lambda s: can_move(s, 0,1),\
                   lambda s: move(s, 0,1))

A13Op = Operator("Move Disk From Peg 1 to Peg 3 if Possible",\
                   lambda s: can_move(s, 0,2),\
                   lambda s: move(s, 0,2))

A21Op  = Operator("Move Disk From Peg 2 to Peg 1 if Possible",\
                   lambda s: can_move(s, 1, 0),\
                   lambda s: move(s, 1, 0))

A23Op  = Operator("Move Disk From Peg 2 to Peg 3 if Possible",\
                   lambda s: can_move(s, 1, 2),\
                   lambda s: move(s, 1, 2))

A31Op  = Operator("Move Disk From Peg 3 to Peg 1 if Possible",\
                   lambda s: can_move(s, 2, 0),\
                   lambda s: move(s, 2, 0))

A32Op  = Operator("Move Disk From Peg 3 to Peg 2 if Possible",\
                   lambda s: can_move(s, 2, 1),\
                   lambda s: move(s, 2, 1))

EndOp  = Operator("Go to the DEAD state",\
                   lambda s: s==((),(),(4,3,2,1)),\
                   lambda s: "DEAD")

OPERATORS = [A12Op, A13Op, A21Op, A23Op, A31Op, A32Op, EndOp]

# The following dictionary maps each action (except the End action)
# to the three operators that might be randomly chosen to perform it.
# In this MDP, the first gets probability P_normal, and the other two
# each get probability P_noise.

ActionOps = {'A1-2': A12Op, 'A1-3': A13Op, 'A2-1': A21Op, 'A2-3': A23Op, 'A3-1': A31Op, 'A3-2': A32Op}

# Here's the helper function for defining operator preconditions:
# Updated as per suggestion from Tyler Williamson
def can_move(s, p1, p2):
    if s == "DEAD": return False
    if not s[p1]: return False
    if s[p2] and s[p1][-1] > s[p2][-1]: return False
    return True

# Here's the corresponding helper function for defining operator
# state transition functions:
import itertools
def move(s, p1, p2):
    ns = [x for x in s]
    ns[p2] = tuple([x for x in itertools.chain(ns[p2], [ns[p1][-1]])])
    ns[p1] = tuple([x for x in ns[p1][:-1]])
    return tuple(ns)

P_normal = 0.8   # As used in the example by Dan Klein and Pieter Abbeel.
P_noise  = 0.1
GoalState = ((),(),(4,3,2,1))

def T(s, a, sp):
    '''Compute the transition probability for going from state s to
       state sp after taking action a.  This could have been implemented
       using a big dictionary, but this looks more easily generalizable
       to larger grid worlds.'''
    if s=="DEAD": return 0
    if sp=="DEAD":
        if s == GoalState and a == "End": return 1
        else: return 0
    if a=="End": return 0
    if s==GoalState and a!= "End": return 0

    op = ActionOps[a]
    if op.is_applicable(s) and sp == op.apply(s): return 1
    return 0.0 # Default case is probability 0.

BadStates = [ ((4,1),(2,),(3,)), ((4,1),(3,),(2,)),
              ((2,),(4,1),(3,)), ((3,),(4,1),(2,)),
              ((2,),(3,),(4,1)), ((3,),(2,),(4,1)) ]

DiskCosts = {'0': 0, '1': -1, '2': -2, '3': -4, '4': -8}

def _get_moved_disk(s1, s2):
    '''gets the moved disk between two ADJACENT, VIABLE states in problem'''
    for p1, p2 in zip(s1, s2):
        if p1 != p2:
            # print(p1, p2, p1[-1] if p1 else None, str(p1[-1]) if p1 else None, p2[-1] if p2 else None, str(p2[-1]) if p2 else None)
            return str(p1[-1]) if len(p1) > len(p2) else str(p2[-1])
    return '0'

def R(s, a, sp):
    '''Return the reward associated with transitioning from s to sp via action a.'''
    if s == 'DEAD': return 0
    if s == GoalState:
        if a != 'End': return -1
        else: return 0
    state_cost = 0
    if sp in BadStates: state_cost += -50
    if sp == GoalState: state_cost += 1000
    if sp == 'DEAD': return state_cost
    elif a == 'End': return -1 # penalize end when it's not possible

    
    disk_cost = DiskCosts[_get_moved_disk(s, sp)]
    return state_cost + disk_cost