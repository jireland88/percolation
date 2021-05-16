import numpy as np

class PathFinder():
    # Abstract Base Class for a Path Finder object
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

        # recursive inner-function
        def is_path_rec(row, col):
            # check for success (on right-most column of lattice)
            if col == n-1: return True

            # check if already visited
            if visited[row][col] == 1:
                return False
            else:
                visited[row][col] = 1

            # check for neighbours, then run function on all neighbours
            for nb in self.Helper.check_neighbours(lattice, n, row, col):
                if is_path_rec(nb[0], nb[1]): return True

            # return False if no success
            return False

        # Check for path starting from all yellow squares in left-most column
        for i in range(0, n):
            if lattice[i][0] == 1:
                if is_path_rec(i, 0): return True

        return False

    def is_centre_path(self, lattice, n):
        visited = np.zeros((n, n))

        def is_centre_path_rec(row,col):
            # check if on the boundary
            if col == 0 or col == n-1 or row == 0 or row == n-1:
                return True

            # check if already visited
            if visited[row][col] == 1:
                return False
            else:
                visited[row][col] = 1

            for nb in self.Helper.check_neighbours(lattice, n, row, col):
                if is_centre_path_rec(nb[0], nb[1]): return True

            return False

        if n % 2 == 0: return None # return None if we have an even-sided lattice
        centre = int((n+1)/2) # otherwise we can compute the centre of the lattice
        if lattice[centre][centre] != 1:
            return False
        else:
            return is_centre_path_rec(centre,centre)

    def is_bottom_to_right_path(self, lattice, n, r):
        visited = np.zeros((n, n))

        def is_bottom_to_right_path_rec(row,col):
            # check condition defined in Q10
            if col == n-1 and row <= n*r:
                return True

            # check if already visited
            if visited[row][col] == 1:
                return False
            else:
                visited[row][col] = 1

            for nb in self.Helper.check_neighbours(lattice, n, row, col):
                # check if in "pink area" (see diagram) (col >= n-row)
                if nb[1] >= n - nb[0]:
                    if is_bottom_to_right_path_rec(nb[0], nb[1]): return True

            return False

        # run on all sites at the bottom of the lattice
        for i in range(0, n):
            if lattice[n-1][i] == 1:
                if is_bottom_to_right_path_rec(n-1, i): return True

        return False

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

    # Only works with square lattice due to time-constraints
    def is_centre_path(self, lattice, n):
        # For explanation of this function see Task 6 of the Jupyter notebook
        A = lattice
        start=int((len(A[:,0])-1)/2)
        if A[start][start]==1:
            x=start
            y=start
            save_x=None
            save_y=None
            c=0
            state=1
            while True :
                if x==0 or y==0 or y==len(A[:,0])-1 or x==len(A[:,0])-1:
                    return True
                if state==1:
                    if y!=0 and A[y-1][x]==1:
                        y=y-1
                        if c==1 or c==2:
                            state=4
                    else:
                        if c==0:
                            save_x=x
                            save_y=y
                            c=1
                        elif c==1 and save_x==x and save_y==y:
                            c=2
                        elif c==2 and save_x==x and save_y==y:
                            return False
                            break
                        state=2
                elif state==2:
                    if A[y][x+1]==1:
                            x=x+1
                            state=1
                    else:
                            state=3

                elif state==3:
                    if c==2 and x==save_x and y<save_y:
                            c=0 # reseting to restart the loop
                            state=1
                    elif y!=len(A[:,0])-1:
                        if A[y+1][x]==1:
                            y=y+1
                            state=2
                        else:
                            state=4
                    else:
                        state=4
                elif state==4:
                    if x!=0:
                        if A[y][x-1]==1:
                                x=x-1

                                state=3
                        else:
                            state=1
                else:
                    print("there is no such state")
        return False
