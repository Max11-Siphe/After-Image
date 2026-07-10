#!/usr/bin/env python3
"""
Targeted Cloud maze improvement tool.
Strategy: Move maze_2_cloud's spawn/goal positions to create more
combined-state complexity, OR redesign parts of maze_2_cloud to
add more meaningful junctions without making it unsolvable.

We want Cloud to be clearly harder than City (107 inputs).
Current Cloud: 113 inputs. We want 130+ inputs.

Approach: Redesign maze_2_cloud.tscn to have a more complex layout
with more junctions, while keeping maze_1_cloud unchanged.
Then validate the new pair.
"""
import os
import sys
from validator import validate_map_layout, solve_puzzle

# Current maze_1_cloud (UNCHANGED - this stays the same)
MAZE1 = """#########################
#S..#.................###
###.#####.###.#######.###
#.#.....#.#.#.....#...###
#.#####.#.#.#####.#.#####
#.#...#.#.......#.#.#G###
#.#.#.#.#######.#.#.#.###
#...#.#...#...#.#.#.#.###
#.###.###.#.#.###.#.#.###
#...#.......#.....#...###
#########################
#.#########.#########.###
#.......................#
#########################"""

# Proposed maze_2_cloud redesign:
# Keep S at (1,1), G at (21,9) but with a MUCH more complex path
# Key changes vs original maze_2:
#   - Added more dead-end branches to create misleading paths
#   - Added more junctions at key crossroads
#   - Increased distance between corridors that lead to goal
#   - Added more walls forcing asymmetric character moves
MAZE2_CANDIDATES = [
    # Candidate A: More complex routing in upper half, forcing more backtracking
    """#########################
#S#.....#.......#.....###
#.#.###.#.#####.#.###.###
#.#.#.#...#...#...#.#.###
#.#.#.#.###.#.#####.#.###
#.#.#...#.#.#.#...#.#.###
#.#.#####.#.#.#.#.###.###
#.....#...#.#.#.#.#...###
#####.#.#.###.#.#.#######
#.......#.......#....G###
#########################
#.#########.#########.###
#.......................#
#########################""",
    # Candidate B: Add extra wall at (7,4) to block shortcut in upper area
    """#########################
#S#.....#.......#.....###
#.#.#####.#.###.#.###.###
#.#...#...#...#...#.#.###
#.#.#.#.#####.#####.#.###
#.#.#.......#...#...#.###
#.###########.#.#.#.#.###
#.....#.....#.#.#.#...###
#####.#.#####.#.#.#######
#.......#.......#....G###
#########################
#.#########.#########.###
#.......................#
#########################""",
    # Candidate C: Modified middle to force longer detour around center
    """#########################
#S#.....#.......#.....###
#.#.#####.#.###.#.###.###
#.#...#...#...#...#.#.###
#.#.#.#.#####.#####.#.###
#.#.###.....#.#.#...#.###
#.#.#####.#.#.#.#.###.###
#.....#...#.#.#.#.#...###
#####.#.#.###.#.#.#######
#.......#.......#....G###
#########################
#.#########.#########.###
#.......................#
#########################""",
]

def test_candidate(maze2_str, maze2_label):
    m2_lines, m2_spawn, m2_goal, errors = validate_map_layout(maze2_str, f"maze2_{maze2_label}")
    if errors:
        print(f"  INVALID: {errors}")
        return None, None, None
        
    m1_lines, m1_spawn, m1_goal, _ = validate_map_layout(MAZE1, "maze1")
    
    solv, length, path, states = solve_puzzle(
        m1_lines, m1_spawn, m1_goal,
        m2_lines, m2_spawn, m2_goal
    )
    
    if solv:
        print(f"  Solvable: YES, Length: {length} inputs, States: {states}")
        print(f"  C1 spawn:{m1_spawn} goal:{m1_goal} | C2 spawn:{m2_spawn} goal:{m2_goal}")
        return length, path, m2_lines
    else:
        print(f"  Solvable: NO (states searched: {states})")
        return None, None, None

if __name__ == "__main__":
    print("Testing Cloud Maze 2 candidates:")
    print()
    
    best_length = 0
    best_idx = -1
    best_path = None
    
    for i, candidate in enumerate(MAZE2_CANDIDATES):
        print(f"Candidate {chr(65+i)}:")
        length, path, lines = test_candidate(candidate, chr(65+i))
        if length and length > best_length:
            best_length = length
            best_idx = i
            best_path = path
            
    print()
    if best_idx >= 0:
        print(f"Best candidate: {chr(65+best_idx)} with {best_length} inputs")
        print(f"Solution: {' -> '.join(best_path)}")
    else:
        print("No valid candidate found")
