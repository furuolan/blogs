"""
Minimax linear program
"""
import numpy as np
from cvxopt import matrix, solvers
solvers.options['glpk'] = {'tm_lim': 1000} # max timeout for glpk

class LinProg(object):
    """
    LP solution for multiple agent zero-sum game with payoffs for PA as A
    """
    def __init__(self, verbose=False):
        if not verbose:
            solvers.options['show_progress'] = False # disable solver output
            solvers.options['glpk'] = {'msg_lev': 'GLP_MSG_OFF'}  # cvxopt 1.1.8
            solvers.options['LPX_K_MSGLEV'] = 0  # previous versions

    def maxmin(self, A, solver="glpk"):
        num_vars = len(A)
        # minimize matrix c
        c = [-1] + [0 for i in range(num_vars)]
        c = np.array(c, dtype="float")
        c = matrix(c)
        # constraints G*x <= h
        G = np.matrix(A, dtype="float").T # reformat each variable is in a row
        G *= -1 # minimization constraint
        G = np.vstack([G, np.eye(num_vars) * -1]) # > 0 constraint for all vars
        new_col = [1 for i in range(num_vars)] + [0 for i in range(num_vars)]
        G = np.insert(G, 0, new_col, axis=1) # insert utility column
        G = matrix(G)
        h = ([0 for i in range(num_vars)] + 
             [0 for i in range(num_vars)])
        h = np.array(h, dtype="float")
        h = matrix(h)
        # contraints Ax = b
        A = [0] + [1 for i in range(num_vars)]
        A = np.matrix(A, dtype="float")
        A = matrix(A)
        b = np.matrix(1, dtype="float")
        b = matrix(b)
        sol = solvers.lp(c=c, G=G, h=h, A=A, b=b, solver=solver)
        return sol

    def ce(self, A, solver=None):
        num_vars = len(A)
        # maximize matrix c
        c = [sum(i) for i in A] # sum of payoffs for both players
        c = np.array(c, dtype="float")
        c = matrix(c)
        c *= -1 # cvxopt minimizes so *-1 to maximize
        # constraints G*x <= h
        G = self.build_ce_constraints(A=A)
        G = np.vstack([G, np.eye(num_vars) * -1]) # > 0 constraint for all vars
        h_size = len(G)
        G = matrix(G)
        h = [0 for i in range(h_size)]
        h = np.array(h, dtype="float")
        h = matrix(h)
        # contraints Ax = b
        A = [1 for i in range(num_vars)]
        A = np.matrix(A, dtype="float")
        A = matrix(A)
        b = np.matrix(1, dtype="float")
        b = matrix(b)
        sol = solvers.lp(c=c, G=G, h=h, A=A, b=b, solver=solver)
        return sol

    def build_ce_constraints(self, A):
        num_vars = int(len(A) ** (1/2))
        G = []
        # row player
        for i in range(num_vars): # action row i
            for j in range(num_vars): # action row j
                if i != j:
                    constraints = [0 for i in A]
                    base_idx = i * num_vars
                    comp_idx = j * num_vars
                    for k in range(num_vars):
                        constraints[base_idx+k] = (- A[base_idx+k][0]
                                                   + A[comp_idx+k][0])
                    G += [constraints]
        # col player
        for i in range(num_vars): # action column i
            for j in range(num_vars): # action column j
                if i != j:
                    constraints = [0 for i in A]
                    for k in range(num_vars):
                        constraints[i + (k * num_vars)] = (
                            - A[i + (k * num_vars)][1] 
                            + A[j + (k * num_vars)][1])
                    G += [constraints]
        return np.matrix(G, dtype="float")


if __name__ == "__main__":
    """
    Tests only
    """
    import unittest
    class TestMinimax(unittest.TestCase):
        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_0(self):
            """
            http://cvxopt.org/examples/tutorial/lp.html
            """
            lp = LinProg(verbose=False)
            A = matrix([ [-1.0, -1.0, 0.0, 1.0], [1.0, -1.0, -1.0, -2.0] ])
            b = matrix([ 1.0, -2.0, 0.0, 4.0 ])
            c = matrix([ 2.0, 1.0 ])
            sol = solvers.lp(c, A, b, solver="glpk")
            probs = sol["x"]
            self.assertEqual(0.5, probs[0])
            self.assertEqual(1.5, probs[1])

        def test_1(self):
            """
            https://www.cs.duke.edu/courses/fall12/cps270/lpandgames.pdf
            """
            lp = LinProg(verbose=False)
            A = [[0,-1,1],[1,0,-1],[-1,1,0]]
            sol = lp.maxmin(A=A, solver="glpk")
            probs = sol["x"]
            self.assertEqual(1/3, probs[1])
            self.assertEqual(1/3, probs[2])
            self.assertEqual(1/3, probs[3])

        def test_2(self):
            """
            https://en.wikipedia.org/wiki/Minimax#Example
            """
            lp = LinProg(verbose=True)
            A = [[3,-2,2],[-1,0,4],[-4,-3,1]]
            sol = lp.maxmin(A=A, solver="glpk")
            probs = sol["x"]
            self.assertEqual(round(1/6, 5), round(probs[1],5))
            self.assertEqual(round(5/6, 5), round(probs[2],5))

        def test_ce_1(self):
            """
            Example p 28: https://www3.ul.ie/ramsey/Lectures/Operations_Research_2/gametheory4.pdf
            """
            A = [[2, 5], [0, 0],
                 [0, 0], [5, 2]]
            A = np.array(A)
            lp = LinProg(verbose=True)
            sol = lp.ce(A=A, solver="glpk")
            probs = sol["x"]
            equil = probs[0] + probs[3]
            self.assertEqual(round(1.0, 5), round(equil, 5))

        def test_ce_2(self):
            """
            Example Chicken game: https://www.cs.rutgers.edu/~mlittman/topics/nips02/nips02/greenwald.ps
            """
            A = [[6, 6], [2, 7],
                 [7, 2], [0, 0]]
            A = np.array(A)
            lp = LinProg(verbose=True)
            sol = lp.ce(A=A, solver="glpk")
            probs = sol["x"]
            print(probs)
            self.assertEqual(round(0.5, 5), round(probs[0], 5))
            self.assertEqual(round(0.25, 5), round(probs[1], 5))
            self.assertEqual(round(0.25, 5), round(probs[2], 5))
            self.assertEqual(round(0, 5), round(probs[3], 5))

        def test_ce_3(self):
            """
            Example Chicken game: https://www.cs.duke.edu/courses/fall16/compsci570/LPandGames.pdf
            """
            A = [[0, 0], [-1, 1],
                 [1, -1], [-5, -5]]
            A = np.array(A)
            lp = LinProg(verbose=True)
            sol = lp.ce(A=A, solver="glpk")
            probs = sol["x"]
            self.assertEqual(round(1.0, 5), round(sum(probs[:3]), 5))

    unittest.main(verbosity=3)