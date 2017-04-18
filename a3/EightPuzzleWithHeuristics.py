'''Graham Kelly (grahamtk)
CSE 415 Assignment 3: Part II
'''
'''EightPuzzleWithHeuristics.py
A QUIET Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this 
problem formulation.  

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''
#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Eight Puzzle w/ Heuristics"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Graham Kelly']
PROBLEM_CREATION_DATE = "19-APR-2017"
PROBLEM_DESC=\
'''This formulation of the Basic Eight problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET tools interface, Version 0.2.
Includes heuristics to facilitate A* search.
'''
#</METADATA>

#<COMMON_CODE>
def can_move(s,From,To):
    '''Tests whether it's legal to move a tile in state s
    from the From place to the To slot.'''
    try:
        possible = Final_state
        if From == To : return False # can't move tile from current space to current space.
        if s.d[From] == 0 or s.d[To] != 0: return False # have to move tile from occupied space to empty one (zero = empty).
        if From not in possible or To not in possible: return False # indices have to be valid.
        dx = abs(get_x(From) - get_x(To)) # delta x
        dy = abs(get_y(From) - get_y(To)) # delta y
        if dx == 1 and dy == 0: return True # adjacent row, same col
        if dy == 1 and dx == 0: return True # adjacent col, same row
        return False # all other possibilities = not movable
    except (Exception) as e:
        print(e)

def get_x(c):
    '''return x coord of passed index in 8 puzzle'''
    return c % 3 

def get_y(c):
    '''return y coord of passed index in 8 puzzle'''
    return int(c / 3)

def move(s,From,To):
    '''Assuming it's legal to make the move, this computes
    the new state resulting from moving the specified tile 
    from From spot to the To spot.'''
    news = s.__copy__() # start with a deep copy.
    d2 = news.d # grab the new state's list.
    d2[To] = d2[From]
    d2[From] = 0
    return news # return new state

def goal_test(s):
    '''if the orders match, then the puzzle is solved'''
    return s.d == Final_state

def goal_message(s):
    return "Successfully solved Basic Eight Puzzle."

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

def h_hamming(state):
    '''Counts the number of tiles out of place'''
    count = 0
    for a, t in zip(state.d, Final_state):
        if a != t:
            count += 1
    return count

from math import sqrt
def h_euclidean(state):
    '''calculates the euclidean distance from each out
    of place tile to its goal position.'''
    distance = 0
    for coord, val in enumerate(state.d):
        coord_ideal = Final_state.index(val)
        distance += sqrt( (get_x(coord) - get_x(coord_ideal))**2 + (get_y(coord) - get_y(coord_ideal))**2 )
    return distance

def h_manhattan(state):
    '''calculates the manhattan distance from each out
    of place tile to its goal position.'''
    distance = 0
    for coord, val in enumerate(state.d):
        coord_ideal = Final_state.index(val)
        distance += abs(get_x(coord) - get_x(coord_ideal)) + abs(get_y(coord) - get_y(coord_ideal))
    return distance

def h_custom(state):
    '''calculates the weighted avg. distance from each out
    of place tile to its goal position. (using other heuristics)'''
    distance = 0
    distance += h_hamming(state) + 4 * h_manhattan(state) + 2 * h_euclidean(state)
    return distance / 7
#</COMMON_CODE>

#<COMMON_DATA>
Final_state = [0, 1, 2, 3, 4, 5, 6, 7, 8] # goal state
#</COMMON_DATA>

#<STATE>
class State():
    def __init__(self, d):
        self.d = d

    def __str__(self):
        # Produces a brief textual description of a state.
        d = self.d
        txt = '[%s, %s, %s,\n %s, %s, %s,\n %s, %s, %s]' % (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
        return txt

    def __eq__(self, s2):
        # tests equality between states
        if not (type(self)==type(s2)): return False
        d1 = self.d
        d2 = s2.d
        return d1==d2

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State([])
        news.d = [n for n in self.d]
        return news
#</STATE>

#<INITIAL_STATE>
# puzzle0:
# INITIAL_STATE = State([1, 0, 2, 3, 4, 5, 6, 7, 8])
# puzzle1a:
# INITIAL_STATE = State([1, 0, 2, 3, 4, 5, 6, 7, 8])
# # puzzle2a:
# INITIAL_STATE = State([3, 1, 2, 4, 0, 5, 6, 7, 8])
# # puzzle4a:
# INITIAL_STATE = State([1, 4, 2, 3, 7, 0, 6, 8, 5])
# puzzle10a.py:
# INITIAL_STATE = State([4, 5, 0, 1, 2, 3, 6, 7, 8])
# puzzle12a.py:
# INITIAL_STATE = State([3, 1, 2, 6, 8, 7, 5, 4, 0])
# puzzle14a.py:
# INITIAL_STATE = State([4, 5, 0, 1, 2, 8, 3, 7, 6])
# puzzle16a.py:
INITIAL_STATE = State([0, 8, 2, 1, 7, 4, 3, 6, 5])

CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>

#<OPERATORS>
from itertools import product
tiles = product(range(9), range(9))
OPERATORS = [Operator("Move tile from "+ str(p)+" to "+str(q),
                      lambda s,p1=p,q1=q: can_move(s,p1,q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p1=p,q1=q: move(s,p1,q1))
             for (p,q) in tiles]
#</OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<HEURISTICS> (optional)
HEURISTICS = {'h_hamming': h_hamming, 'h_euclidean': h_euclidean, 'h_manhattan' : h_manhattan, 'h_custom': h_custom}
#</HEURISTICS>
