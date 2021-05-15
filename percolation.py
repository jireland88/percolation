import numpy as np
import matplotlib.pyplot as plt

from path_helpers import *
from path_finders import *

class Percolation(object):
    def __init__(self, lattice, PathFinder):
        self.lattice = lattice
        self.n = self.lattice.shape[0]
        self.PathFinder = PathFinder

        self.init_lat = lattice

    def reset(self):
        self.lattice = self.init_lat

    def update_lattice(self, i, j, val):
        self.lattice[i][j] = val

    def is_path(self): return self.PathFinder.is_path(self.lattice, self.n)

    def is_centre_path(self): return self.PathFinder.is_centre_path(self.lattice, self.n)

    def percolate(self, p):
        self.reset()
        for i in range(0,self.n):
            for j in range(0,self.n):
                self.update_lattice(i,j,np.random.binomial(1, p))
        return self.lattice

    def simulate(self, iter, p):
        self.reset()
        n_True = 0
        for i in range(iter):
            self.reset()
            self.percolate(p)
            if self.is_path():
                n_True += 1
        return n_True / iter

    def simulate_centre(self, iter, p):
        self.reset()
        n_True = 0
        for i in range(iter):
            self.reset()
            self.percolate(p)
            if self.is_centre_path():
                n_True += 1
        return n_True / iter

class PercolationSophisticated(Percolation):
    def percolate_rand(self, p):
        self.reset()
        for i in range(0,self.n):
            for j in range(0,self.n):
                self.update_lattice(i,j,random())
                if self.lattice[i][j] < p:
                    self.lattice[i][j] = 1
                else:
                    self.lattice[i][j] = 0
        return self.lattice

#    def find_critical_value():

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
        for i in range(0, m):
            r = self.perc_obj.simulate_centre(iter, i/m)
            xs.append(i/m)
            ys.append(r)
        plt.plot(xs, ys, "-bo")

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
        for i in range(0, m):
            r = self.perc_obj.simulate(iter, i/m)
            xs.append(i/m)
            ys.append(r)
        plt.plot(xs, ys, "-bo")
        plt.xlabel("p")
        plt.ylabel("F(p)")
        plt.show()

    def find_critical_value_bs(self, iter_sim, iter_search, l=0, u=1, m=0):
        p = (u+l)/2

        if m >= iter_search: return p

        r = self.perc_obj.simulate(iter_sim, p)

        print(l,p,u,r)

        if r < 0.5:
            return self.find_critical_value_bs(iter_sim, iter_search, p, u, m+1)
        else:
            return self.find_critical_value_bs(iter_sim, iter_search, l, p, m+1)
