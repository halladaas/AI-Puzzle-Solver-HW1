##############################################################################
###
###   CMP 333 PROJECT 1 -- SEARCH
###
###   SOLVE FUNCTION used to solve various AI search problems
###
###   Michel Pasquier 2019, to be adapted/expanded as necessary
###


from AI_search import generalSearch, breadthFirstSearch, depthFirstSearch, \
    iterativeDeepeningSearch, uniformCostSearch, greedySearch,astarSearch, \
    Stack, Queue, PriorityQueue
from EightPuzzleProblem import EightPuzzleProblem
from MagicTriangleProblem import MagicTriangleProblem
from PacmanProblem import PacmanProblem
import pandas as pd

def solve(problem, search_algorithms):

    #!--Halla: Storing results in a dataframe-----
    results = []
    
    #!--Halla: added algorithm name as a parameter
    def print_info(solution, algorithm):
        if not solution:
            print("No solution!")
            return
        state, num_nodes_exp, num_nodes_gen = solution
        if isinstance(problem, EightPuzzleProblem):
            finalstate,_,steps = state
            cost = len(steps)
        else:
            finalstate, steps = state[:2]
            cost = len(steps)
            
        print(f"Final state: {finalstate}")
        print(f"Solution: {steps}")
        print(f"Cost: {cost}")
        print(f"Number of nodes expanded: {num_nodes_exp}")
        print(f"Number of nodes generated: {num_nodes_gen}")
        print("="*80+"\n")
        results.append([algorithm,num_nodes_exp,num_nodes_gen,cost])
        
    print(problem.__class__.__name__)
    #! aziz: add prune calls
    prune_type = 'none'

    for algo in search_algorithms:
        if algo.__name__ in ["greedySearch", "astarSearch"]: # heuristic search
            for heuristic in problem.getHeuristics():
              print(f"Algorithm used: {algo.__name__} | Pruning: {prune_type}")
              print(f"Heuristic used: {heuristic.__name__}")
              solution = algo(problem, heuristic, pruning = prune_type)
              print_info(solution, f"{algo.__name__}_{prune_type}") #!--Halla: added algo name as a parameter
        else:
            print(f"Algorithm used: {algo.__name__} | Pruning: {prune_type}")
            solution = algo(problem, pruning=prune_type)
            print_info(solution, f"{algo.__name__}_{prune_type}") #!--Halla: added algo name as a parameter
    
    #!--Halla: Storing results in a dataframe-----
    df = pd.DataFrame(results, columns=['problem', 'nodes_expanded', 'nodes_generated', 'cost'])
    return df

puzzle = [1,8,0,
          4,3,2,
          5,7,6]
#solve(EightPuzzleProblem(puzzle), [breadthFirstSearch, uniformCostSearch, astarSearch, iterativeDeepeningSearch])

#!----Halla-------
df = solve(MagicTriangleProblem(10), [breadthFirstSearch, depthFirstSearch, iterativeDeepeningSearch, uniformCostSearch, greedySearch, astarSearch])
print(df)


pacmap = ["P---------",
          "%%-%%-%-%%",
          "---%--%---",
          "-%%%-%%%-%",
          "---%%%-.-%",
          "-%------%%"]

# solve(PacmanProblem(pacmap, (0,0), (4,7)), [breadthFirstSearch,greedySearch,astarSearch])


#!#! =========== Nawaf ==========
#!#! EightPuzzleProblem.py

print('\n\n\n')

puzzle = [
    1, 3, 8,
    4, 0, 2,
    5, 7, 6
]

df = solve(EightPuzzleProblem(puzzle),
          [
            #  depthFirstSearch, #!#! exempt because it is not complete in the precense of cycles and infinite branches. Pruning may solve this issue.
            breadthFirstSearch, 
            iterativeDeepeningSearch, 
            uniformCostSearch,
            # greedySearch, #!#! exempt because it is not complete in the precense of cycles and infinite branches. Pruning may solve this issue.
            astarSearch
          ]
      )

# print(df)

randomPuzzle = [
    1, 8, 2,
    0, 4, 3,
    7, 6, 5
]

df = solve(EightPuzzleProblem(randomPuzzle),
          [
            #  depthFirstSearch, #!#! exempt because it is not complete in the precense of cycles and infinite branches. Pruning may solve this issue.  
              breadthFirstSearch, 
              iterativeDeepeningSearch, 
              uniformCostSearch,
            # greedySearch, #!#! exempt because it is not complete in the precense of cycles and infinite branches. Pruning may solve this issue.
              astarSearch
          ]
      )

print(df)



###
