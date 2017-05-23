'''MDP.py
S. Tanimoto, May 2016, 2017.

Provides representations for Markov Decision Processes, plus
functionality for running the transitions.

The transition function should be a function of three arguments:
T(s, a, sp), where s and sp are states and a is an action.
The reward function should also be a function of the three same
arguments.  However, its return value is not a probability but
a numeric reward value -- any real number.

operators:  state-space search objects consisting of a precondition
 and deterministic state-transformation function.
 We assume these are in the "QUIET" format used in earlier assignments.

actions:  objects (for us just Python strings) that are 
 stochastically mapped into operators at runtime according 
 to the Transition function.


CSE 415 STUDENTS: Implement the 3 methods indicated near the
end of this file.
modified by GRAHAM KELLY grahamtk 5/22/2017
'''
import random
from collections import defaultdict
import sys

REPORTING = True

class MDP:
    def __init__(self):
        self.known_states = set()
        self.succ = {} # hash of adjacency lists by state.
        self.fully_explored = False

    def register_start_state(self, start_state):
        self.start_state = start_state
        self.known_states.add(start_state)

    def register_actions(self, action_list):
        self.actions = action_list

    def register_operators(self, op_list):
        self.ops = op_list

    def register_transition_function(self, transition_function):
        self.T = transition_function

    def register_reward_function(self, reward_function):
        self.R = reward_function

    def state_neighbors(self, state):
        '''Return a list of the successors of state.  First check
           in the hash self.succ for these.  If there is no list for
           this state, then construct and save it.
           And then return the neighbors.'''
        neighbors = self.succ.get(state, False)
        if neighbors==False:
            neighbors = [op.apply(state) for op in self.ops if op.is_applicable(state)]
            self.succ[state]=neighbors
            self.known_states.update(neighbors)
        return neighbors

    def random_episode(self, nsteps):
        self.current_state = self.start_state
        self.known_states = set()
        self.known_states.add(self.current_state)
        self.current_reward = 0.0
        for i in range(nsteps):
            self.take_action(random.choice(self.actions))
            if self.current_state == 'DEAD':
                print('Terminating at DEAD state.')
                break
        if REPORTING: print("Done with "+str(i)+" of random exploration.")

    def take_action(self, a):
        s = self.current_state
        neighbors = self.state_neighbors(s)
        threshold = 0.0
        rnd = random.uniform(0.0, 1.0)
        r = self.R(s,a,s)
        for sp in neighbors:
            threshold += self.T(s, a, sp)
            if threshold>rnd:
                r = self.R(s, a, sp)
                s = sp
                break
        self.current_state = s
        self.known_states.add(self.current_state)
        if REPORTING: print("After action "+a+", moving to state "+str(self.current_state)+\
                            "; reward is "+str(r))

    def generateAllStates(self):
        self.known_states = set() # re init to empty set
        self.bfs(self.start_state)
        self.fully_explored = True

    def bfs(self, state):
        self.known_states.add(state)
        neighbors = self.state_neighbors(state)

        to_explore = [s for s in neighbors if s not in self.succ]
        for s in to_explore:
            self.bfs(s)
        return

    def valueIteration(self, discount, iterations):
        if not self.fully_explored:
            self.generateAllStates()

        self.V = defaultdict(float) #default val = 0

        for i in range(iterations):
            for state in self.known_states:
                    adj_vs = []
                    for neighbor in self.succ.get(state):
                        for action in self.actions:
                            v =  self.T(state, action, neighbor) * (discount*self.V[neighbor] + self.R(state, action, neighbor))
                            adj_vs.append(v)
                    opt = max(adj_vs) if adj_vs else self.V[state]
                    self.V[state] = opt

    def action_info(self, state, action):
        neighbors = self.state_neighbors(state)
        T_prob = [self.T(state, action, state)]
        val_state = [(self.R(state, action, state), state)]
        for s_prime in neighbors:
            if s_prime[0] == state[0] and s_prime[1] == state[1]: continue #deep equals for some reason
            prob = self.T(state, action, s_prime)
            if prob > 0:
                T_prob.append(prob + T_prob[-1]) # generate cumulative prob
                val_state.append((self.R(state, action, s_prime), s_prime))
        return T_prob, val_state

    def QLearning(self, discount, nEpisodes, epsilon):
        N = defaultdict(int)
        self.Q = defaultdict(float)

        for i in range(nEpisodes):
            self.current_state = self.start_state
            # j = 0
            while (self.current_state != "DEAD"):
                state = self.current_state
                samples = []
                for a in self.actions:
                    T_prob, val_state = self.action_info(state, a)
                    r, s_prime = random.choices(val_state, cum_weights=T_prob, k=1)[0] if sum(T_prob) > 0 else (val_state[0][0], state)
                    # sample = discount*self.Q[s_prime, a] + r
                    sample = discount*self.V[s_prime] + r #assume optimal from here on out; this was better than line above
                    samples.append((sample, a, s_prime))

                rand = random.random()
                sample, a_prime, s_prime = max(samples, key=lambda x: x[0]) if (1-rand) < epsilon else random.choice(samples)
                N[(state,a_prime)] += 1
                alpha = 1.0 / N[(state,a_prime)]
                Q_k = self.Q[(state,a_prime)]
                self.Q[(state,a_prime)] = (1-alpha) * Q_k + (alpha * sample)
                self.current_state = s_prime
            if REPORTING and i % 100 == 0:
                print('Completed %d episodes' % (i + 1))

    def extractPolicy(self):
        self.optPolicy = {}
        for s in self.known_states:
            opt_val, opt_action = max([(self.Q[(s, a)], a) for a in self.actions])
            self.optPolicy[s] = opt_action
        return self.optPolicy

    '''for EC'''
    def follow_policy(self):
        if not self.optPolicy:
            self.extractPolicy()
        self.current_state = self.start_state
        while self.current_state != 'DEAD':
            self.take_action(self.optPolicy[self.current_state])

