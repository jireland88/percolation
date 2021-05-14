from percolation import *
from path_helpers import *
from path_finders import *

iters = 50

P_05 = Percolation(np.zeros((5, 5)), RecPathFinder(TriangleNeighbours()))
PT = PercolationTools(P_05)

PT.plot_centre_prob(50, 1)