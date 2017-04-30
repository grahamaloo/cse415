'''William Menten-Weil wtmenten
CSE 415, Spring 2017, University of Washington
Instructor:  S. Tanimoto.
Assignment 3 Part II.  3. A*
'''
# Astar.py, April 2017
# Based on ItrDFS.py, Ver 0.3, April 11, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan puzzle10a

import sys
from queue import PriorityQueue

# DO NOT CHANGE THIS SECTION
if sys.argv==[''] or len(sys.argv)<3:
    import EndPoverty as Problem
    heuristics = lambda s: Problem.HEURISTICS['h_hamming'](s)
    initial_state = Problem.CREATE_INITIAL_STATE()

else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)
    initial_state = Problem.State(importlib.import_module(sys.argv[3]).CREATE_INITIAL_STATE())



print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

# DO NOT CHANGE THIS SECTION
def runAStar():
    #initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    # initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT)+" states examined.")
    return path, name

from itertools import count
# A star search algorithm
# TODO: finish A star implementation
def AStar(initial_state):
    counter = count() # this breaks pq ties
    global COUNT, BACKLINKS
    # TODO: initialze and put first state into
    # priority queue with respective priority
    # add any auxiliary data structures as needed
    OPEN = PriorityQueue()
    CLOSED = []
    OPEN.put((0, next(counter), initial_state))
    BACKLINKS[initial_state] = -1


    while not OPEN.empty():
        COUNT += 1
        S = OPEN.get()
        while S[2] in CLOSED:
            S = OPEN.get()
        cost = S[0]
        S = S[2]
        CLOSED.append(S)
        if COUNT % 100:
            sys.stdout.write('.')
            sys.stdout.flush()

        # DO NOT CHANGE THIS SECTION: begining
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
        # DO NOT CHANGE THIS SECTION: end

        # TODO: finish A* implementation
        for op in Problem.OPERATORS:

          #Optionally uncomment the following when debugging
          #a new problem formulation.
          # print("Trying operator: "+op.name)
          if op.precond(S):
            new_state = op.state_transf(S)
            if not (new_state in CLOSED):
                h = heuristics(new_state)
                # h += cost
                new_pq_item = (h, next(counter), new_state)
                OPEN.put(new_pq_item)
                BACKLINKS[new_state] = S



# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    print("\nPath length = "+str(len(path)-1))
    return path

if __name__=='__main__':
    path, name = runAStar()

