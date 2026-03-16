##############################################################################
###
###   CMP 333 PROJECT 1 -- SEARCH
###
###   AI SEARCH ALGORITHMS AND SUPPORTING DATA STRUCTURES for the frontier
###   General Search and BFS, DFS, IDA, UFS, A*, and Greedy search;
###   Stack, Queue, and Priority Queue.
###
###   Michel Pasquier 2019, adapted from the code @
###   https://kartikkukreja.wordpress.com/2015/06/14/heuristics-in-ai-search/
###

#! importing the problems
from EightPuzzleProblem import EightPuzzleProblem
from MagicTriangleProblem import MagicTriangleProblem

class Stack:
    def __init__(self): self.items = []

    def push(self, item): self.items.append(item)

    def pop(self): return self.items.pop()

    def empty(self): return not self.items

from collections import deque
class Queue:
    def __init__(self): self.items = deque()

    def push(self, item): self.items.append(item)

    def pop(self): return self.items.popleft()

    def empty(self): return not self.items

import heapq
class PriorityQueue:
    def __init__(self, priorityFunction):
        self.priorityFunction = priorityFunction
        self.heap = []

    def push(self, item):
        heapq.heappush(self.heap, (self.priorityFunction(item), item))

    def pop(self):
        (_, item) = heapq.heappop(self.heap)
        return item

    def empty(self): return not self.heap


#! aziz's implementation

def generalSearch(problem, strategy, pruning = 'none'):
    start_state = problem.getStartState()

    strategy.push((start_state, None, [start_state]))
    #! node now looks like (state, parent, path)

    # added counters to keep track of the number of nodes expanded/generated
    num_nodes_exp = 0
    num_nodes_gen = 1
    
    #! aziz: WIP
    explored = set()

    while not strategy.empty():
        state, parent, path = strategy.pop()
        
        #! aziz: WIP
        if pruning == 'full':
            state_ref = str(state)
            if state_ref in explored: continue
            explored.add(state_ref)
            
        num_nodes_exp += 1
        #> uncomment below to print the priority queue at each iteration
        #print(strategy.heap)

        #> uncomment below to print the node being expanded
        #print(current_node)
        if problem.isGoalState(state):
            return (state, num_nodes_exp, num_nodes_gen)
        
        for move in problem.getSuccessors(state):
            #! aziz: problem-specific extraction:
            #! 8puzzle returns (state, action, cost) -> need move[0]
            #! MT returns the state tuple directly -> move
            if isinstance(problem, MagicTriangleProblem):
                next_state = move
            else:
                next_state = move[0]
                
            #! parent pruning: avoid moving back directly to the previous state
            if pruning == 'parent' and parent is not None:
                if next_state == parent:
                    #print('DEBUG PARENT PRUNED')
                    continue
            
            #! ancestor pruning: avoid forming cycles in the current path
            if pruning == 'ancestor':
                if next_state in path:
                    continue
            
            #! update the new path
            new_path = path + [next_state]

            #! push new tuple into strategy
            strategy.push((next_state, state, new_path))
            num_nodes_gen += 1

        #> uncomment to print num of nodes generated after each node expansion
        #print(num_nodes_gen)
    return None


#! aziz: updated the arguments and handling the node tuple
def breadthFirstSearch(problem, pruning = 'none'): return generalSearch(problem, Queue(), pruning)

def depthFirstSearch(problem, pruning = 'none'): return generalSearch(problem, Stack(), pruning)

#! aziz: modified search to allow pruning
def iterativeDeepeningSearch(problem, pruning = 'none'):
    num_nodes_exp = 0
    num_nodes_gen = 1
    def depthLimitedDFS(problem, state, depth, parent=None, path=None):
        if path is None: path = [state]
        nonlocal num_nodes_gen, num_nodes_exp
        num_nodes_exp += 1
        if problem.isGoalState(state): return state
        if depth <= 0: return None
        for move in problem.getSuccessors(state):
            if isinstance(problem, MagicTriangleProblem):
                next_state = move
            else:
                next_state = move[0]
                
            if pruning == 'parent' and parent is not None and next_state == parent: 
                continue
            if pruning == 'ancestor' and next_state in path: 
                continue
            
            num_nodes_gen += 1
            solution = depthLimitedDFS(problem, next_state, depth-1, state, path + [next_state])
            if solution is not None: 
                return solution
        return None

    depth = 1
    while True:
        solution = depthLimitedDFS(problem, problem.getStartState(), depth)
        if solution is not None:
            return (solution, num_nodes_exp, num_nodes_gen)
        depth += 1

def uniformCostSearch(problem, pruning = 'none'):
    #!----Halla : added isinstance checking and path cost for the MTP
    if isinstance(problem, EightPuzzleProblem):
        pathCost = lambda node: (sum(node[0][3]) if len(node[0]) > 3 else len(node[0][-1]))
    elif isinstance(problem, MagicTriangleProblem ):
        pathCost = lambda node: (len(node[2]))
    #! aziz: add a fallback case (temporary until 8puzzle & Sokoban)
    else:
        pathCost = lambda node: len(node[2]) 
        
    return generalSearch(problem, PriorityQueue(pathCost),  pruning)

def greedySearch(problem, heuristic, pruning = 'none'):
    return generalSearch(problem, PriorityQueue( lambda node: heuristic(node[0])), pruning)

def astarSearch(problem, heuristic, pruning = 'none'):
    # the given function uses the number of steps as g-cost (uniform cost)
    # the number of elements in a state changes for different problems, hence
    # the following checks
    
    #!----Halla : added isinstance checking and path cost for the MTP
    if isinstance(problem, EightPuzzleProblem):
        totalCost = lambda node: (sum(node[0][3]) if len(node[0]) > 3 else len(node[0][-1])) + heuristic(node[0])
    elif isinstance(problem, MagicTriangleProblem ):
        totalCost = lambda node: (len(node[2])) + heuristic(node[0])
    #! aziz: fallback case (tmp)
    else:
        totalCost = lambda node: len(node[2]) + heuristic(node[0])
        
    return generalSearch(problem, PriorityQueue(totalCost), pruning)