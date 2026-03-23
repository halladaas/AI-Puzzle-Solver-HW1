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
    
    #! Using dictionary method instead of set
    presentSet = dict() 

    while not strategy.empty():
        state, parent, path = strategy.pop()
        num_nodes_exp += 1
        #> uncomment below to print the priority queue at each iteration
        #print(strategy.heap)

        #> uncomment below to print the node being expanded
        #print(current_node)

        if problem.isGoalState(state):
            return (state, num_nodes_exp, num_nodes_gen)
            
        for move in problem.getSuccessors(state):
            #!#! nawaf: changed next_state to maintain the structure of the 8-puzzle state
            next_state = move 
            #! extract physical board
            board_tuple = tuple(next_state[0]) 
            
            #! update the new path (defined before cost calculation)
            new_path = path + [next_state]
            
            #! full pruning logic
            if pruning == 'full':
                if isinstance(strategy, PriorityQueue): 
                    cost = strategy.priorityFunction((next_state, state, new_path))
                    if cost < presentSet.get(board_tuple, float('inf')): 
                        presentSet[board_tuple] = cost
                    else: 
                        continue
                else:
                    if board_tuple in presentSet: 
                        continue
                    else: 
                        presentSet[board_tuple] = True
                        
            #! parent pruning: avoid moving back directly to the previous state (compare index 0)
            elif pruning == 'parent' and parent is not None:
                if next_state[0] == parent[0]:
                    continue
                    
            #! ancestor pruning: avoid forming cycles in the current path (compare index 0)
            elif pruning == 'ancestor':
                path_boards = [p[0] for p in path]
                if next_state[0] in path_boards:                      
                    continue

            #! push new tuple into strategy
            strategy.push((next_state, state, new_path))
            num_nodes_gen += 1

        #> uncomment to print num of nodes generated after each node expansion
        #print(num_nodes_gen)
    return None

#------------Algorithms------------

#! aziz: updated the arguments
def breadthFirstSearch(problem, pruning = 'none'): return generalSearch(problem, Queue(), pruning)

def depthFirstSearch(problem, pruning = 'none'): return generalSearch(problem, Stack(), pruning)


#! aziz: modified search to allow pruning. added full, ancestor and parent. EXTRA work - algo not required
def iterativeDeepeningSearch(problem, pruning = 'none'):
    num_nodes_exp = 0
    num_nodes_gen = 1
    def depthLimitedDFS(problem, state, depth, parent=None, path=None, presentSet=None):
        if path is None: path = [state]
        nonlocal num_nodes_gen, num_nodes_exp
        num_nodes_exp += 1
        if problem.isGoalState(state): return state
        if depth <= 0: return None
        for move in problem.getSuccessors(state):
            next_state = move #!#! nawaf: changed next_state to move because otherwise each iteration will remove all state node information except the first one. 
            #! similar pruning logic cf. generalSearch
            if pruning == 'full':
                board_tuple = tuple(next_state[0])
                if board_tuple in presentSet and presentSet[board_tuple] >= depth - 1:
                    continue
                presentSet[board_tuple] = depth - 1

            elif pruning == 'parent' and parent is not None and next_state[0] == parent[0]: 
                continue
            
            elif pruning == 'ancestor':
                path_boards = [p[0] for p in path]
                if next_state[0] in path_boards: 
                    continue            
            
            num_nodes_gen += 1
            solution = depthLimitedDFS(problem, next_state, depth-1, state, path + [next_state], presentSet)
            if solution is not None: 
                return solution
        return None

    depth = 1
    while True:
        #! reset the explored presentSet every iteration
        presentSet = {tuple(problem.getStartState()[0]): depth} if pruning == 'full' else None
        
        solution = depthLimitedDFS(problem, problem.getStartState(), depth, presentSet=presentSet)
        if solution is not None:
            return (solution, num_nodes_exp, num_nodes_gen)
        depth += 1


def uniformCostSearch(problem, pruning = 'none'):
    #!----Halla : added isinstance checking and path cost for the MTP
    #! aziz: cost = just length of the path = node[2] for all problem instances    
    if isinstance(problem, MagicTriangleProblem ):
        pathCost = lambda state: (len(state[2]))
        
    return generalSearch(problem, PriorityQueue(pathCost), pruning)


def greedySearch(problem, heuristic, pruning = 'none'):
    
    #return generalSearch(problem, PriorityQueue( lambda node: heuristic(node[1])), pruning)
    return generalSearch(problem, PriorityQueue(heuristic), pruning)

def astarSearch(problem, heuristic, pruning = 'none'):
    # the given function uses the number of steps as g-cost (uniform cost)
    # the number of elements in a state changes for different problems, hence
    # the following checks
    
    #! xx--Halla : added isinstance checking and path cost for the MTP--xx
    #! aziz: cost = just length of the path = node[2] for all problem instances + heuristic
    
    # totalCost = lambda node: len(node[1]) + heuristic(node[1])            
    # return generalSearch(problem, PriorityQueue(totalCost), pruning)
    
    if isinstance(problem, MagicTriangleProblem ):
        totalCost = lambda state: (len(state[2])) + heuristic(state)
    
    return generalSearch(problem, PriorityQueue(totalCost), pruning)