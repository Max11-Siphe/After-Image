#!/usr/bin/env python3
import os
import sys
from validator import extract_map_string, validate_map_layout, solve_puzzle

def main():
    m1_path = os.path.join("levels", "maze_1_cloud.tscn")
    m2_path = os.path.join("levels", "maze_2_cloud.tscn")
    
    m1_str, _ = extract_map_string(m1_path)
    m2_str, _ = extract_map_string(m2_path)
    
    m1_lines, m1_spawn, m1_goal, _ = validate_map_layout(m1_str, "m1")
    m2_lines, m2_spawn, m2_goal, _ = validate_map_layout(m2_str, "m2")
    
    # Run baseline solver
    solv, base_len, base_path, base_states = solve_puzzle(
        m1_lines, m1_spawn, m1_goal,
        m2_lines, m2_spawn, m2_goal
    )
    print(f"Baseline Cloud Path Length: {base_len} inputs")
    
    best_len = base_len
    best_m1 = list(m1_lines)
    best_m2 = list(m2_lines)
    
    # Try adding/removing walls in maze 1 or maze 2
    # Only in rows 1 to 9, cols 1 to 23
    # Do not touch spawn or goal
    candidates = []
    for y in range(1, 10):
        for x in range(1, 24):
            candidates.append((x, y))
            
    print(f"Searching for wall modifications to increase length...")
    
    # Let's try placing single wall additions in Maze 1 that block certain paths
    # and force longer coordination.
    found_improvements = []
    
    for x, y in candidates:
        # Check Maze 1
        if m1_lines[y][x] == '.':
            # Try placing a wall here
            test_m1 = [list(row) for row in m1_lines]
            test_m1[y][x] = '#'
            test_m1_str = ["".join(row) for row in test_m1]
            
            solv, length, path, states = solve_puzzle(
                test_m1_str, m1_spawn, m1_goal,
                m2_lines, m2_spawn, m2_goal
            )
            
            if solv and length > best_len:
                found_improvements.append(('m1_wall', x, y, length))
                
        # Check Maze 2
        if m2_lines[y][x] == '.':
            # Try placing a wall here
            test_m2 = [list(row) for row in m2_lines]
            test_m2[y][x] = '#'
            test_m2_str = ["".join(row) for row in test_m2]
            
            solv, length, path, states = solve_puzzle(
                m1_lines, m1_spawn, m1_goal,
                test_m2_str, m2_spawn, m2_goal
            )
            
            if solv and length > best_len:
                found_improvements.append(('m2_wall', x, y, length))
                
    # Sort improvements by length
    found_improvements.sort(key=lambda x: x[3], reverse=True)
    for imp in found_improvements[:10]:
        print(f"Type: {imp[0]} at ({imp[1]}, {imp[2]}), New Length: {imp[3]}")

if __name__ == "__main__":
    main()
