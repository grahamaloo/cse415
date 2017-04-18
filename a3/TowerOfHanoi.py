'''TowerOfHanoi.py
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
PROBLEM_NAME = "Towers of Hanoi"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "11-APR-2017"
PROBLEM_DESC=\
'''This formulation of the Tower of Hanoi problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface, Version 0.2.
'''
#</METADATA>

#<COMMON_CODE>

def can_move(s,From,To):
  '''Tests whether it's legal to move a disk in state s
     from the From peg to the To peg.'''
  try:
   pf=s.d[From] # peg disk goes from
   pt=s.d[To]   # peg disk goes to
   if pf==[]: return False  # no disk to move.
   df=pf[-1]  # get topmost disk at From peg..
   if pt==[]: return True # no disk to worry about at To peg.
   dt=pt[-1]  # get topmost disk at To peg.
   if df<dt: return True # Disk is smaller than one it goes on.
   return False # Disk too big for one it goes on.
  except (Exception) as e:
   print(e)

def move(s,From,To):
  '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the topmost disk
     from the From peg to the To peg.'''
  news = s.__copy__() # start with a deep copy.
  d2 = news.d # grab the new state's dictionary.
  pf=d2[From] # peg disk goes from.
  df=pf[-1]  # the disk to move.
  d2[From]=pf[:-1] # remove it from its old peg.
  d2[To]+=[df] # Put disk onto destination peg.
  return news # return new state

def goal_test(s):
  '''If the first two pegs are empty, then s is a goal state.'''
  return s.d['peg1']==[] and s.d['peg2']==[]

def goal_message(s):
  return "The Tower Transport is Triumphant!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

def h_hamming3(state):
  "Counts the number of disks NOT at the destination peg."
  p3 = state.d['peg3']
  return NDISKS - len(p3)

def h_weighted_hamming(state):
  "Computes a weighted sum of the number of disks NOT at the destination peg."
  p3 = state.d['peg3']
  sum = 0
  for n in range(1,NDISKS+1):
    if not (n in p3): sum += n
  return sum
#</COMMON_CODE>

#<COMMON_DATA>
N_disks = 4
#</COMMON_DATA>

#<STATE>
class State():
  def __init__(self, d):
    self.d = d

  def __str__(self):
    # Produces a brief textual description of a state.
    d = self.d
    txt = "["
    for i, peg in enumerate(['peg1','peg2','peg3']):
      txt += str(d[peg])
      if i<2: txt += ","
    return txt+"]"

  def __eq__(self, s2):
    if not (type(self)==type(s2)): return False
    d1 = self.d; d2 = s2.d
    return d1['peg1']==d2['peg1'] and d1['peg2']==d2['peg2'] and d1['peg3']==d2['peg3']

  def __hash__(self):
    return (str(self)).__hash__()

  def __copy__(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    for peg in ['peg1', 'peg2', 'peg3']:
      news.d[peg]=self.d[peg][:]
    return news
#</STATE>

#<INITIAL_STATE>
INITIAL_STATE = State({'peg1': list(range(N_disks,0,-1)), 'peg2':[], 'peg3':[] })
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>

#<OPERATORS>
peg_combinations = [('peg'+str(a),'peg'+str(b)) for (a,b) in
                    [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]]
OPERATORS = [Operator("Move disk from "+p+" to "+q,
                      lambda s,p1=p,q1=q: can_move(s,p1,q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p1=p,q1=q: move(s,p1,q1) )
             for (p,q) in peg_combinations]
#</OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<HEURISTICS> (optional)
HEURISTICS = {'h_hamming3': h_hamming3, 'h_weighted_hamming':h_weighted_hamming}
#</HEURISTICS>
