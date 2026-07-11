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
    
    # We want to find a layout with shortest path > 120 and <= 150.
    # Let's collect candidates for modifications.
    # To reduce space, let's only modify maze 1 or maze 2, not both at the same time.
    # Let's list candidates in maze 1 first.
    m1_candidates = []
    for y in range(1, 10):
        for x in range(1, 24):
            if (x, y) != m1_spawn and (x, y) != m1_goal:
                m1_candidates.append((x, y))
                
    m2_candidates = []
    for y in range(1, 10):
        for x in range(1, 24):
            if (x, y) != m2_spawn and (x, y) != m2_goal:
                m2_candidates.append((x, y))
                
    print(f"Searching two-cell modifications for Maze 1 (candidates={len(m1_candidates)})...")
    
    found = []
    
    # Try 1-cell changes first
    for x1, y1 in m1_candidates:
        c1 = m1_lines[y1][x1]
        n1 = '#' if c1 == '.' else '.'
        
        test_m1 = [list(row) for row in m1_lines]
        test_m1[y1][x1] = n1
        test_m1_str = ["".join(row) for row in test_m1]
        
        s, length, path, states = solve_puzzle(
            test_m1_str, m1_spawn, m1_goal,
            m2_lines, m2_spawn, m2_goal
        )
        if s and length > base_len:
            found.append((length, [('m1', x1, y1, c1, n1)]))
            
    # Try 2-cell changes in Maze 1
    # To make it fast, let's look at pairs
    count = 0
    total_pairs = len(m1_candidates) * (len(m1_candidates) - 1) // 2
    for i in range(len(m1_candidates)):
        x1, y1 = m1_candidates[i]
        c1 = m1_lines[y1][x1]
        n1 = '#' if c1 == '.' else '.'
        
        for j in range(i + 1, len(m1_candidates)):
            x2, y2 = m1_candidates[j]
            c2 = m1_lines[y2][x2]
            n2 = '#' if c2 == '.' else '.'
            
            test_m1 = [list(row) for row in m1_lines]
            test_m1[y1][x1] = n1
            test_m1[y2][x2] = n2
            test_m1_str = ["".join(row) for row in test_m1]
            
            s, length, path, states = solve_puzzle(
                test_m1_str, m1_spawn, m1_goal,
                m2_lines, m2_spawn, m2_goal
            )
            if s and length > base_len:
                found.append((length, [('m1', x1, y1, c1, n1), ('m1', x2, y2, c2, n2)]))
                
        count += len(m1_candidates) - i - 1
        if count % 2000 == 0 or count == total_pairs:
            print(f"Progress Maze 1: {count}/{total_pairs} pairs checked...")

    print(f"Searching two-cell modifications for Maze 2 (candidates={len(m2_candidates)})...")
    
    # Try 1-cell changes in Maze 2
    for x1, y1 in m2_candidates:
        c1 = m2_lines[y1][x1]
        n1 = '#' if c1 == '.' else '.'
        
        test_m2 = [list(row) for row in m2_lines]
        test_m2[y1][x1] = n1
        test_m2_str = ["".join(row) for row in test_m2]
        
        s, length, path, states = solve_puzzle(
            m1_lines, m1_spawn, m1_goal,
            test_m2_str, m2_spawn, m2_goal
        )
        if s and length > base_len:
            found.append((length, [('m2', x1, y1, c1, n1)]))
            
    # Try 2-cell changes in Maze 2
    count = 0
    total_pairs = len(m2_candidates) * (len(m2_candidates) - 1) // 2
    for i in range(len(m2_candidates)):
        x1, y1 = m2_candidates[i]
        c1 = m2_lines[y1][x1]
        n1 = '#' if c1 == '.' else '.'
        
        for j in range(i + 1, len(m2_candidates)):
            x2, y2 = m2_candidates[j]
            c2 = m2_lines[y2][x2]
            n2 = '#' if c2 == '.' else '.'
            
            test_m2 = [list(row) for row in m2_lines]
            test_m2[y1][x1] = n1
            test_m2[y2][x2] = n2
            test_m2_str = ["".join(row) for row in test_m2]
            
            s, length, path, states = solve_puzzle(
                m1_lines, m1_spawn, m1_goal,
                test_m2_str, m2_spawn, m2_goal
            )
            if s and length > base_len:
                found.append((length, [('m2', x1, y1, c1, n1), ('m2', x2, y2, c2, n2)]))
                
        count += len(m2_candidates) - i - 1
        if count % 2000 == 0 or count == total_pairs:
            print(f"Progress Maze 2: {count}/{total_pairs} pairs checked...")
            
    # Sort and print top results
    found.sort(key=lambda x: x[0], reverse=True)
    print(f"\nTop 20 results:")
    for length, changes in found[:20]:
        change_desc = ", ".join([f"{ch[0]} ({ch[1]}, {ch[2]}): {ch[3]} -> {ch[4]}" for ch in changes])
        print(f"Length: {length} inputs | Changes: {change_desc}")

if __name__ == "__main__":
    main()
