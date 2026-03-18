##############################################################################
###
###   TEST ALL SOKOBAN PUZZLES
###
###   Loads and tests all puzzle files in Sokoban_boards/
###

import os
from SokobanPuzzleProblem import SokobanPuzzleProblem

def load_puzzle(filepath):
    """Load a puzzle from a .txt file."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    # Remove empty lines and strip newlines
    board = [line.rstrip('\n') for line in lines if line.strip()]
    return board

def test_puzzle(filepath):
    """Test a single puzzle file."""
    puzzle_name = os.path.basename(filepath)

    try:
        board = load_puzzle(filepath)
        problem = SokobanPuzzleProblem(board)

        # Get start state
        start = problem.getStartState()
        player_pos, boxes = start

        # Get heuristic
        heuristics = problem.getHeuristics()
        h_value = heuristics[0](start)

        # Get successors
        successors = problem.getSuccessors(start)

        print(f"✓ {puzzle_name}")
        print(f"  Player: {player_pos}, Boxes: {len(boxes)}, Goals: {len(problem.goals)}")
        print(f"  Heuristic: {h_value}, Possible moves: {len(successors)}")

        return True
    except Exception as e:
        print(f"✗ {puzzle_name}: {e}")
        return False

if __name__ == "__main__":
    puzzle_dir = "Sokoban_boards"

    if not os.path.exists(puzzle_dir):
        print(f"Puzzle directory '{puzzle_dir}' not found!")
        exit(1)

    # Get all puzzle files
    puzzle_files = sorted([
        os.path.join(puzzle_dir, f)
        for f in os.listdir(puzzle_dir)
        if f.endswith('.txt') and 'output' not in f
    ])

    print("=" * 60)
    print("TESTING ALL SOKOBAN PUZZLES")
    print("=" * 60 + "\n")

    passed = 0
    failed = 0

    for puzzle_file in puzzle_files:
        if test_puzzle(puzzle_file):
            passed += 1
        else:
            failed += 1
        print()

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
