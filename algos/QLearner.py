import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.98, \
        radr = 0.999, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        # current pos
        self.s = 0
        self.a = 0
        
        # data structures
        self.Q = np.random.random((num_states, num_actions))
        # T table of [s, a, s_prime] experience count
        self.T_count = np.ones(
            (num_states, self.num_actions, num_states)) * 0.00001
        # T table of [s, a, s_prime] probability count
        self.T = np.ones(
            (num_states, self.num_actions, num_states)) * 0.00001
        self.R = np.ones((num_states, self.num_actions)) * 0
        

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        if rand.uniform(0,1) < self.rar:
            self.a = rand.randint(0, self.num_actions-1)
        else:
            self.a = np.argmax(self.Q, axis = 1)[self.s]
        if self.verbose: print "s =", s,"a =", self.a
        return self.a


    def query(self, s_prime, r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        # update Q table
        future_reward = max(self.Q[s_prime])
        current_q = self.Q[self.s][self.a]
        self.Q[self.s][self.a] = ((1 - self.alpha) * current_q +
                self.alpha * (r + self.gamma * future_reward))

        # Dyna hallucinate experience
        if self.dyna > 0:
            self.run_dyna(self.s, self.a, s_prime, r)
        
        # return next action
        self.s = s_prime
        self.rar = self.rar * self.radr
        if rand.uniform(0,1) < self.rar:
            self.a = rand.randint(0, self.num_actions-1)
        else:
            self.a = np.argmax(self.Q, axis = 1)[self.s]
        if self.verbose: print "s =", s_prime,"a =", self.a,"r =",r
        return self.a

    
    def run_dyna(self, s, a, s_prime, r):
        # update T and R
        self.T_count[s][a][s_prime] += 1
        self.T[s][a][:] = (self.T_count[s][a][:] /
                           sum(self.T_count[s][a][:]))
        self.R[s][a] = ((1-self.alpha) * self.R[s][a] +
                        self.alpha * r)
        # run hallucinations
        for i in range(self.dyna):
            self.new_dyna_experience()
            self.rar = self.rar * self.radr # reduce random selection
        # end run_dyna

    def new_dyna_experience(self):
        s = np.random.random_integers(0, self.num_states - 1)
        a = np.random.random_integers(0, self.num_actions - 1)
        s_prime = np.argmax(self.T[s][a][:])
        r = self.R[s][a]
        # update Q table
        future_reward = max(self.Q[s_prime])
        current_q = self.Q[s][a]
        self.Q[s][a] = ((1 - self.alpha) * current_q +
                self.alpha * (r + self.gamma * future_reward))

