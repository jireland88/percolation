import numpy as np

class PathFinder():
    def __init__(self, Helper):
        self.Helper = Helper
    
    def is_path():
        raise NotImplementedError

    def is_centre_path():
        raise NotImplementedError

class RecPathFinder(PathFinder):
    def __init__(self, Neighbours):
        super().__init__(Neighbours)

    def is_path(self, lattice, n):
        visited = np.zeros((n, n))

        def is_path_rec(row, col):
            # check for success
            if col == n-1: return True

            # check if already visited
            if visited[row][col] == 1:
                return False
            else:
                visited[row][col] = 1

            # check for neighbours
            for nb in self.Helper.check_neighbours(lattice, n, row, col):
                if is_path_rec(nb[0], nb[1]): return True

            # return False if no success
            return False

        for i in range(0, n):
            if lattice[i][0] == 1:
                if is_path_rec(i, 0): return True

        return False
    
    def is_centre_path(self, lattice, n):
        visited = np.zeros((n, n))

        def is_centre_path_rec(row,col):
            # TODO: for some reason code never gets to col=0 or row = 0
            if col == 0 or col == n-1 or row == 0 or row == n-1:
                print(row, col)
                return True

            #if col == 0 or row == 0:
            #    print(row, col)
            #    return True

            # check if already visited
            if visited[row][col] == 1:
                return False
            else:
                visited[row][col] = 1

            for nb in self.Helper.check_neighbours(lattice, n, row, col):
                if is_centre_path_rec(nb[0], nb[1]): return True

            return False

        if n % 2 == 0: return None
        centre = int((n+1)/2)
        if lattice[centre][centre] != 1:
            return False
        else:
            return is_centre_path_rec(centre,centre)

class RobotPathFinder(PathFinder):
    def __init__(self, StateChooser):
        super().__init__(StateChooser)

    def is_path(self, lattice, n):
        for i in range(n):
            if lattice[i][0] == 1:
                x=0
                y=i
                state=1
                path_exists = True
                while path_exists == True:
                    x, y, state, path_exists, success = self.Helper.next_state(lattice, x, y, state)
                    if success: return True
        return False