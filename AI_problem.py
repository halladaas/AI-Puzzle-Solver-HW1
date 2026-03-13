##############################################################################
###
###   CMP 333 PROJECT 1 -- SEARCH
###
###   ABSTRACT PROBLEM CLASS used with various AI search algorithms
###
###   Michel Pasquier 2019, adapted from the code @
###   https://kartikkukreja.wordpress.com/2015/06/14/heuristics-in-ai-search/
###


from abc import ABC, abstractmethod

class SearchProblem (ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def getStartState(self): pass

    @abstractmethod
    def isGoalState(self, state): pass

    @abstractmethod
    def getSuccessors(self, state): pass

    # added a function to return a list of compatible heuristics
    def getHeuristics(self): pass

###