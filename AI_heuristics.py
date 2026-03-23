##############################################################################
###
###   CMP 333 PROJECT 1 -- SEARCH
###
###   HEURISTIC FUNCTIONS for the 8-puzzle problem used by search algorithms
###   to be amended/expanded for other problems defined via the Problem class

###   Michel Pasquier 2019, adapted from the code @
###   https://kartikkukreja.wordpress.com/2015/06/14/heuristics-in-ai-search/
###


class AI_heuristics:

    def hammingDistance(grid):
        # a state is a tuple of the form (grid, pos0, path)
        grid = grid[0]
        return len([i for i in range(len(grid)) if grid[i] != 0 and grid[i] != i+1])

    # e.g. print(hammingDistance(([2,1,3,4,5,6,7,8,0], 8, [])))

    def manhattanDistance(grid):
        grid = grid[0]
        def distance(i):
            return 0 if grid[i] == 0 else abs(((grid[i]-1) / 3) - (i / 3)) + abs(((grid[i]-1) % 3) - (i % 3))
        return sum(distance(i) for i in range(len(grid)))

    #!-----Halla: MagicTriangleProblem------------
    def avgSumOffset(state):
        """
            Calculates the cost of a state as the:
                average difference of the side sums from the true sum S
                OR
                max cost = S when a state is impossible to solve
                
            Args: state (tuple): ([triangle], [path], S)
            Returns: cost
            
        """
        #halla: state form changed after edits. now all_vars is of the form ([triangle], [path], S)
        all_vars, _, _ = state #print to check the state variables
        triangle, path, S = all_vars
        
        #calculate the side sums
        circles = ([0,1,2],[2,3,4], [4,5,0])

        sideSum1 = sum([triangle[c] for c in circles[0]])
        sideSum2 = sum([triangle[c] for c in circles[1]])
        sideSum3 = sum([triangle[c] for c in circles[2]])
        sideSums = (sideSum1,sideSum2,sideSum3)
        
        
        #if a state is impossible to solve
        #the cost = max cost possible = S (initial state cost)
        for sideSum, sideCircles in zip(sideSums, circles):
            
            #impossible state 1: a side is full but its sum != S
            if sideSum != S and 0 not in [triangle[c] for c in sideCircles]:
                return S
            
            # impossible state 2: a side sum >= S but it's not full
            if sideSum >= S and 0 in [triangle[c] for c in sideCircles]:
                return S
                
        return sum([abs(S - s) for s in sideSums])/3
        
        
###