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
from AI_heuristics import AI_heuristics

class EightPuzzleProblem (SearchProblem):
    # the 3x3 puzzle grid is an array with the grid cells in row-major order
    # 0 represents empty block
    def __init__(self, grid):
        self.grid = list(grid)
        for i in range(len(grid)):
            if self.grid[i] == 0:
                self.pos0 = i
                break

    # a state is a tuple ([grid], pos0, [path])
    def getStartState(self): return (self.grid, self.pos0, [])

    # the goal state is defined as [1,2,3,4,5,6,7,8,0]
    def isGoalState(self, state):
        #!#! DEBUG print('state: ', state)
        grid, pos0, *_ = state #!#! nawaf: accomodates the change of state::generalSearch()::AI_search.py where it now has a variable-length list representing the path.
        for i in range(8):
            if grid[i] != i+1: return False
        return pos0 == 8

    def getSuccessors(self, state):
        moves = []
        grid, pos0, path = state
        # uncomment below to print the current state
        #print(state)
        def generateMove(incr, action):
            pathCopy = list(path)
            pathCopy.append(action)
            gridCopy = list(grid)
            gridCopy[pos0], gridCopy[pos0 + incr] = gridCopy[pos0 + incr], gridCopy[pos0]
            moves.append((gridCopy, pos0 + incr, pathCopy))

        if pos0 >= 3: generateMove(-3, 'U')      # slide empty block up
        if pos0 <= 5: generateMove(3, 'D')       # slide empty block down
        if (pos0%3) > 0: generateMove(-1, 'L')   # Slide empty block left
        if (pos0%3) < 2: generateMove(1, 'R')    # Slide empty block right

        # uncomment to print the generated nodes
        # print([i[2] for i in moves])
        return moves

    def getHeuristics(self):
        return [AI_heuristics.manhattanDistance, AI_heuristics.hammingDistance]


###