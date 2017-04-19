'''Graham Kelly (grahamtk)
CSE 415 Assignment 3: Part II
'''
# ItrDFS.py
# Ver 0.3, April 11, 2017.
# Iterative Depth-First Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET2" file format.
# See the TowersOfHanoi.py example file for details.
# Examples of Usage:
# python3 ItrDFS.py TowersOfHanoi
# python3 ItrDFS.py EightPuzzle

import sys

if sys.argv==[''] or len(sys.argv)<2:
  import EightPuzzle as Problem
  # import TowerOfHanoi as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])


print("\nWelcome to ItrDFS")
COUNT = None
BACKLINKS = {}

def runDFS():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  IterativeDFS(initial_state)
  print(str(COUNT)+" states examined.")

def IterativeDFS(initial_state):
  global COUNT, BACKLINKS

  OPEN = [initial_state]
  CLOSED = []
  BACKLINKS[initial_state] = -1

  while OPEN != []:
    S = OPEN[0]
    del OPEN[0]
    CLOSED.append(S)

    if Problem.GOAL_TEST(S):
      print("\n"+Problem.GOAL_MESSAGE_FUNCTION(S))
      backtrace(S)
      return

    COUNT += 1
    if (COUNT % 32)==0:
       print(".",end="")
       if (COUNT % 128)==0:
         print("COUNT = "+str(COUNT))
         print("len(OPEN)="+str(len(OPEN)))
         print("len(CLOSED)="+str(len(CLOSED)))
    L = []
    for op in Problem.OPERATORS:
      #Optionally uncomment the following when debugging
      #a new problem formulation.
      #print("Trying operator: "+op.name)
      if op.precond(S):
        new_state = op.state_transf(S)
        if not (new_state in OPEN) and not (new_state in CLOSED):
          L.append(new_state)
          BACKLINKS[new_state] = S
          #Uncomment for debugging:
          #print(new_state)

    OPEN = L + OPEN

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
  return path    
  
if __name__=='__main__':
  runDFS()

