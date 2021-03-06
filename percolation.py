import numpy as np
import matplotlib.pyplot as plt

from path_helpers import *
from path_finders import *

class Percolation(object):
    def __init__(self, lattice, PathFinder):
        self.lattice = lattice
        self.n = self.lattice.shape[0]
        self.PathFinder = PathFinder

        # Store initial lattice for when we reset
        self.init_lat = lattice

    def reset(self):
        self.lattice = self.init_lat

    def update_lattice(self, i, j, val):
        self.lattice[i][j] = val

    def is_path(self): return self.PathFinder.is_path(self.lattice, self.n)

    def is_centre_path(self): return self.PathFinder.is_centre_path(self.lattice, self.n)

    def is_bottom_to_right_path(self, r): return self.PathFinder.is_bottom_to_right_path(self.lattice, self.n, r)

    def percolate(self, p):
        self.reset()
        for i in range(0,self.n):
            for j in range(0,self.n):
                # np.random.binomial(1, p) = 1 w.p. p and 0 otherwise
                self.update_lattice(i,j,np.random.binomial(1, p))
        return self.lattice

    def simulate(self, iter, p):
        # simulates the value of F_n(p) using given number of iterations
        n_True = 0
        for i in range(iter):
            # reset the lattice, create a random percolation and increment if there is a path
            self.reset()
            self.percolate(p)
            if self.is_path():
                n_True += 1
        return n_True / iter

    def simulate_centre(self, iter, p):
        # simulates the value of G_n(p) using a given number of iterations
        n_True = 0
        for i in range(iter):
            # reset the lattice, create a random percolation and increment if there is a path
            self.reset()
            self.percolate(p)
            if self.is_centre_path():
                n_True += 1
        return n_True / iter

    def simulate_bottom_right(self, iter, p_c, r):
        # simulates the probability that the bottom and left sides are connected as outlined in T10
        n_True = 0
        for i in range(iter):
            # reset the lattice, create a random percolation and increment if there is a path
            self.reset()
            self.percolate(p_c)
            if self.is_bottom_to_right_path(r):
                n_True += 1
        return n_True / iter

# class to provide additional features to a percolation
class PercolationTools(object):
    def __init__(self, perc_obj):
        self.perc_obj = perc_obj

    def update_perc(self, perc_obj):
        self.perc_obj = perc_obj

    def display(self, ax, no_print=True):
        xi = np.arange(0, self.perc_obj.n+1)
        yi = np.arange(0, self.perc_obj.n+1)
        X, Y = np.meshgrid(xi, yi)

        # flipping array so output matches array
        if not no_print: print(self.perc_obj.lattice)
        ax.pcolormesh(X, Y, np.flipud(self.perc_obj.lattice))

    def plot_centre_prob(self, iter, dp, plot_G = False, G=None):
        plt.figure()
        m = 10**dp
        xs = []
        ys = []
        # simulate G_n(p) for each p and plot
        for i in range(0, m):
            r = self.perc_obj.simulate_centre(iter, i/m)
            xs.append(i/m)
            ys.append(r)
        plt.plot(xs, ys, "-bo")

        # G is an approximate function that can be overlayed
        if plot_G == True:
            ps = np.linspace(0,1,100)
            Gs = [G(p) for p in ps]
            print(Gs[0:10])
            plt.plot(ps, Gs, "-r")

        plt.xlabel("p")
        plt.ylabel("G(p)")
        plt.show()

    def find_critical_value_g(self, iter, dp):
        plt.figure()
        m = 10**dp
        xs = []
        ys = []
        # simulate F_n(p) for each p and plot
        for i in range(0, m):
            r = self.perc_obj.simulate(iter, i/m)
            xs.append(i/m)
            ys.append(r)
        plt.plot(xs, ys, "-bo")
        plt.xlabel("p")
        plt.ylabel("F(p)")
        plt.show()

    def find_critical_value_bs(self, iter_sim, iter_search, l=0, u=1, m=0):
        # standard recursive binary search algorithm
        p = (u+l)/2

        if m >= iter_search: return p

        r = self.perc_obj.simulate(iter_sim, p)

        print(l,p,u,r)

        # if F_n(p) is less than 50/50 branch to lower half, otherwise branch to upper half
        if r < 0.5:
            return self.find_critical_value_bs(iter_sim, iter_search, p, u, m+1)
        else:
            return self.find_critical_value_bs(iter_sim, iter_search, l, p, m+1)
