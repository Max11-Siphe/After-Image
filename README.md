#AfterImage

echoes never walk alone

A 2D maze game built in a 24-hour game jam under the theme "Echoes and Reflections."

#Concept

Two mazes sit side by side, each completely different in layout. A character stands in each maze, but both are controlled by the same input — when Character 1 moves left, Character 2 moves right, like a reflection. The player can only see one maze at a time.

Between the two mazes lies a swap zone. Navigate it correctly, and control swaps to the other character — now inverted, now in unfamiliar territory, continuing to solve a maze you were previously only steering blind. Leaving a maze triggers an echo trail, a fading visual trace of the path just walked, tying the game mechanically and visually back to the theme.

#How to Play
Move your character through the maze (arrow keys / WASD — confirm against final build).
Reach the swap zone to transfer control to your mirrored character in the other maze.
Solve both mazes to win. Getting trapped or failing ends the run, with the option to try again.

#Levels
Dungeon — mossy stone, torchlit corridors, labyrinth atmosphere
City — a shift in setting and mood from the dungeon opener
Clouds — an ethereal, airy final theme
Theme Interpretation
Reflections — mirrored character movement across two independently-designed mazes, forcing the player to hold two mental models of control at once.
Echoes — the swap-triggered trail effect renders the literal path just taken, visualized as a fading echo left behind rather than constant ambient decoration.

#Team & Roles
Role	Responsibility
Person A	Core systems — character controller, mirrored input logic, swap-zone mechanic, win/lose logic
Person B	Maze/level building — TileMap layout, wall collision, tileset configuration, camera/view switching
Person C (Paris)	Art & polish — character sprites, tilesets, backgrounds, UI/HUD, title & end screens, echo/trail visual design

#Built With
Godot Engine (GDScript)
Piskel — pixel art and sprite/animation creation
Lospec — color palette reference
Status & Known Limitations

