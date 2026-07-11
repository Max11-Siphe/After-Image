#!/usr/bin/env python3
"""
AfterImage Solvability Validator
Validates all 4 maze pairs under the exact simultaneous-goal rules:
- Characters do NOT lock after reaching a goal
- Win condition: BOTH characters on their goals AT THE SAME TIME
- Character 2 moves in the OPPOSITE direction to Character 1
- A wall blocks only that character; the other may still move

Run from the after-image project root:
    python3 testing/validator.py
"""
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
    raw_lines = map_str.split('\n')
    lines = [l.strip() for l in raw_lines if l.strip()]

    if len(lines) != 14:
        errors.append(f"Row count is {len(lines)}, expected exactly 14")

    for i, line in enumerate(lines):
        if len(line) != 25:
            errors.append(f"Row {i} has length {len(line)}, expected exactly 25")

    s_count = 0
    g_count = 0
    spawn_pos = None
    goal_pos  = None
    unsupported = set()

    num_rows = len(lines)
    for y in range(num_rows):
        for x in range(len(lines[y])):
            ch = lines[y][x]
            if ch == 'S':
                s_count += 1
                spawn_pos = (x, y)
            elif ch == 'G':
                g_count += 1
                goal_pos = (x, y)
            elif ch not in ('#', '.'):
                unsupported.add((ch, x, y))

    if s_count != 1:
        errors.append(f"Contains {s_count} 'S' chars, expected 1")
    if g_count != 1:
        errors.append(f"Contains {g_count} 'G' chars, expected 1")

    # Boundary checks
    if len(lines) > 0 and len(lines[0]) == 25:
        for x in range(25):
            if lines[0][x] != '#':
                errors.append(f"Top boundary open at col {x}")
            if len(lines) == 14 and lines[13][x] != '#':
                errors.append(f"Bottom boundary open at col {x}")
    for y in range(len(lines)):
        if len(lines[y]) == 25:
            if lines[y][0] != '#':
                errors.append(f"Left boundary open at row {y}")
            if lines[y][24] != '#':
                errors.append(f"Right boundary open at row {y}")

    if spawn_pos and len(lines) == 14 and len(lines[spawn_pos[1]]) == 25:
        if lines[spawn_pos[1]][spawn_pos[0]] == '#':
            errors.append("Spawn 'S' is inside a wall")
    if goal_pos and len(lines) == 14 and len(lines[goal_pos[1]]) == 25:
        if lines[goal_pos[1]][goal_pos[0]] == '#':
            errors.append("Goal 'G' is inside a wall")

    if unsupported:
        errors.append(f"Unsupported chars: {sorted(list(unsupported))}")

    return lines, spawn_pos, goal_pos, errors


def _walkable(x, y, lines):
    if x < 0 or x >= 25 or y < 0 or y >= 14:
        return False
    return lines[y][x] != '#'


def solve_puzzle(maze1_lines, m1_spawn, m1_goal, maze2_lines, m2_spawn, m2_goal):
    """
    BFS over combined state (c1x, c1y, c2x, c2y).
    Characters do NOT lock after reaching their goal.
    Win = both characters simultaneously on their goals.
    Character 2 moves in the OPPOSITE direction to Character 1.
    """
    MOVES = [
        ('Up',    0, -1),
        ('Down',  0,  1),
        ('Left', -1,  0),
        ('Right', 1,  0),
    ]

    start = (m1_spawn[0], m1_spawn[1], m2_spawn[0], m2_spawn[1])
    goal  = (m1_goal[0],  m1_goal[1],  m2_goal[0],  m2_goal[1])

    if start == goal:
        return True, 0, [], 1

    queue   = deque([(start, [])])
    visited = {start}
    searched = 0

    while queue:
        state, path = queue.popleft()
        searched += 1
        c1x, c1y, c2x, c2y = state

        for name, dx, dy in MOVES:
            # C1 moves in direction
            n1x, n1y = c1x + dx, c1y + dy
            if not _walkable(n1x, n1y, maze1_lines):
                n1x, n1y = c1x, c1y

            # C2 moves in OPPOSITE direction
            n2x, n2y = c2x - dx, c2y - dy
            if not _walkable(n2x, n2y, maze2_lines):
                n2x, n2y = c2x, c2y

            nxt = (n1x, n1y, n2x, n2y)

            if nxt == goal:
                return True, len(path) + 1, path + [name], searched

            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [name]))

    return False, -1, [], searched


def calculate_metrics(maze1_lines, m1_spawn, maze2_lines, m2_spawn):
    MOVES = [(0,-1),(0,1),(-1,0),(1,0)]

    def junctions(lines):
        count = 0
        for y in range(1, 13):
            for x in range(1, 24):
                if lines[y][x] != '#':
                    n = sum(1 for dx,dy in MOVES if _walkable(x+dx, y+dy, lines))
                    if n >= 3:
                        count += 1
        return count

    start = (m1_spawn[0], m1_spawn[1], m2_spawn[0], m2_spawn[1])
    queue   = deque([start])
    visited = {start}
    while queue:
        c1x, c1y, c2x, c2y = queue.popleft()
        for dx, dy in MOVES:
            n1x, n1y = c1x+dx, c1y+dy
            if not _walkable(n1x, n1y, maze1_lines): n1x, n1y = c1x, c1y
            n2x, n2y = c2x-dx, c2y-dy
            if not _walkable(n2x, n2y, maze2_lines): n2x, n2y = c2x, c2y
            nxt = (n1x, n1y, n2x, n2y)
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)

    return len(visited), junctions(maze1_lines), junctions(maze2_lines)


def validate_pair(label, m1_path, m2_path):
    print(f"\n{'='*54}")
    print(f"  {label}")
    print(f"{'='*54}")

    m1_str, err1 = extract_map_string(m1_path)
    m2_str, err2 = extract_map_string(m2_path)
    if err1 or err2:
        if err1: print(f"  [ERROR] Maze 1: {err1}")
        if err2: print(f"  [ERROR] Maze 2: {err2}")
        return None

    m1_lines, m1_spawn, m1_goal, e1 = validate_map_layout(m1_str, os.path.basename(m1_path))
    m2_lines, m2_spawn, m2_goal, e2 = validate_map_layout(m2_str, os.path.basename(m2_path))

    if e1:
        print(f"  Maze 1 layout errors:")
        for e in e1: print(f"    - {e}")
    if e2:
        print(f"  Maze 2 layout errors:")
        for e in e2: print(f"    - {e}")
    if e1 or e2:
        print("  Skipping solvability check due to layout errors.")
        return {'label': label, 'valid': False, 'errors': e1+e2}

    print(f"  C1 spawn: {m1_spawn}  goal: {m1_goal}")
    print(f"  C2 spawn: {m2_spawn}  goal: {m2_goal}")

    solv, moves_count, path, searched = solve_puzzle(
        m1_lines, m1_spawn, m1_goal,
        m2_lines, m2_spawn, m2_goal
    )

    result = {
        'label': label, 'valid': True, 'solvable': solv,
        'm1_spawn': m1_spawn, 'm1_goal': m1_goal,
        'm2_spawn': m2_spawn, 'm2_goal': m2_goal,
        'moves_count': moves_count, 'path': path, 'searched': searched
    }

    if solv:
        reachable, m1j, m2j = calculate_metrics(m1_lines, m1_spawn, m2_lines, m2_spawn)
        dc = sum(1 for i in range(1, len(path)) if path[i] != path[i-1])

        # Asymmetric move count
        asym = 0
        c1x, c1y = m1_spawn; c2x, c2y = m2_spawn
        mv = {'Up':(0,-1),'Down':(0,1),'Left':(-1,0),'Right':(1,0)}
        for mn in path:
            dx, dy = mv[mn]
            n1x,n1y = c1x+dx,c1y+dy
            w1 = _walkable(n1x,n1y,m1_lines)
            n2x,n2y = c2x-dx,c2y-dy
            w2 = _walkable(n2x,n2y,m2_lines)
            if not w1 or not w2: asym += 1
            if w1: c1x,c1y=n1x,n1y
            if w2: c2x,c2y=n2x,n2y

        print(f"  Solvable:         YES")
        print(f"  Shortest path:    {moves_count} inputs")
        print(f"  States searched:  {searched}")
        print(f"  Reachable states: {reachable}")
        print(f"  Junctions M1/M2:  {m1j} / {m2j}")
        print(f"  Direction changes:{dc}")
        print(f"  Asymmetric moves: {asym}")
        print(f"  Solution:         {' -> '.join(path)}")
        result.update({'reachable': reachable, 'm1j': m1j, 'm2j': m2j, 'dc': dc, 'asym': asym})
    else:
        print(f"  Solvable:         NO")
        print(f"  States searched:  {searched}")

    return result


def run_all():
    levels_dir = "levels"
    pairs = [
        ("Level 0 — Tutorial",
         os.path.join(levels_dir, "tutorial_maze_1.tscn"),
         os.path.join(levels_dir, "tutorial_maze_2.tscn")),
        ("Level 1 — Dungeon",
         os.path.join(levels_dir, "maze_1_dungeon.tscn"),
         os.path.join(levels_dir, "maze_2_dungeon.tscn")),
        ("Level 2 — City",
         os.path.join(levels_dir, "maze_1_city.tscn"),
         os.path.join(levels_dir, "maze_2_city.tscn")),
        ("Level 3 — Cloud",
         os.path.join(levels_dir, "maze_1_cloud.tscn"),
         os.path.join(levels_dir, "maze_2_cloud.tscn")),
    ]

    results = []
    for label, m1, m2 in pairs:
        r = validate_pair(label, m1, m2)
        if r:
            results.append(r)

    # Write report
    report_path = os.path.join("testing", "validation_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("AFTERIMAGE SOLVABILITY VALIDATION REPORT\n")
        f.write("Rule: Win = both characters on goals SIMULTANEOUSLY (no locking)\n")
        f.write("="*60 + "\n\n")
        for r in results:
            f.write(f"Pair: {r['label']}\n")
            if not r['valid']:
                f.write("  Status: INVALID MAP DATA\n")
                for e in r['errors']:
                    f.write(f"    - {e}\n")
            else:
                if r['solvable']:
                    f.write(f"  Solvable:         YES\n")
                    f.write(f"  C1 spawn: {r['m1_spawn']}  goal: {r['m1_goal']}\n")
                    f.write(f"  C2 spawn: {r['m2_spawn']}  goal: {r['m2_goal']}\n")
                    f.write(f"  Shortest path:    {r['moves_count']} inputs\n")
                    f.write(f"  States searched:  {r['searched']}\n")
                    f.write(f"  Reachable states: {r.get('reachable','?')}\n")
                    f.write(f"  Junctions M1/M2:  {r.get('m1j','?')} / {r.get('m2j','?')}\n")
                    f.write(f"  Direction changes:{r.get('dc','?')}\n")
                    f.write(f"  Asymmetric moves: {r.get('asym','?')}\n")
                    f.write(f"  Solution path: {' -> '.join(r['path'])}\n")
                else:
                    f.write(f"  Solvable: NO\n")
                    f.write(f"  States searched: {r['searched']}\n")
            f.write("\n" + "-"*60 + "\n\n")

    print(f"\nReport saved → {report_path}")

    # Summary table
    print("\n" + "="*54)
    print("SUMMARY")
    print("="*54)
    print(f"{'Level':<25} {'Inputs':>7} {'States':>8} {'Junc':>6} {'DC':>4} {'Asym':>5}")
    print("-"*54)
    for r in results:
        if r.get('solvable'):
            junc = f"{r.get('m1j','?')}/{r.get('m2j','?')}"
            print(f"{r['label']:<25} {r['moves_count']:>7} {r.get('reachable',0):>8} {junc:>6} {r.get('dc',0):>4} {r.get('asym',0):>5}")
        else:
            print(f"{r['label']:<25} {'UNSOLVABLE':>7}")


if __name__ == "__main__":
    run_all()
