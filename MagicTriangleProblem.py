# %%
from AI_problem import SearchProblem
from AI_heuristics import AI_heuristics

# %%
class MagicTriangleProblem (SearchProblem):
    
    def __init__(self, S):
        self.S = S
        self.triangle = [0,0,0,0,0,0] # numbers in the triangle         

    # def get side sums
    def getSideSums(self, triangle):
        sideSum1 = triangle[0] + triangle[1] + triangle[2]
        sideSum2 = triangle[2] + triangle[3] + triangle[4]
        sideSum3 = triangle[4] + triangle[5] + triangle[0]
        return (sideSum1, sideSum2, sideSum3)
    
    # a state is a tuple ([triangle], [path], S)
    def getStartState(self): return (self.triangle, [], self.S)

    # example goal state for S = 9: [1,5,3,4,2,6]
    def isGoalState(self, state):
        triangle, _, S = state
        sideSums = self.getSideSums(triangle)
        return (all(s == S for s in sideSums)) and (0 not in triangle)

    def getSuccessors(self, state):
        
        moves = []
        triangle, path, S = state
        allnums = [1,2,3,4,5,6]

        # uncomment below to print the current state
        #print(state)
    
        # pick one circle and assign it a unique number
        for circle in range(len(triangle)):
            
            if triangle[circle] == 0: # assign if empty 
                # define possible assignments for a circle
                possible_numbers = [i for i in allnums if i not in triangle]
            
                # assign all possibilities to the circle
                for num in possible_numbers:
                    pathCopy = list(path)
                    triangleCopy = list(triangle)
                    triangleCopy[circle] = num
                    pathCopy.append((circle, num))
                    moves.append((triangleCopy, pathCopy, S))
                break
                        
        # uncomment to print the generated nodes
        # print([i[2] for i in moves])
        return moves

    def getHeuristics(self):
        return [AI_heuristics.avgSumOffset]



