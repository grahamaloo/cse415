'''William Menten-Weil wtmenten & Graham Kelly grahamtk
CSE 415, Spring 2017, University of Washington
Instructor:  S. Tanimoto.
Assignment 4
'''
'''EndPoverty.py
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
PROBLEM_NAME = "EndPoverty"
PROBLEM_VERSION = "1"
PROBLEM_AUTHORS = ['W. Menten-Weil', 'G. Kelly']
PROBLEM_CREATION_DATE = "26-APR-2017"
PROBLEM_DESC=\
'''This formulation of the End Poverty problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface, Version 1.
'''
#</METADATA>
import copy
import math
import itertools
import statistics
import random

#<COMMON_DATA>
POVERTY_LEVEL = 35000
MIN_WAGE = 7000
WAGE_SPREAD = 75000
INITIAL_POP_SIZE = 1000
INFLATION = 0.018
MAX_TAX = .55
MIN_TAX = .05
TAX_RET_RATE = .25
growth_dynamic = .01
growth_const = 0.02
#</COMMON_DATA>

#<COMMON_CODE>

def can_adj_tax(s,i,delta):
  '''Tests whether it's legal to
    adjust the tax in state = s
    for bracket index = i
    by value = delta'''
  b_value_index = 1
  proposed_tax = s.b[i][b_value_index] + delta

  if proposed_tax > MAX_TAX or proposed_tax < MIN_TAX:
    return False # tax rate cannot fall below 0

  # now test if shifting by delta will invalidate the order of the brackets
  target_b = s.b[i][b_value_index] + delta
  if i == 0:
    post_b = s.b[i+1][b_value_index]
    return target_b < post_b
  elif i == len(s.b) - 1:
    prev_b = s.b[i-1][b_value_index]
    return prev_b < target_b
  else:
    prev_b = s.b[i-1][b_value_index]
    post_b = s.b[i+1][b_value_index]
    return prev_b < target_b < post_b

def can_adj_cutoff(s,i,delta):
  '''Tests whether it's legal to
    adjust the cuttoff in state = s
    for bracket index = i
    by value = delta'''
  b_value_index = 0
  if s.b[i][b_value_index] + delta <= 0 or i == len(s.b)-1 or i == 0:
    return False # cutoff cannot fall below 0

  target_b = s.b[i][b_value_index] + delta

  if i == 0:
    post_b = s.b[i+1][b_value_index]
    return target_b < post_b
  elif i == len(s.b) - 1:
    prev_b = s.b[i-1][b_value_index]
    # return prev_b < target_b
    return False # last tax brackets cutoff must be +inf
  else:
    prev_b = s.b[i-1][b_value_index]
    post_b = s.b[i+1][b_value_index]
    return prev_b < target_b < post_b

def adj_tax(s, i, delta):
  new_s = s.__copy__()
  new_s.b[i][1] += delta
  return advance(new_s)

def adj_cutoff(s, i, delta):
  new_s = s.__copy__()
  new_s.b[i][0] += delta
  return advance(new_s)

# progresses a year in the state
def advance(s):
  s = grow_wages(s)
  return s

def grow_wages(s):
  avg_wage = sum(s.p) / float(len(s.p))
  std = statistics.stdev(s.p)
  std_dist = lambda w, avg=avg_wage, std=std : abs((w - avg) / std)
  s.p = [ w * (1 + growth_func(std_dist(w)) + INFLATION) for w in s.p]
  return s

def growth_func(x):

  sigmoid_value = 1/(1+math.e**(-x/2))
  framed = ( sigmoid_value * growth_dynamic) + growth_const
  return framed

def goal_test(s):
  # test if everyone is above poverty level after tax and tax return
  temp_s = s.__copy__()
  taxes = 0
  for i, p in enumerate(temp_s.p):
    unfound = True
    current_bracket = 0
    while unfound:
      cut, rate = temp_s.b[current_bracket]
      if p <= cut:
        taxes += p * rate
        temp_s.p[i] *= (1 -  rate)
        unfound = False
      else:
        current_bracket += 1
  per_p_subsidy = taxes * TAX_RET_RATE / len(temp_s.p)
  for i, p in enumerate(s.p):
      temp_s.p[i] += per_p_subsidy
  
  return all(p >= POVERTY_LEVEL for p in temp_s.p)

def goal_message(s):
  return "Poverty has ended!"

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
  "Counts the number of people below the poverty line."
  count = 0
  for i,p in enumerate(state.p):
    if p < POVERTY_LEVEL: count += 1

  return count + bracket_tax_dif(state) * 100

def bracket_tax_dif(s):
  b_val_idx = 1
  difs = []
  for i in range(len(s.b)-1):
    difs.append((s.b[i+1][b_val_idx] - s.b[i][b_val_idx]))
  avg_dif = sum(difs) / float(len(difs))
  return avg_dif

def h_avg(state):
  "returns average distance below the poverty line for those below poverty line."
  avg = 0
  for i,p in enumerate(state.p):
    if p < POVERTY_LEVEL: avg += POVERTY_LEVEL - p
  avg = avg / len(state.p)

  return avg + bracket_tax_dif(state) * 100
#</COMMON_CODE>

#<STATE>
class State():
  def __init__(self, p, b):
    self.p = p
    self.b = b

  def __str__(self):
    # Produces a brief textual description of a state.
    return "People: %s\nTax Brackets: %s" % (self.p, self.b)

  def __eq__(self, s2):
    if not (type(self)==type(s2)): return False
    pop1, tax1 = self.p, self.b; pop2, tax2 = s2.p, s2.b
    return pop1 == pop2 and tax1 == tax2

  def __hash__(self):
    return (str(self)).__hash__()

  def __copy__(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State([],[])
    news.p, news.b = [t for t in self.p], [copy.copy(t) for t in self.b]
    return news
#</STATE>

#<INITIAL_STATE>
random.seed()
def generate_initial_state(pop_size=INITIAL_POP_SIZE):
  pop = sorted([random.weibullvariate(0.85, 1.5) * WAGE_SPREAD + MIN_WAGE for x in range(pop_size)])
  return pop

INITAL_POPULATION = generate_initial_state()
INITAL_TAX_BRACKETS = [[11000, .0], [25000, .6], [35000, .9], [50000, .12], [75000, .15], [100000, .16], [math.inf, .17]]
INITIAL_STATE = State(
    INITAL_POPULATION,
    INITAL_TAX_BRACKETS
  )
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>

#<OPERATORS>
tax_deltas = [ 0.01,]
cutoff_deltas = [1000,]
directions = [-1, 1]

OPERATORS = [
  [
    Operator("Change cutoff by %.2f for bracket %s" % (delta * direction, i), lambda s, i=i, delta=delta, direction=direction: can_adj_cutoff(s, i, delta * direction), lambda s, i=i, delta=delta, direction=direction: adj_cutoff(s,i, delta * direction))
    for delta,direction,i in itertools.product(cutoff_deltas, directions, range(len(INITAL_TAX_BRACKETS)))
  ],
  [
    Operator("Change tax rate by %.2f for bracket %s" % (delta * direction, i), lambda s, i=i, delta=delta, direction=direction: can_adj_tax(s, i, delta * direction), lambda s, i=i, delta=delta, direction=direction: adj_tax(s,i, delta * direction))
    for delta,direction,i in itertools.product(tax_deltas, directions, range(len(INITAL_TAX_BRACKETS)))
  ],
]
OPERATORS = list(itertools.chain(*OPERATORS))
#</OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<HEURISTICS> (optional)
HEURISTICS = {'h_hamming': h_hamming, 'h_avg': h_avg}
#</HEURISTICS>
