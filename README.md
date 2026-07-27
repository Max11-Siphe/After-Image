# After-Image
Itch.io Game Submission for Game Jam Hosted by BBD

*echoes never walk alone*

A 2D maze game built for a 24-hour game jam under the theme **"Echoes and Reflections."**

## Concept
Two mazes sit side by side, each completely different in layout. A character stands in each maze, but both are controlled by the same input — when Character 1 moves left, Character 2 moves right, like a reflection. The player can only see one maze at a time.

Between the two mazes lies a **swap zone**. Navigate it correctly, and control swaps to the other character — now inverted, now in unfamiliar territory, continuing to solve a maze you were previously only steering blind. Leaving a maze triggers an **echo trail**, a fading visual trace of the path just walked, tying the game mechanically and visually back to the theme.

## How to Play

- Move your character through the maze using the arrow keys / WASD (confirm control scheme with your build).
- Reach the swap zone to transfer control to your mirrored character in the other maze.
- Solve both mazes to win. Getting stuck or trapped ends the run.

## Levels

1. **Dungeon** — mossy stone, torchlit corridors, labyrinth atmosphere
2. **City** — a change of setting and mood from the dungeon opener
3. **Clouds** — an ethereal, airy final theme

## Team & Roles

| Role | Responsibility |
|---|---|
| Person A | Core systems — character controller, mirrored input logic, swap-zone mechanic, win/lose logic |
| Person B | Maze/level building — TileMap layout, wall collision, tileset configuration, camera/view switching |
| Person C | Art & polish — character sprites, tilesets, backgrounds, UI/HUD, title & end screens, echo/trail visual design |

## Built With

- **Godot Engine** (GDScript)
- **Piskel** — pixel art and sprite creation

## Assets & Credits

- All character, tile, and UI art created or modified in-house for this jam.

## Theme Interpretation

- **Reflections** — mirrored character movement across two independent mazes.
- **Echoes** — the swap-triggered trail effect renders the literal path just taken, visualized as a fading echo left behind.

## Status

Built in 24 hours. Known limitations and stretch goals not completed in time are noted here for future iteration:
- *(list anything left unfinished — e.g. second maze theme, animated wind/dust effects, sound implementation, etc.)*

## Credits

Made by Paris Amorita Nyoni,Siphe Makitshi and Nothando Ndlovu.