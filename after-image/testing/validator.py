#!/usr/bin/env python3
import os
import sys
from collections import deque

def extract_map_string(file_path):
    if not os.path.exists(file_path):
        return None, f"File does not exist: {file_path}"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        start_marker = 'map_string = "'
        start_idx = content.find(start_marker)
        if start_idx == -1:
            return None, f"Could not find 'map_string = \"' in {file_path}"
        start_idx += len(start_marker)
        end_idx = content.find('"', start_idx)
        if end_idx == -1:
            return None, f"Could not find closing quote for map_string in {file_path}"
        return content[start_idx:end_idx], None
    except Exception as e:
        return None, f"Error reading {file_path}: {e}"

def validate_map_layout(map_str, file_name):
    errors = []
    # Split into lines and clean
    raw_lines = map_str.split('\n')
    lines = []
    for line in raw_lines:
        cleaned = line.strip()
        if cleaned:
            lines.append(cleaned)
            
    # Check row count
    if len(lines) != 14:
        errors.append(f"Row count is {len(lines)}, expected exactly 14")
        
    # Check column count
    for i, line in enumerate(lines):
        if len(line) != 25:
            errors.append(f"Row {i} has length {len(line)}, expected exactly 25")
            
    # Check character validation
    s_count = 0
    g_count = 0
    spawn_pos = None
    goal_pos = None
    unsupported_chars = set()
    
    # We will only proceed with coordinates check if lines sizes are valid
    num_rows = len(lines)
    for y in range(num_rows):
        row_len = len(lines[y])
        for x in range(row_len):
            char = lines[y][x]
            if char == 'S':
                s_count += 1
                spawn_pos = (x, y)
            elif char == 'G':
                g_count += 1
                goal_pos = (x, y)
            elif char not in ('#', '.'):
                unsupported_chars.add((char, x, y))
                
    if s_count != 1:
        errors.append(f"Contains {s_count} 'S' characters, expected exactly 1")
    if g_count != 1:
        errors.append(f"Contains {g_count} 'G' characters, expected exactly 1")
        
    # Check outer boundaries
    # Top and bottom rows must be all '#'
    if len(lines) > 0 and len(lines[0]) == 25:
        for x in range(25):
            if lines[0][x] != '#':
                errors.append(f"Top boundary open at col {x}: {lines[0][x]}")
            if len(lines) == 14 and lines[13][x] != '#':
                errors.append(f"Bottom boundary open at col {x}: {lines[13][x]}")
    # First and last columns must be '#'
    for y in range(len(lines)):
        if len(lines[y]) == 25:
            if lines[y][0] != '#':
                errors.append(f"Left boundary open at row {y}: {lines[y][0]}")
            if lines[y][24] != '#':
                errors.append(f"Right boundary open at row {y}: {lines[y][24]}")
                
    # Check spawn & goal in walls
    if spawn_pos and len(lines) == 14 and len(lines[spawn_pos[1]]) == 25:
        if lines[spawn_pos[1]][spawn_pos[0]] == '#':
            errors.append(f"Spawn 'S' is inside a wall (#)")
    if goal_pos and len(lines) == 14 and len(lines[goal_pos[1]]) == 25:
        if lines[goal_pos[1]][goal_pos[0]] == '#':
            errors.append(f"Goal 'G' is inside a wall (#)")
            
    if unsupported_chars:
        errors.append(f"Unsupported characters found: {sorted(list(unsupported_chars))}")
        
    return lines, spawn_pos, goal_pos, errors

def solve_puzzle(maze1_lines, m1_spawn, m1_goal, maze2_lines, m2_spawn, m2_goal):
    # Directions
    # Up: (0, -1), Down: (0, 1), Left: (-1, 0), Right: (1, 0)
    # Character 2 moves in negated direction
    moves = {
        'Up': (0, -1),
        'Down': (0, 1),
        'Left': (-1, 0),
        'Right': (1, 0)
    }
    
    def is_walkable(x, y, lines):
        if x < 0 or x >= 25 or y < 0 or y >= 14:
            return False
        # Treat anything other than '#' as walkable
        return lines[y][x] != '#'
        
    start_state = (m1_spawn[0], m1_spawn[1], m2_spawn[0], m2_spawn[1])
    goal_state = (m1_goal[0], m1_goal[1], m2_goal[0], m2_goal[1])
    
    if start_state == goal_state:
        return True, 0, [], 1
        
    queue = deque([(start_state, [])])
    visited = {start_state}
    states_searched = 0
    
    while queue:
        state, path = queue.popleft()
        states_searched += 1
        
        c1x, c1y, c2x, c2y = state
        
        for move_name, (dx, dy) in moves.items():
            # Character 1 moves in dx, dy
            n1x, n1y = c1x + dx, c1y + dy
            if not is_walkable(n1x, n1y, maze1_lines):
                n1x, n1y = c1x, c1y
                
            # Character 2 moves in -dx, -dy
            n2x, n2y = c2x - dx, c2y - dy
            if not is_walkable(n2x, n2y, maze2_lines):
                n2x, n2y = c2x, c2y
                
            next_state = (n1x, n1y, n2x, n2y)
            
            if next_state == goal_state:
                return True, len(path) + 1, path + [move_name], states_searched
                
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [move_name]))
                
    return False, -1, [], states_searched

def calculate_metrics(maze1_lines, m1_spawn, maze2_lines, m2_spawn):
    # Let's count reachable states and some metrics
    moves = {
        'Up': (0, -1),
        'Down': (0, 1),
        'Left': (-1, 0),
        'Right': (1, 0)
    }
    def is_walkable(x, y, lines):
        if x < 0 or x >= 25 or y < 0 or y >= 14:
            return False
        return lines[y][x] != '#'
        
    start_state = (m1_spawn[0], m1_spawn[1], m2_spawn[0], m2_spawn[1])
    queue = deque([start_state])
    visited = {start_state}
    
    # We will also count junctions for maze 1 and maze 2
    def count_junctions(lines):
        junctions = 0
        for y in range(1, 13):
            for x in range(1, 24):
                if lines[y][x] != '#':
                    # count walkable neighbors
                    walkable_neighbors = 0
                    for dx, dy in moves.values():
                        if is_walkable(x + dx, y + dy, lines):
                            walkable_neighbors += 1
                    if walkable_neighbors >= 3:
                        junctions += 1
        return junctions

    m1_junctions = count_junctions(maze1_lines)
    m2_junctions = count_junctions(maze2_lines)
    
    while queue:
        state = queue.popleft()
        c1x, c1y, c2x, c2y = state
        for dx, dy in moves.values():
            n1x, n1y = c1x + dx, c1y + dy
            if not is_walkable(n1x, n1y, maze1_lines):
                n1x, n1y = c1x, c1y
            n2x, n2y = c2x - dx, c2y - dy
            if not is_walkable(n2x, n2y, maze2_lines):
                n2x, n2y = c2x, c2y
            next_state = (n1x, n1y, n2x, n2y)
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
                
    return len(visited), m1_junctions, m2_junctions

def validate_pair(name, m1_path, m2_path):
    print(f"==================================================")
    print(f"Validating Pair: {name}")
    print(f"==================================================")
    
    m1_str, err1 = extract_map_string(m1_path)
    m2_str, err2 = extract_map_string(m2_path)
    
    if err1 or err2:
        if err1: print(f"Error reading Maze 1: {err1}")
        if err2: print(f"Error reading Maze 2: {err2}")
        return None
        
    m1_lines, m1_spawn, m1_goal, errors1 = validate_map_layout(m1_str, os.path.basename(m1_path))
    m2_lines, m2_spawn, m2_goal, errors2 = validate_map_layout(m2_str, os.path.basename(m2_path))
    
    if errors1:
        print(f"Malformed data in Maze 1 ({os.path.basename(m1_path)}):")
        for err in errors1:
            print(f"  - {err}")
    if errors2:
        print(f"Malformed data in Maze 2 ({os.path.basename(m2_path)}):")
        for err in errors2:
            print(f"  - {err}")
            
    if errors1 or errors2:
        print("Validation errors exist. Skipping solvability analysis.")
        return {
            'name': name,
            'valid': False,
            'errors': errors1 + errors2
        }
        
    print(f"Maze 1 Spawn: {m1_spawn}, Goal: {m1_goal}")
    print(f"Maze 2 Spawn: {m2_spawn}, Goal: {m2_goal}")
    
    solv, moves_count, path, states = solve_puzzle(
        m1_lines, m1_spawn, m1_goal,
        m2_lines, m2_spawn, m2_goal
    )
    
    if solv:
        reachable_states, m1_junc, m2_junc = calculate_metrics(m1_lines, m1_spawn, m2_lines, m2_spawn)
        # Count direction changes
        dir_changes = 0
        for i in range(1, len(path)):
            if path[i] != path[i-1]:
                dir_changes += 1
        # Count asymmetric movements (where one character is blocked)
        asymmetric_moves = 0
        c1x, c1y, c2x, c2y = m1_spawn[0], m1_spawn[1], m2_spawn[0], m2_spawn[1]
        move_vecs = {'Up': (0, -1), 'Down': (0, 1), 'Left': (-1, 0), 'Right': (1, 0)}
        for move_name in path:
            dx, dy = move_vecs[move_name]
            # check if blocked
            n1x, n1y = c1x + dx, c1y + dy
            w1 = m1_lines[n1y][n1x] != '#' if (0<=n1x<25 and 0<=n1y<14) else False
            
            n2x, n2y = c2x - dx, c2y - dy
            w2 = maze2_lines = m2_lines[n2y][n2x] != '#' if (0<=n2x<25 and 0<=n2y<14) else False
            
            if not w1 or not w2:
                asymmetric_moves += 1
                
            if w1: c1x, c1y = n1x, n1y
            if w2: c2x, c2y = n2x, n2y

        print(f"Solvable: YES")
        print(f"Shortest Solution Length: {moves_count} inputs")
        print(f"Reachable Combined States: {reachable_states}")
        print(f"Junctions: Maze 1: {m1_junc}, Maze 2: {m2_junc}")
        print(f"Direction changes in shortest path: {dir_changes}")
        print(f"Asymmetric moves in shortest path: {asymmetric_moves}")
        print(f"States searched: {states}")
        print(f"Solution: {' -> '.join(path)}")
        return {
            'name': name,
            'valid': True,
            'solvable': True,
            'moves_count': moves_count,
            'path': path,
            'states_searched': states,
            'reachable_states': reachable_states,
            'm1_spawn': m1_spawn,
            'm1_goal': m1_goal,
            'm2_spawn': m2_spawn,
            'm2_goal': m2_goal,
            'm1_junc': m1_junc,
            'm2_junc': m2_junc,
            'dir_changes': dir_changes,
            'asymmetric_moves': asymmetric_moves
        }
    else:
        print(f"Solvable: NO")
        print(f"States searched: {states}")
        return {
            'name': name,
            'valid': True,
            'solvable': False,
            'states_searched': states,
            'm1_spawn': m1_spawn,
            'm1_goal': m1_goal,
            'm2_spawn': m2_spawn,
            'm2_goal': m2_goal
        }

def run_all_validations():
    levels_dir = "levels"
    pairs = [
        ("Tutorial (Level 1)", os.path.join(levels_dir, "tutorial_maze_1.tscn"), os.path.join(levels_dir, "tutorial_maze_2.tscn")),
        ("City Pair", os.path.join(levels_dir, "maze_1_city.tscn"), os.path.join(levels_dir, "maze_2_city.tscn")),
        ("Cloud Pair", os.path.join(levels_dir, "maze_1_cloud.tscn"), os.path.join(levels_dir, "maze_2_cloud.tscn")),
        ("Dungeon Pair", os.path.join(levels_dir, "maze_1_dungeon.tscn"), os.path.join(levels_dir, "maze_2_dungeon.tscn"))
    ]
    
    results = []
    for name, m1, m2 in pairs:
        res = validate_pair(name, m1, m2)
        if res:
            results.append(res)
            
    # Write report
    report_path = os.path.join("testing", "validation_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("AFTERIMAGE SOLVABILITY VALIDATOR REPORT\n")
        f.write("======================================\n\n")
        for r in results:
            f.write(f"Pair: {r['name']}\n")
            if not r['valid']:
                f.write("  Status: INVALID MAP DATA\n")
                for err in r['errors']:
                    f.write(f"    - {err}\n")
            else:
                f.write(f"  Status: VALID MAPS\n")
                f.write(f"  Maze 1 Spawn: {r['m1_spawn']}, Goal: {r['m1_goal']}\n")
                f.write(f"  Maze 2 Spawn: {r['m2_spawn']}, Goal: {r['m2_goal']}\n")
                if r['solvable']:
                    f.write(f"  Solvable: YES\n")
                    f.write(f"  Shortest Solution Length: {r['moves_count']} inputs\n")
                    f.write(f"  Reachable Combined States: {r['reachable_states']}\n")
                    f.write(f"  Junctions: Maze 1: {r['m1_junc']}, Maze 2: {r['m2_junc']}\n")
                    f.write(f"  Direction changes in shortest path: {r['dir_changes']}\n")
                    f.write(f"  Asymmetric moves in shortest path: {r['asymmetric_moves']}\n")
                    f.write(f"  States searched: {r['states_searched']}\n")
                    f.write(f"  Solution path: {' -> '.join(r['path'])}\n")
                else:
                    f.write(f"  Solvable: NO\n")
                    f.write(f"  States searched: {r['states_searched']}\n")
            f.write("\n--------------------------------------\n\n")
            
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    run_all_validations()
