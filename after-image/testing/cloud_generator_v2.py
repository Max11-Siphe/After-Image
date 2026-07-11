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
    
    solv, base_len, base_path, base_states = solve_puzzle(
        m1_lines, m1_spawn, m1_goal,
        m2_lines, m2_spawn, m2_goal
    )
    print(f"Baseline Cloud Path Length: {base_len} inputs")
    
    # Try adding/removing walls in maze 1 or maze 2
    # Only in rows 1 to 9, cols 1 to 23
    # Do not touch spawn or goal
    candidates = []
    for y in range(1, 10):
        for x in range(1, 24):
            candidates.append((x, y))
            
    print(f"Searching {len(candidates)} cells for wall modifications...")
    
    improvements = []
    
    for x, y in candidates:
        # Maze 1 modifications
        if (x, y) != m1_spawn and (x, y) != m1_goal:
            current_char = m1_lines[y][x]
            next_char = '#' if current_char == '.' else '.'
            
            test_m1 = [list(row) for row in m1_lines]
            test_m1[y][x] = next_char
            test_m1_str = ["".join(row) for row in test_m1]
            
            solv, length, path, states = solve_puzzle(
                test_m1_str, m1_spawn, m1_goal,
                m2_lines, m2_spawn, m2_goal
            )
            if solv and length > base_len:
                improvements.append(('m1', x, y, current_char, next_char, length))
                
        # Maze 2 modifications
        if (x, y) != m2_spawn and (x, y) != m2_goal:
            current_char = m2_lines[y][x]
            next_char = '#' if current_char == '.' else '.'
            
            test_m2 = [list(row) for row in m2_lines]
            test_m2[y][x] = next_char
            test_m2_str = ["".join(row) for row in test_m2]
            
            solv, length, path, states = solve_puzzle(
                m1_lines, m1_spawn, m1_goal,
                test_m2_str, m2_spawn, m2_goal
            )
            if solv and length > base_len:
                improvements.append(('m2', x, y, current_char, next_char, length))
                
    # Sort and print improvements
    improvements.sort(key=lambda x: x[5], reverse=True)
    print(f"Found {len(improvements)} improvements:")
    for imp in improvements[:15]:
        print(f"Maze {imp[0]} at ({imp[1]}, {imp[2]}): change '{imp[3]}' to '{imp[4]}' -> New Length: {imp[5]} inputs")

if __name__ == "__main__":
    main()
