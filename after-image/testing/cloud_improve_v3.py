#!/usr/bin/env python3
"""
Cloud level difficulty booster.
Since single-maze changes only yield marginal improvements,
try simultaneous changes to BOTH maze_1_cloud and maze_2_cloud.

Strategy: 
1. Move spawn/goal positions to create fundamentally different topology
2. Redesign maze_2 to have the goal in a corner position
3. Maximize combined-state complexity (reachable states * direction changes)
"""
import os
from validator import validate_map_layout, solve_puzzle, extract_map_string, calculate_metrics

# Original maze_1_cloud (keep unchanged)
M1_ORIGINAL = """#########################
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

# Proposed maze_2_cloud with:
# - Spawn moved to (23,1) instead of (1,1) — mirrors maze_1 better
# - Goal at (1,8) — opposite corner from spawn
# - Dense corridor network with many junctions
# Both mazes now have spawns on OPPOSITE sides, forcing very different movement needs
M2_WITH_MIRRORED_SPAWN = """#########################
#......................S#
#.#####.#####.#####.###.#
#.#.....#...#.#...#.#...#
#.#.#####.#.#.#.#.###.#.#
#...#.....#.#...#.#...#.#
#.###.#####.#####.#.###.#
#.#...#.........#.#.#...#
#.#.#.###.#####.#.#.#.###
#G..#.....#.......#.....#
#########################
#.#########.#########.###
#.......................#
#########################"""

# Also try: Maze 2 spawn at top-right, goal at bottom-left
M2_TOPLEFT_SPAWN = """#########################
#S.....#.......#.....###
#.#####.#.#####.#.#######
#.#.....#.#.....#.#...###
#.#.###.#.#.###.#.#.#####
#.#.#...#.#.#...#.#.#G###
#.#.###.#.#.###.#.#.#####
#.#.....#.#.....#.#...###
#.#######.#######.#.#####
#.....................####
#########################
#.#########.#########.###
#.......................#
#########################"""

# New maze_2: more junctions, goal at (21,12) instead of (21,9)
# Longer path to goal through bottom section
M2_DEEPER_GOAL = """#########################
#S#.....#.......#.....###
#.#.#####.#.###.#.###.###
#.#...#...#...#...#.#.###
#.#.#.#.#####.#####.#.###
#.#.#.......#...#...#.###
#.###########.#.#.#.#.###
#.....#.....#.#.#.#...###
#####.#.###.###.#.#######
#.......#.......#.....###
#########################
#.###########.#######.###
#.....................G##
#########################"""

def test(m1_str, m2_str, label):
    m1_lines, m1_spawn, m1_goal, e1 = validate_map_layout(m1_str, "m1")
    m2_lines, m2_spawn, m2_goal, e2 = validate_map_layout(m2_str, "m2")
    if e1 or e2:
        print(f"  {label}: INVALID — {e1+e2}")
        return
    solv, length, path, states = solve_puzzle(m1_lines, m1_spawn, m1_goal, m2_lines, m2_spawn, m2_goal)
    if solv:
        reachable, m1j, m2j = calculate_metrics(m1_lines, m1_spawn, m2_lines, m2_spawn)
        # Count dir changes
        dc = sum(1 for i in range(1, len(path)) if path[i] != path[i-1])
        print(f"  {label}: Solvable YES, {length} inputs, {states} searched, {reachable} reachable states, junctions {m1j}/{m2j}, dir_changes {dc}")
        print(f"         C1: {m1_spawn}->{m1_goal}, C2: {m2_spawn}->{m2_goal}")
    else:
        print(f"  {label}: Solvable NO (states searched: {states})")

if __name__ == "__main__":
    print("Baseline (original both mazes):")
    m2_orig_str, _ = extract_map_string(os.path.join("levels", "maze_2_cloud.tscn"))
    test(M1_ORIGINAL, m2_orig_str, "Original")
    print()
    
    print("Candidates:")
    test(M1_ORIGINAL, M2_WITH_MIRRORED_SPAWN, "Mirrored-Spawn")
    test(M1_ORIGINAL, M2_TOPLEFT_SPAWN, "TopLeft-Spawn")
    test(M1_ORIGINAL, M2_DEEPER_GOAL, "Deeper-Goal (row 12)")
