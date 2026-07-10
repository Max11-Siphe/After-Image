#!/usr/bin/env python3
"""
Final Cloud maze improvement: analytically designed maze_2_cloud
with same spawn (1,1) and goal (21,9) but more complex topology.

Design goals for maze_2:
- Many more junctions (increase from 9 to 12+)
- Longer minimum path by requiring character to visit multiple rooms
- More walls creating asymmetry with maze_1
- No shortcuts that reduce the combined solution length
- Maintain 25×14 and all borders solid
"""
import os
import sys
from validator import validate_map_layout, solve_puzzle

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

# Completely redesigned maze_2 with:
# - Many more junctions (15+)
# - Spawn at (1,1), Goal at (21,9)  
# - Long winding path forced by walls
# - Strong asymmetry vs maze_1
MAZE2_REDESIGN = [
    # Design D: Dense web layout - many junctions, long forced path
    """#########################
#S.#...#...#...#...#.####
#.##.#.#.#.#.#.#.#.#.####
#....#...#...#...#...####
###.####.####.####.######
#...#....#....#....#.####
#.#.#.##.#.##.#.##.#.####
#.#...#..#.#..#.#..#.####
#.#####.##.##.##.########
#.........#.......#.G####
#########################
#.#########.#########.###
#.......................#
#########################""",

    # Design E: Maze 2 with horizontal layers + many connectors
    """#########################
#S...................####
#.#.###.###.###.###.#####
#.#.#...#...#...#.#.#####
#.#.#.###.###.###.#.#####
#.#.#.#...#...#...#.#####
#.###.#.###.###.###.#####
#.#...#.#...#...#...#####
#.#.###.#.###.###.#######
#...............#....G###
#########################
#.#########.#########.###
#.......................#
#########################""",

    # Design F: Force character 2 through a maze that zig-zags vertically
    # many times before reaching goal at (21,9)
    """#########################
#S.#...................##
#.##.##########.########
#.#.#...........#......#
#.#.#.##########.######.#
#.#.#.#...........#....##
#.#.#.#.##########.####.#
#.#.#.#.#.......#.#...#.#
#.#.#.#.#.#####.#.#.###.#
#.........#...#...#..G..#
#########################
#.#########.#########.###
#.......................#
#########################""",

    # Design G: Realistic hard maze with many branching corridors
    # Spawn (1,1), Goal (21,9)
    """#########################
#S.#...#...#...........##
#.##.#.#.#.#.#####.#####
#....#.#.#...#.....#.####
###.##.#.#.###.###.#.####
#...#..#.#...#.#...#.####
#.###.##.#.#.#.#.###.####
#.#...#..#.#...#.#...####
#.#.###.##.#####.#.######
#...#.......#....#.G.####
#########################
#.#########.#########.###
#.......................#
#########################""",

    # Design H: Use the existing maze_2_cloud but remove 2 shortcuts
    # that allow the solver to take easy paths
    # Original had shortcut corridors at rows 6-7; we wall them off
    """#########################
#S#.....#.......#.....###
#.#.#####.#.###.#.###.###
#.#...#...#...#...#.#.###
#.#.#.#.#####.#####.#.###
#.#.#.......#.#.#...#.###
#.###########.#.#.#.#.###
#.....#.....#.#.#.#...###
#####.#.###.###.#.#######
#.......#.......#....G###
#########################
#.#########.#########.###
#.......................#
#########################""",

    # Design I: Force character 2 through top-right quadrant detour
    """#########################
#S#.....#...#...#.....###
#.#.#####.#.#.#.#.###.###
#.#...#...#.#.#...#.#.###
#.#.#.#.###.###.###.#.###
#.#.#...#...#.#.#...#.###
#.#######.#.#.#.#.#.#.###
#.....#...#.#...#.#...###
#####.#.###.#####.#######
#.......#.......#....G###
#########################
#.#########.#########.###
#.......................#
#########################""",
]

def test_candidate(maze2_str, label):
    m2_lines, m2_spawn, m2_goal, errors = validate_map_layout(maze2_str, f"m2_{label}")
    if errors:
        print(f"  INVALID: {errors}")
        return None, None
    m1_lines, m1_spawn, m1_goal, _ = validate_map_layout(MAZE1, "m1")
    solv, length, path, states = solve_puzzle(m1_lines, m1_spawn, m1_goal, m2_lines, m2_spawn, m2_goal)
    if solv:
        print(f"  Solvable: YES, Length: {length}, States: {states}, C2 spawn:{m2_spawn} goal:{m2_goal}")
        return length, path
    else:
        print(f"  Solvable: NO (states: {states}), C2 spawn:{m2_spawn} goal:{m2_goal}")
        return None, None

if __name__ == "__main__":
    baseline_m1, m1_spawn, m1_goal, _ = validate_map_layout(MAZE1, "m1")
    
    # Get baseline
    # Use original maze_2_cloud
    import os
    from validator import extract_map_string
    m2_orig_str, _ = extract_map_string(os.path.join("levels", "maze_2_cloud.tscn"))
    m2_orig, m2_spawn, m2_goal, _ = validate_map_layout(m2_orig_str, "orig")
    s, bl, bp, bst = solve_puzzle(baseline_m1, m1_spawn, m1_goal, m2_orig, m2_spawn, m2_goal)
    print(f"Original Cloud: {bl} inputs, {bst} states")
    print()
    
    labels = "DEFGHI"
    best = (bl, None, None)
    for i, cand in enumerate(MAZE2_REDESIGN):
        label = labels[i]
        print(f"Design {label}:")
        length, path = test_candidate(cand, label)
        if length and length > best[0]:
            best = (length, path, cand)
    
    print()
    if best[1]:
        found_label = labels[MAZE2_REDESIGN.index(best[2])]
        print(f"Best improvement: Design {found_label} with {best[0]} inputs")
        print(f"Solution: {' -> '.join(best[1])}")
    else:
        print("No improvement found over baseline.")
