# CMP 333 - Project 1: Sokoban Puzzle Problem
# Aref

from AI_problem import SearchProblem

class SokobanPuzzleProblem(SearchProblem):

    def __init__(self, board):
        """
        Parse the board (list of strings) into walls, goals, boxes, and player.
        Handles: '#' wall, '.' goal, '$' box, '@' player,
                 '*' box-on-goal, '+' player-on-goal
        """
        self.walls = set()
        self.goals = set()
        boxes = set()
        player_pos = None

        for row in range(len(board)):
            for col in range(len(board[row])):
                char = board[row][col]
                if char == '#':
                    self.walls.add((row, col))
                elif char == '.':
                    self.goals.add((row, col))
                elif char == '$':
                    boxes.add((row, col))
                elif char == '@':
                    player_pos = (row, col)
                elif char == '*':          # box already on a goal
                    self.goals.add((row, col))
                    boxes.add((row, col))
                elif char == '+':          # player standing on a goal
                    self.goals.add((row, col))
                    player_pos = (row, col)

        self.start_player = player_pos
        self.start_boxes  = frozenset(boxes)

    # ------------------------------------------------------------------ #

    def getStartState(self):
        #! aziz: matching state tuple in generalSearch
        return ((self.start_player, self.start_boxes), [])
    # ------------------------------------------------------------------ #

    def isGoalState(self, state):
        #! aziz: extract the physical board from index 0
        physical_board = state[0]
        _, boxes = physical_board
        return boxes == self.goals   #! every box sits on a goal

    # ------------------------------------------------------------------ #

    def getSuccessors(self, state):
        """
        Returns list of (successor_state, action, step_cost).
        Each move costs 1.
        Directions: up = row-1, down = row+1, left = col-1, right = col+1
        """
        physical_board, path = state
        player_pos, boxes = physical_board
        successors = []

        directions = {
            'up':    (-1,  0),
            'down':  ( 1,  0),
            'left':  ( 0, -1),
            'right': ( 0,  1),
        }

        for action, (dr, dc) in directions.items():
            row, col = player_pos
            next_pos = (row + dr, col + dc)

            #! Can't walk into a wall
            if next_pos in self.walls:
                continue

            new_boxes = set(boxes)

            if next_pos in boxes:
                #! There's a box — try to push it
                box_next = (row + 2*dr, col + 2*dc)

                #! Box can't be pushed into a wall or another box
                if box_next in self.walls or box_next in boxes:
                    continue

                #! Valid push: move box forward, player steps into box's old spot
                new_boxes.remove(next_pos)
                new_boxes.add(box_next)
            
            new_path = list(path)
            new_path.append(action)
            
            #! aziz: matching generalSearch structure
            new_state = ((next_pos, frozenset(new_boxes)), new_path)
            successors.append(new_state)

        return successors

    # ------------------------------------------------------------------ #

    def getHeuristics(self):
        """Return a list of heuristic functions."""
        return [self._manhattanDistance]

    def _manhattanDistance(self, state):
        """
        Sum of Manhattan distances from each box to its nearest goal.
        This is admissible (never overestimates) since each box needs
        at least that many moves to reach some goal.
        """
        _, boxes = state[0]
        total = 0
        for box in boxes:
            nearest = min(
                abs(box[0] - g[0]) + abs(box[1] - g[1])
                for g in self.goals
            )
            total += nearest
        return total
