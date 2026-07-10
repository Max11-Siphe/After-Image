#!/usr/bin/env python3
"""
City maze improvement: make City harder than Cloud (113 inputs).
Target: City shortest solution > 120 inputs.
Strategy: Redesign maze_1_city or maze_2_city to force longer paths.
Keep spawns and goals at their current positions.

Current City:
- maze_1_city: S=(1,1) G=(11,5)  
- maze_2_city: S=(1,1) G=(1,3)
Current: 107 inputs. Need > 113.
"""
import os
from validator import validate_map_layout, solve_puzzle, calculate_metrics, extract_map_string

def test(m1_str, m2_str, label):
    m1_lines, m1_spawn, m1_goal, e1 = validate_map_layout(m1_str, "m1")
    m2_lines, m2_spawn, m2_goal, e2 = validate_map_layout(m2_str, "m2")
    if e1 or e2:
        print(f"  {label}: INVALID — {e1 + e2}")
        return None
    solv, length, path, states = solve_puzzle(m1_lines, m1_spawn, m1_goal, m2_lines, m2_spawn, m2_goal)
    if solv:
        reachable, m1j, m2j = calculate_metrics(m1_lines, m1_spawn, m2_lines, m2_spawn)
        dc = sum(1 for i in range(1, len(path)) if path[i] != path[i-1])
        print(f"  {label}: {length} inputs | {reachable} reachable | junc {m1j}/{m2j} | dc {dc}")
        print(f"    C1: {m1_spawn}->{m1_goal}  C2: {m2_spawn}->{m2_goal}")
        return {'length': length, 'states': states, 'reachable': reachable, 'dc': dc, 'path': path, 'm1': m1_str, 'm2': m2_str}
    else:
        print(f"  {label}: Solvable NO (searched: {states})")
        return None

# Original city mazes
M1_ORIG_STR, _ = extract_map_string(os.path.join("levels", "maze_1_city.tscn"))
M2_ORIG_STR, _ = extract_map_string(os.path.join("levels", "maze_2_city.tscn"))

# Maze 2 variants: keep S=(1,1) G=(1,3) but add more complexity
# M2-A: Add extra dead-ends and more junctions in the middle
M2_A = """#########################
#S..#.........#.....#.###
###.###.#####.###.#.#.###
#G#.#...#...#...#.#.#.###
#.#.#.###.#.###.#.#.#.###
#.#...#...#...#...#.#.###
#.#####.#.#.#######.#.###
#.....#.#.#.#.#.....#.###
#.#.###.#.###.#.#####.###
#.#.....#.............###
#########################
#.#########.#########.###
#.......................#
#########################"""

# M2-B: More walls blocking direct routes
M2_B = """#########################
#S..#.........#.....#.###
###.###.#####.###.#.#.###
#G#.#...#...#...#.#.#.###
#.#.#.###.#.###.#.#.#.###
#.#.#.#...#.#...#.#.#.###
#.#.###.#.#.#.###.###.###
#.....#.#.#.#.#.....#.###
#.#.###.#.###.#.#####.###
#.#.....#...........####
#########################
#.#########.#########.###
#.......................#
#########################"""

# M2-C: Force character 2 through upper-right before reaching goal at (1,3)
M2_C = """#########################
#S..#.....#...#.....#.###
###.###.###.#.###.#.#.###
#G#.#...#...#...#.#.#.###
#.#.#.###.#.###.#.#.#.###
#.#...#...#...#...#.#.###
#.#####.#.#.#######.#.###
#.....#.#.#.#.......#.###
#.#.###.#.###.#######.###
#.#.....#.............###
#########################
#.#########.#########.###
#.......................#
#########################"""

# M1 variants: keep S=(1,1) G=(11,5) but restructure routes
M1_A = """#########################
#S....#.....#.........###
#####.#.###.#.###.#######
#...#...#...#...#.....###
#.#.#####.###.#####.#.###
#.#.....#.#G..#...#.#.###
#.#####.#.###.#.#.###.###
#.....#.#.#...#.#.....###
#.###.###.#.#########.###
#...#.......#.........###
#########################
#.#########.#########.###
#.......................#
#########################"""

M1_B = """#########################
#S....#.....#.........###
#####.#.###.#.###.#######
#...#.#.#...#...#.....###
#.#.#.###.###.#####.#.###
#.#...#...#G..#...#.#.###
#.#####.#.#####.#.###.###
#.....#.#.#.....#.....###
#.###.###.#.#########.###
#...#.......#.........###
#########################
#.#########.#########.###
#.......................#
#########################"""

if __name__ == "__main__":
    print("Baseline City:")
    r0 = test(M1_ORIG_STR, M2_ORIG_STR, "Orig+Orig")
    print()
    
    results = []
    combos = [
        ("M1Orig+M2A", M1_ORIG_STR, M2_A),
        ("M1Orig+M2B", M1_ORIG_STR, M2_B),
        ("M1Orig+M2C", M1_ORIG_STR, M2_C),
        ("M1A+M2Orig", M1_A, M2_ORIG_STR),
        ("M1B+M2Orig", M1_B, M2_ORIG_STR),
        ("M1A+M2C", M1_A, M2_C),
        ("M1B+M2C", M1_B, M2_C),
    ]
    for label, m1, m2 in combos:
        r = test(m1, m2, label)
        if r:
            results.append((label, r))
    
    print()
    print("=== RANKING BY LENGTH ===")
    results.sort(key=lambda x: x[1]['length'], reverse=True)
    for label, r in results[:5]:
        print(f"  {label}: length={r['length']}, reachable={r['reachable']}, dc={r['dc']}")
