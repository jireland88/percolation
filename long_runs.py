import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from path_helpers import *
from path_finders import *
from percolation import *

# p_c square lattice
P = Percolation(np.zeros((500, 500)), RobotPathFinder(SquareStateChooser()))
PT = PercolationTools(P)
p_c_square = PT.find_critical_value_bs(50, 20)

# p_c triangle lattice
TP = Percolation(np.zeros((500,500)), RobotPathFinder(TriangleStateChooser()))
TPT = PercolationTools(TP)
p_c_triangle = TPT.find_critical_value_bs(50, 20)

# beta
P = Percolation(np.zeros((51, 51)), RecPathFinder(TriangleNeighbours()))

def beta():
    epsilons = [x for x in np.linspace(0, 2e-1, 100) if x != 0]
    Gs = [P.simulate_centre(100, 0.5 + e) for e in epsilons]

    log_epsilons = []
    log_Gs = []

    for i in range(0, len(epsilons)):
        if Gs[i] != 0:
            log_epsilons.append(np.log(epsilons[i]))
            log_Gs.append(np.log(Gs[i]))

    regr = LinearRegression().fit(np.array(log_epsilons).reshape(-1,1), log_Gs)

    return regr.coef_[0]

betas = [beta() for _ in range(50)]

beta_hat = sum(betas)/len(betas)

d = {"p_c_square" : p_c_square, "p_c_triangle ": p_c_triangle, "beta_hat" : beta_hat}
df = pd.DataFrame.from_dict(d, orient="index")
df.to_csv("values.csv")
