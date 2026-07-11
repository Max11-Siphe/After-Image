#!/usr/bin/env python3
"""
Complete Cloud maze pair redesign.
Goal: Create a solvable pair with ≥ 120 combined steps AND > 11697 reachable states
(to beat Dungeon on at least one metric).

Strategy: Keep spawn at (1,1) for both mazes.
Redesign BOTH mazes with more junctions and longer forced paths.
The key: maze_1 and maze_2 must create high combined-state complexity.

We want:
- shortest solution > 117 (Dungeon), ideally 125+
- OR reachable states > 11697
- AND dir_changes > 45 (Dungeon)

Multiple candidates tested.
"""
import os
from validator import validate_map_layout, solve_puzzle, calculate_metrics

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
        asym = 0
        c1x,c1y = m1_spawn; c2x,c2y = m2_spawn
        mv = {'Up':(0,-1),'Down':(0,1),'Left':(-1,0),'Right':(1,0)}
        for mn in path:
            dx,dy = mv[mn]
            n1x,n1y = c1x+dx,c1y+dy
            w1 = 0<=n1x<25 and 0<=n1y<14 and m1_lines[n1y][n1x]!='#'
            n2x,n2y = c2x-dx,c2y-dy
            w2 = 0<=n2x<25 and 0<=n2y<14 and m2_lines[n2y][n2x]!='#'
            if not w1 or not w2: asym+=1
            if w1: c1x,c1y=n1x,n1y
            if w2: c2x,c2y=n2x,n2y
        print(f"  {label}: {length} inputs | {states} searched | {reachable} reachable | junc {m1j}/{m2j} | dc {dc} | asym {asym}")
        print(f"    C1: {m1_spawn}->{m1_goal}  C2: {m2_spawn}->{m2_goal}")
        return {'length': length, 'states': states, 'reachable': reachable, 'dc': dc, 'asym': asym, 'path': path, 'm1': m1_str, 'm2': m2_str}
    else:
        print(f"  {label}: Solvable NO (searched: {states})")
        return None

# ---------- MAZE 1 VARIANTS ----------

# M1-A: Original maze_1_cloud
M1_ORIG = """#########################
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

# M1-B: More junctions in upper-right, longer forced path to goal
M1_B = """#########################
#S..#.................###
###.#####.###.#######.###
#.#.....#.#.#.....#...###
#.#####.#.#.#####.#.#####
#.#...#.#...#...#.#.#G###
#.#.#.#.#####.#.#.#.#.###
#...#.#...#...#.#.#.#.###
#.###.###.#.#.###.#.#.###
#...#.......#.....#...###
#########################
#.#########.#########.###
#.......................#
#########################"""

# M1-C: Added extra junction, slightly more complex
M1_C = """#########################
#S..#.....#...........###
###.#####.#.###.#######.#
#.#.....#.#.#.#.....#...#
#.#####.#.#.#.#####.#.###
#.#...#.#.......#.#.#G###
#.#.#.#.#######.#.#.#.###
#...#.#...#...#.#.#.#.###
#.###.###.#.#.###.#.#.###
#...#.......#.....#...###
#########################
#.#########.#########.###
#.......................#
#########################"""

# ---------- MAZE 2 VARIANTS ----------

# M2-ORIG: Original maze_2_cloud
M2_ORIG = """#########################
#S#.....#.......#.....###
#.#.#####.#.###.#.###.###
#.#...#...#...#...#.#.###
#.#.#.#.#####.#####.#.###
#.#.#.......#...#...#.###
#.###########.#.#.#.#.###
#.....#.....#.#.#.#...###
#####.#.###.###.#.#######
#.......#.......#....G###
#########################
#.#########.#########.###
#.......................#
#########################"""

# M2-B: Modified to have extra detour on the right side
M2_B = """#########################
#S#.....#.......#.....###
#.#.#####.#.###.#.###.###
#.#...#...#...#...#.#.###
#.#.#.#.#####.#####.#.###
#.#.#...#...#...#...#.###
#.###.###.#.#.#.#.#.#.###
#.....#...#.#.#.#.#...###
#####.#.###.###.#.#######
#.......#.......#....G###
#########################
#.#########.#########.###
#.......................#
#########################"""

# M2-C: Extra wall forcing a longer detour around center-right
M2_C = """#########################
#S#.....#.......#.....###
#.#.#####.#.###.#.###.###
#.#...#...#...#.#.#.#.###
#.#.#.#.#####.#.#.#.#.###
#.#.#...#...#.#.#...#.###
#.###.###.#.#.#.#.###.###
#.....#...#.#.#.#.#...###
#####.#.###.###.#.#######
#.......#.......#....G###
#########################
#.#########.#########.###
#.......................#
#########################"""

# M2-D: Entire upper section restructured for more forced routing
M2_D = """#########################
#S#.....#...#...#.....###
#.#.#####.#.#.#.#.###.###
#.#...#...#.#.#...#.#.###
#.#.#.#.###.###.###.#.###
#.#.#...#.#.#.#.#...#.###
#.###.###.#.#.#.#.#.#.###
#.....#...#...#.#.#...###
#####.#.###.###.#.#######
#.......#.......#....G###
#########################
#.#########.#########.###
#.......................#
#########################"""

if __name__ == "__main__":
    results = []
    combos = [
        ("Orig+Orig", M1_ORIG, M2_ORIG),
        ("Orig+M2B", M1_ORIG, M2_B),
        ("Orig+M2C", M1_ORIG, M2_C),
        ("Orig+M2D", M1_ORIG, M2_D),
        ("M1B+Orig", M1_B, M2_ORIG),
        ("M1B+M2B", M1_B, M2_B),
        ("M1B+M2C", M1_B, M2_C),
        ("M1B+M2D", M1_B, M2_D),
        ("M1C+Orig", M1_C, M2_ORIG),
        ("M1C+M2D", M1_C, M2_D),
    ]
    
    for label, m1, m2 in combos:
        r = test(m1, m2, label)
        if r:
            results.append((label, r))
    
    print()
    print("=== RANKING BY LENGTH ===")
    results.sort(key=lambda x: x[1]['length'], reverse=True)
    for label, r in results[:5]:
        print(f"  {label}: length={r['length']}, reachable={r['reachable']}, dc={r['dc']}, asym={r['asym']}")
