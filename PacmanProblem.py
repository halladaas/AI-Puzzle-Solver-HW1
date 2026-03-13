##############################################################################
###
###   CMP 333 PROJECT 1 -- SEARCH
###
###   EIGHT-PUZZLE PROBLEM CLASS used with various AI search algorithms
###
###   Michel Pasquier 2019, adapted from the code @
###   https://kartikkukreja.wordpress.com/2015/06/14/heuristics-in-ai-search/
###


from AI_problem import SearchProblem

class PacmanProblem(SearchProblem):
    # the grid is a 2D array, pacman and the food are tuples (r,c)
    def __init__(self, grid, pacman, food):
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0])
        self.pacman = pacman
        self.food = food

    # since we need to output the solution path, it is stored in the state as
    # tuple(tuple(r,c), [tuple(r1,c1), tuple(r2,c2), ...])  where the first
    # tuple is the current position of pacman and the list is the path taken
    def getStartState(self): return (self.pacman, [self.pacman])

    def isGoalState(self, state): return state[0] == self.food

    def getSuccessors(self, state):
        moves = []
        path = state[1]

        def getMove(r, c):
            if self.grid[r][c] != '%':           # not a wall
                newPath = list(path)
                move = (r, c)
                newPath.append(move)
                moves.append((move, newPath))
        if state[0][0] > 0:
            getMove(state[0][0]-1, state[0][1])  # go up
        if state[0][0] < self.rows -1:
            getMove(state[0][0]+1, state[0][1])  # go down
        if state[0][1] > 0:
            getMove(state[0][0], state[0][1]-1)  # go left
        if state[0][1] < self.columns - 1:
            getMove(state[0][0], state[0][1]+1)  # go right
        return moves

    def getHeuristics(self):
        # straight-line distance between pacman and the food
        def straightLineDistance(state):
            pacman, food = state[0], self.food
            return ((food[1]-pacman[1])**2 + (food[0]-pacman[0])**2)**0.5
        return [straightLineDistance]


###