'''Grid.py
Create the Grid World MDP used in many of the Berkeley lectures.

Also run a test consisting of one episode of random exploration
in this world, receiving the rewards along the way.

S. Tanimoto, May 14, 2016.


CSE 415 Students: DO NOT MODIFY THIS FILE, AND DO NOT TURN IT IN.

'''

ACTIONS = ['North', 'South', 'East', 'West', 'End']
# Note that an action is NOT the same thing as an operator, because
# in an MDP, the action indicates only an intended operator, and
# the actual operator that is used is random, according to the
# probability in the transition table.

INITIAL_STATE = (0,0)

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

NorthOp = Operator("Move North if Possible",\
                   lambda s: can_move(s, 0,1),\
                   lambda s: move(s, 0,1))

SouthOp = Operator("Move South if Possible",\
                   lambda s: can_move(s, 0,-1),\
                   lambda s: move(s, 0,-1))

WestOp  = Operator("Move West if Possible",\
                   lambda s: can_move(s, -1, 0),\
                   lambda s: move(s, -1, 0))

EastOp  = Operator("Move East if Possible",\
                   lambda s: can_move(s, 1, 0),\
                   lambda s: move(s, 1, 0))

EndOp  = Operator("Go to the DEAD state",\
                   lambda s: s==(3,2) or s==(3,1),\
                   lambda s: "DEAD")

OPERATORS = [NorthOp, SouthOp, WestOp, EastOp, EndOp]

# The following dictionary maps each action (except the End action)
# to the three operators that might be randomly chosen to perform it.
# In this MDP, the first gets probability P_normal, and the other two
# each get probability P_noise.

ActionOps = {'North': [NorthOp, WestOp, EastOp],
             'South': [SouthOp, EastOp, WestOp],
             'East':  [EastOp, SouthOp, NorthOp],
             'West':  [WestOp, NorthOp, SouthOp]}

# Here's the helper function for defining operator preconditions:
# Updated as per suggestion from Tyler Williamson
def can_move(s, dx, dy):
    if s=="DEAD" or s in [(3,2), (3,1)]: return False
    x, y = s
    if x+dx < 0 or x+dx > 3: return False
    if y+dy < 0 or y+dy > 2: return False
    if x+dx==1 and y+dy==1: return False # Can't move into the rock.
    return True

# Here's the corresponding helper function for defining operator
# state transition functions:
def move(s, dx, dy):
    x, y = s
    return (x+dx, y+dy)

P_normal = 0.8   # As used in the example by Dan Klein and Pieter Abbeel.
P_noise  = 0.1

def T(s, a, sp):
    '''Compute the transition probability for going from state s to
       state sp after taking action a.  This could have been implemented
       using a big dictionary, but this looks more easily generalizable
       to larger grid worlds.'''
    if s=="DEAD": return 0
    if sp=="DEAD":
      if s==(3,2) or s==(3,1): return 1
    sx, sy = s
    spx, spy = sp
    if sx==spx and sy == spy-1:
        if a=="North": return P_normal
        if a=="East" or a=="West": return P_noise
    if sx==spx and sy == spy+1:
        if a=="South": return P_normal
        if a=="East" or a=="West": return P_noise
    if sx==spx-1 and sy == spy:
        if a=="East": return P_normal
        if a=="North" or a=="South": return P_noise
    if sx==spx+1 and sy == spy:
        if a=="West": return P_normal
        if a=="North" or a=="South": return P_noise
    if s==sp:  # This means precondition was not satisfied, in most problem formulations.#
        # Go through the 3 relevant operators in order of highest-probability first, and
        # total up the probabilities of those whose preconditions were not satisfied.
        ops = ActionOps[a]
        prob = 0.0
        if not ops[0].is_applicable(s): prob += P_normal
        if not ops[1].is_applicable(s): prob += P_noise
        if not ops[2].is_applicable(s): prob += P_noise
        return prob
    return 0.0 # Default case is probability 0.

def R(s, a, sp):
    '''Return the reward associated with transitioning from s to sp via action a.'''
    if s=='DEAD': return 0
    if s==(3,2): return 1.0  # the Gem
    if s==(3,1): return -1.0 # the Pit
    return -0.01   # cost of living.

                  