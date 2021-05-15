class Helper():
    def check_neighbours(self, lattice, n, row, col):
        raise NotImplementedError

    def next_state(self, lattice, x, y, state):
        raise NotImplementedError

class SquareNeighbours(Helper):
    def check_neighbours(self, lattice, n, row, col):
        to_check = []

        if row - 1 >= 0 and lattice[row-1][col] == 1:
            to_check.append([row-1, col])
        if row + 1 < n and lattice[row+1][col] == 1:
            to_check.append([row+1, col])
        if col - 1 >= 0 and lattice[row][col-1] == 1:
            to_check.append([row, col-1])
        if col + 1 < n and lattice[row][col+1] == 1:
            to_check.append([row, col+1])

        return to_check

class TriangleNeighbours(Helper):
    def check_neighbours(self, lattice, n, row, col):
        to_check = []

        if row - 1 >= 0 and lattice[row-1][col] == 1:
            to_check.append([row-1, col])
        if row + 1 < n and lattice[row+1][col] == 1:
            to_check.append([row+1, col])
        if col - 1 >= 0 and lattice[row][col-1] == 1:
            to_check.append([row, col-1])
        if col + 1 < n and lattice[row][col+1] == 1:
            to_check.append([row, col+1])
        if col + 1 < n and row - 1 < n and lattice[row-1][col+1] == 1:
            to_check.append([row-1, col+1])
        if col - 1 >= 0 and row + 1 < n and lattice[row+1][col-1] == 1:
            to_check.append([row+1, col-1])

        return to_check

class SquareStateChooser(Helper):
    def next_state(self, lattice, x, y, state):
        success = False
        path_exists = True
        if state==1:
            if y!=0 and lattice[y-1][x]==1:
                y=y-1
                state=4
            else:
                state=2
        elif state==2:
            if x==len(lattice[0,:])-1:
                success = True
            if success != True and lattice[y][x+1]==1:
                x=x+1
                state=1
            else:
                state=3
        elif state==3:
            if y!=len(lattice[:,0])-1:
                if lattice[y+1][x]==1:
                    y=y+1
                    state=2
                else:
                    state=4
            else:
                state=4
        elif state==4:
            #print(str(x)+' = x '+str(y)+' = y')
            if x!=0:
                if lattice[y][x-1]==1:
                    x=x-1
                    state=3
                else:
                    state=1
            else:
                path_exists = False
        else:
            print("there is no such state")
        return x, y, state, path_exists, success

class TriangleStateChooser(Helper):
    def next_state(self, lattice, x, y, state):
        n = len(lattice[0,:])-1
        success = False
        path_exists = True
        if state==1:
            if y!=0 and lattice[y-1][x]==1:
                y=y-1
                state=6
            else:
                state=2
        elif state==2:
            if x==n:
                success = True
            elif success != True and lattice[y-1][x+1]==1 and y!=0:
                x=x+1
                y=y-1
                state=1
            else:
                state=3
        elif state==3:
            if x==n:
                success = True
            if success != True and lattice[y][x+1]==1:
                x=x+1
                state=2
            else:
                state=4
        elif state==4:
            if y!=n:
                if lattice[y+1][x]==1:
                    y=y+1
                    state=3
                else:
                    state=5
            else:
                state=5
        elif state==5:
            if x!=0:
                if y!=n:
                    if lattice[y+1][x-1]==1:
                        x=x-1
                        y=y+1
                        state=4
                    else:
                        state=6
                else:
                    state=6
            else:
                path_exists = False
        elif state==6:
            if x!=0:
                if lattice[y][x-1]==1:
                    x=x-1
                    state=5
                else:
                    state=1
            else:
                path_exists = False
        else:
            print("there is no such state")
        return x, y, state, path_exists, success
