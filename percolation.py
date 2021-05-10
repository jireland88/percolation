import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

class Percolation(object):
    def __init__(self, lattice):
        self.lattice = lattice
        self.n = self.lattice.shape[0]

        self.init_lat = lattice

    def reset(self):
        self.lattice = self.init_lat

    def update_lattice(self, i, j, val):
        self.lattice[i][j] = val

    def check_neighbours(self, row, col):
        to_check = []

        if row - 1 > 0 and self.lattice[row-1][col] == 1:
            to_check.append([row-1, col])
        if row + 1 < self.n and self.lattice[row+1][col] == 1:
            to_check.append([row+1, col])
        if col - 1 > 0 and self.lattice[row][col-1] == 1:
            to_check.append([row, col-1])
        if col + 1< self.n and self.lattice[row][col+1] == 1:
            to_check.append([row, col+1])

        return to_check

    def is_path(self):
        visited = np.zeros((self.n, self.n))

        def is_path_rec(row, col):
            # check for success
            if col == self.n-1: return True

            # check if already visited
            if visited[row][col] == 1:
                return False
            else:
                visited[row][col] = 1

            # check for neighbours
            for n in self.check_neighbours(row, col):
                if is_path_rec(n[0], n[1]): return True

            # return False if no success
            return False

        for i in range(0, self.n):
            if self.lattice[i][0] == 1:
                if is_path_rec(i, 0): return True

        return False

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


    def is_centre_path(self):
        visited = np.zeros((self.n, self.n))

        def is_centre_path_rec(row,col):
            if col in [0,self.n-1] or row in [0,self.n-1]: return True

            # check if already visited
            if visited[row][col] == 1:
                return False, visited
            else:
                visited[row][col] = 1

            for n in self.check_neighbours(row, col):
                if is_centre_path_rec(n[0], n[1]): return True

            return False

        if self.n % 2 == 0: return None
        centre = int((self.n+1)/2)
        if self.lattice[centre][centre] != 1:
            return False
        else:
            return is_centre_path_rec(centre,centre)

    def simulate_centre(self, iter, p):
        self.reset()
        n_True = 0
        for i in range(iter):
            self.reset()
            self.percolate(p)
            if self.is_centre_path():
                n_True += 1
        return n_True / iter

class TriPercolation(Percolation):
    def check_neighbours(self, row, col):
        to_check = []

        if row - 1 > 0 and self.lattice[row-1][col] == 1:
            to_check.append([row-1, col])
        if row + 1 < self.n and self.lattice[row+1][col] == 1:
            to_check.append([row+1, col])
        if col - 1 > 0 and self.lattice[row][col-1] == 1:
            to_check.append([row, col-1])
        if col + 1 < self.n and self.lattice[row][col+1] == 1:
            to_check.append([row, col+1])
        if col + 1 < self.n and row + 1 < self.n and self.lattice[row+1][col+1] == 1:
            to_check.append([row+1, col+1])
        if col - 1 > 0 and row - 1 > 0 and self.lattice[row-1][col-1] == 1:
            to_check.append([row-1, col-1])

        return to_check

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

class PercolationRobot(object):
    def is_path():
        A=self.lattice
        for i in range(len(A[:,0])):
            if A[i][0]==0:
                x=0
                y=i
                state=1
                while True:
                    if state==1:
                        if y!=0 and A[y-1][x]==1:
                            y=y-1
                            state=4
                        else:
                            state=2
                    elif state==2:
                        if x==len(A[0,:])-1:
                            return True
                        if A[y][x+1]==1:
                            x=x+1
                            state=1
                        else:
                            state=3
                    elif state==3:
                        if y!=len(A[:,0])-1:
                            if A[y+1][x]==1:
                                y=y+1
                                state=2
                            else:
                                state=4
                        else:
                            state=4
                    elif state==4:
                        #print(str(x)+' = x '+str(y)+' = y')
                            if x!=0:
                                if A[y][x-1]==1:
                                    x=x-1
                                    state=3
                                else:
                                    state=1
                            else:
                                print('breaking')
                                break
                    else:
                        print("there is no such state")
        return False
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

    def plot_centre_prob(self, iter, dp):
        plt.figure()
        m = 10**dp
        xs = []
        ys = []
        for i in range(0, m):
            r = self.perc_obj.simulate_centre(iter, i/m)
            xs.append(i/m)
            ys.append(r)
        plt.plot(xs, ys, "-bo")
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

    def find_beta(self, epsilons, iter):
        log_epsilons = []
        log_G = []
        for e in epsilons:
            log_epsilons.append(np.log(e))
            log_G.append(np.log(self.perc_obj.simulate_centre(iter, 0.5 + e)))

        regr = linear_model.LinearRegression()
        regr.fit(np.array(log_epsilons).reshape(-1, 1), np.array(log_G).reshape(-1, 1))
        print(regr.coef_, regr.intercept_)
