extends Node2D

# Level data: display_num, display_name, maze1_scene, maze2_scene
const LEVEL_DATA = [
	{
		"display_num": 0,
		"name": "Tutorial",
		"difficulty": "Intro",
		"maze1_scene": "res://levels/tutorial_maze_1.tscn",
		"maze2_scene": "res://levels/tutorial_maze_2.tscn"
	},
	{
		"display_num": 1,
		"name": "Dungeon",
		"difficulty": "Easy",
		"maze1_scene": "res://levels/maze_1_dungeon.tscn",
		"maze2_scene": "res://levels/maze_2_dungeon.tscn"
	},
	{
		"display_num": 2,
		"name": "City",
		"difficulty": "Medium",
		"maze1_scene": "res://levels/maze_1_city.tscn",
		"maze2_scene": "res://levels/maze_2_city.tscn"
	},
	{
		"display_num": 3,
		"name": "Cloud",
		"difficulty": "Hard",
		"maze1_scene": "res://levels/maze_1_cloud.tscn",
		"maze2_scene": "res://levels/maze_2_cloud.tscn"
	},
	{
		"display_num": 4,
		"name": "Dream Core",
		"difficulty": "Finale",
		"maze1_scene": "res://levels/dream_core_room.tscn",
		"maze2_scene": "res://levels/dream_core_room.tscn"
	}
]

@onready var hud: CanvasLayer = $HUD
@onready var win_screen: CanvasLayer = $WinScreen

var maze1: Node2D
var maze2: Node2D
var character1: CharacterBody2D
var character2: CharacterBody2D

var current_level_index: int = 0
var current_view: int = 1
var is_game_won: bool = false

# Echo Footprints State
const FootprintClass = preload("res://scripts/footprint.gd")
var footprint_reveal_triggered: bool = false
var footprint_reveal_used: bool = false
var footprint_fade_active: bool = false
var footprint_fade_tween: Tween = null
var footprints_p1: Array[Node2D] = []
var footprints_p2: Array[Node2D] = []

# Intro and UI Overlays
var intro_scene: CanvasLayer = null
var tutorial_instructions: CanvasLayer = null
var dream_core_intro: CanvasLayer = null
var endings_screen: CanvasLayer = null

func _ready() -> void:
	setup_input_actions()
	win_screen.primary_pressed.connect(_on_win_screen_primary)
	win_screen.retry_pressed.connect(_on_win_screen_retry)
	win_screen.quit_pressed.connect(_on_win_screen_quit)
	
	# Start by displaying story intro title screen
	show_story_introduction()

func setup_input_actions() -> void:
	var actions = {
		"move_left":  [KEY_LEFT, KEY_A],
		"move_right": [KEY_RIGHT, KEY_D],
		"move_up":    [KEY_UP, KEY_W],
		"move_down":  [KEY_DOWN, KEY_S],
		"switch_view":[KEY_TAB]
	}
	for action in actions:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
			for key in actions[action]:
				var event = InputEventKey.new()
				event.physical_keycode = key
				InputMap.action_add_event(action, event)

func show_story_introduction() -> void:
	# Clean up any existing instances
	if is_instance_valid(intro_scene):
		intro_scene.queue_free()
	
	# Hide gameplay HUD & characters during story
	hud.visible = false
	win_screen.visible = false
	is_game_won = true # block input
	
	var intro_scene_res = load("res://UI/intro_cutscene.tscn")
	intro_scene = intro_scene_res.instantiate()
	add_child(intro_scene)
	intro_scene.intro_finished.connect(_on_intro_finished)

func _on_intro_finished(success: bool) -> void:
	if success:
		# Show tutorial screen
		intro_scene.queue_free()
		show_tutorial_instructions()
	else:
		# Should not reach here because 'No' triggers GameOver which has its own buttons handled in the scene
		pass

func show_tutorial_instructions() -> void:
	if is_instance_valid(tutorial_instructions):
		tutorial_instructions.queue_free()
		
	var tut_res = load("res://UI/tutorial_instructions.tscn")
	tutorial_instructions = tut_res.instantiate()
	add_child(tutorial_instructions)
	tutorial_instructions.tutorial_started.connect(_on_tutorial_started)

func _on_tutorial_started() -> void:
	tutorial_instructions.queue_free()
	hud.visible = true
	load_level(0)

func _unhandled_input(event: InputEvent) -> void:
	# If any story or intro overlay is open, block all movement and tab
	if is_instance_valid(intro_scene) or is_instance_valid(tutorial_instructions) or is_instance_valid(dream_core_intro) or is_instance_valid(endings_screen):
		return
		
	if is_game_won:
		return
	if not is_instance_valid(character1) or not is_instance_valid(character2):
		return
	if character1.is_moving or character2.is_moving:
		return

	if event.is_action_pressed("switch_view"):
		toggle_view()
		if not footprint_reveal_used:
			show_echo_trails()
		get_viewport().set_input_as_handled()
		return

	var dir = Vector2i.ZERO
	if   event.is_action_pressed("move_left"):  dir = Vector2i.LEFT
	elif event.is_action_pressed("move_right"): dir = Vector2i.RIGHT
	elif event.is_action_pressed("move_up"):    dir = Vector2i.UP
	elif event.is_action_pressed("move_down"):  dir = Vector2i.DOWN

	if dir != Vector2i.ZERO:
		character1.try_move(dir)
		character2.try_move(dir)   # Character 2 inverts internally
		get_viewport().set_input_as_handled()

func load_level(index: int) -> void:
	# Freeze input during load
	is_game_won = true

	# Clean up previous level nodes
	if is_instance_valid(maze1):
		remove_child(maze1)
		maze1.queue_free()
	if is_instance_valid(maze2):
		remove_child(maze2)
		maze2.queue_free()
	maze1 = null
	maze2 = null
	character1 = null
	character2 = null
	
	clear_trails()

	current_level_index = index
	var data = LEVEL_DATA[index]

	# Instantiate new mazes
	var m1_res = load(data.maze1_scene)
	maze1 = m1_res.instantiate()
	maze1.position = Vector2(80, 46)
	add_child(maze1)

	var m2_res = load(data.maze2_scene)
	maze2 = m2_res.instantiate()
	maze2.position = Vector2(80, 46)
	add_child(maze2)

	# Instantiate characters
	var player_scene = load("res://players/player.tscn")

	character1 = player_scene.instantiate()
	character1.name = "Character1"
	character1.is_inverted = false
	character1.maze_layer = maze1.tilemap_layer
	character1.spawn_grid_pos = maze1.spawn_grid_pos

	character1.goal_grid_pos = maze1.goal_grid_pos
	character1.swap_grid_pos = maze1.swap_grid_pos

	character1.goal_reached.connect(_on_character_goal_reached)
	character1.swap_zone_entered.connect(_on_swap_zone_entered)
	maze1.add_child(character1)

	character2 = player_scene.instantiate()
	character2.name = "Character2"
	character2.is_inverted = true
	character2.maze_layer = maze2.tilemap_layer
	character2.spawn_grid_pos = maze2.spawn_grid_pos

	character2.goal_grid_pos = maze2.goal_grid_pos
	character2.swap_grid_pos = maze2.swap_grid_pos

	character2.goal_reached.connect(_on_character_goal_reached)
	character2.swap_zone_entered.connect(_on_swap_zone_entered)
	maze2.add_child(character2)

	# Custom visual representation for the Dream Core Finale
	if current_level_index == 4:
		customize_dream_core_goals()

	restart_game()

	# If this is the Dream Core room, show the Dream Core Finale introductory screen before gameplay
	if current_level_index == 4:
		show_dream_core_intro()

func show_dream_core_intro() -> void:
	if is_instance_valid(dream_core_intro):
		dream_core_intro.queue_free()
		
	var dc_res = load("res://UI/dream_core_intro.tscn")
	dream_core_intro = dc_res.instantiate()
	add_child(dream_core_intro)
	is_game_won = true # Keep input blocked
	dream_core_intro.continue_pressed.connect(_on_dream_core_intro_continued)

func _on_dream_core_intro_continued() -> void:
	dream_core_intro.queue_free()
	is_game_won = false # Allow gameplay starting

func customize_dream_core_goals() -> void:
	# Modify goals visual representation to look like a glowing Dream Core target
	if is_instance_valid(maze1) and is_instance_valid(maze1.goal_sprite):
		maze1.goal_sprite.modulate = Color(0.9, 0.4, 0.9, 1.0)
		maze1.goal_sprite.scale = Vector2(1.3, 1.3)
	if is_instance_valid(maze2) and is_instance_valid(maze2.goal_sprite):
		maze2.goal_sprite.modulate = Color(0.9, 0.4, 0.9, 1.0)
		maze2.goal_sprite.scale = Vector2(1.3, 1.3)

func _on_swap_zone_entered() -> void:
	if is_game_won:
		return
	print("SWAP — char1: ", character1.grid_pos, "  char2: ", character2.grid_pos)
	
	character1.is_inverted = !character1.is_inverted
	character2.is_inverted = !character2.is_inverted
	character1.update_sprite()
	character2.update_sprite()
	character1.teleport_to_swap()
	character2.teleport_to_swap()
	toggle_view()

func show_echo_trails() -> void:
	footprint_reveal_triggered = true
	footprint_reveal_used = true
	footprint_fade_active = true
	
	# Instantiate footprints for P1 on Maze 1
	for pt in character1.path_history:
		var fp = FootprintClass.new()
		fp.position = Vector2(pt.x * 32 + 16, pt.y * 32 + 16)
		fp.color = Color(0.2, 0.7, 1.0, 0.8) # Blue/Cyan
		maze1.add_child(fp)
		footprints_p1.append(fp)
		
	# Instantiate footprints for P2 on Maze 2
	for pt in character2.path_history:
		var fp = FootprintClass.new()
		fp.position = Vector2(pt.x * 32 + 16, pt.y * 32 + 16)
		fp.color = Color(1.0, 0.5, 0.2, 0.8) # Orange/Red
		maze2.add_child(fp)
		footprints_p2.append(fp)
		
	# Set up the 5-second fade-out Tween
	footprint_fade_tween = create_tween()
	footprint_fade_tween.set_parallel(true)
	
	for fp in footprints_p1:
		footprint_fade_tween.tween_property(fp, "modulate:a", 0.0, 5.0)
	for fp in footprints_p2:
		footprint_fade_tween.tween_property(fp, "modulate:a", 0.0, 5.0)
		
	footprint_fade_tween.set_parallel(false)
	footprint_fade_tween.tween_callback(func():
		clear_trails()
	)

func clear_trails() -> void:
	if footprint_fade_tween:
		footprint_fade_tween.kill()
		footprint_fade_tween = null
		
	for fp in footprints_p1:
		if is_instance_valid(fp):
			fp.queue_free()
	footprints_p1.clear()
	
	for fp in footprints_p2:
		if is_instance_valid(fp):
			fp.queue_free()
	footprints_p2.clear()
	
	footprint_fade_active = false

func toggle_view() -> void:
	current_view = 2 if current_view == 1 else 1
	update_view_visibility()

func update_view_visibility() -> void:
	if is_instance_valid(maze1):
		maze1.visible = (current_view == 1)
	if is_instance_valid(maze2):
		maze2.visible = (current_view == 2)
	hud.set_viewing_maze(current_view)

func _on_character_goal_reached() -> void:
	if not is_instance_valid(character1) or not is_instance_valid(character2):
		return

	# Update goal glow
	if is_instance_valid(maze1):
		maze1.set_occupied(character1.has_reached_goal)
	if is_instance_valid(maze2):
		maze2.set_occupied(character2.has_reached_goal)

	hud.set_completion_status(character1.has_reached_goal, character2.has_reached_goal)
	
	if current_level_index == 4:
		# Let the movement finish completely before ending checks
		await get_tree().process_frame
		check_dream_core_endings()
	else:
		check_win_condition()

func check_dream_core_endings() -> void:
	if is_game_won:
		return
	
	# Evaluate goals reached after movements are finalized
	var p1_reached = (character1.grid_pos == character1.goal_grid_pos)
	var p2_reached = (character2.grid_pos == character2.goal_grid_pos)
	
	if p1_reached or p2_reached:
		is_game_won = true # Stop player movement/further actions
		
		# Short delay so the step to the core is visible
		await get_tree().create_timer(0.4).timeout
		
		if p1_reached and p2_reached:
			show_ending_screen("shared")
		elif p1_reached:
			show_ending_screen("p1_solo")
		elif p2_reached:
			show_ending_screen("p2_solo")

func show_ending_screen(type: String) -> void:
	if is_instance_valid(endings_screen):
		endings_screen.queue_free()
		
	var endings_res = load("res://UI/endings_screen.tscn")
	endings_screen = endings_res.instantiate()
	add_child(endings_screen)
	endings_screen.setup_ending(type)
	endings_screen.restart_game_pressed.connect(_on_ending_restart)
	endings_screen.return_to_title_pressed.connect(_on_ending_return_to_title)
	endings_screen.quit_pressed.connect(_on_win_screen_quit)

func _on_ending_restart() -> void:
	endings_screen.queue_free()
	# Restart Game must begin again from Level 0 (Tutorial) directly, skipping intro
	hud.visible = true
	load_level(0)

func _on_ending_return_to_title() -> void:
	endings_screen.queue_free()
	show_story_introduction()

func check_win_condition() -> void:
	if is_game_won:
		return
	if character1.has_reached_goal and character2.has_reached_goal:
		is_game_won = true

		# Play win flash on both goals
		if is_instance_valid(maze1):
			maze1.play_win_flash()
		if is_instance_valid(maze2):
			maze2.play_win_flash()

		# Short delay so flash is visible
		await get_tree().create_timer(0.8).timeout

		if not is_game_won:
			return   # Was cancelled by retry/load during wait

		# Level 3 (Cloud) completion offers entry into the Dream Core
		var is_last = (current_level_index == LEVEL_DATA.size() - 1)
		win_screen.setup_screen(is_last)
		
		# If level is Cloud (index 3), change primary button text to "Enter the Dream Core"
		if current_level_index == 3:
			win_screen.primary_button.text = "Enter the Dream Core"
			
		win_screen.visible = true

func restart_game() -> void:
	is_game_won = false
	win_screen.visible = false
	current_view = 1

	footprint_reveal_triggered = false
	footprint_reveal_used = false
	footprint_fade_active = false
	clear_trails()

	if is_instance_valid(character1):
		character1.reset_to_start()
	if is_instance_valid(character2):
		character2.reset_to_start()

	update_view_visibility()

	if is_instance_valid(maze1):
		maze1.set_occupied(false)
	if is_instance_valid(maze2):
		maze2.set_occupied(false)

	var data = LEVEL_DATA[current_level_index]
	hud.set_level_info(
		data.display_num,
		LEVEL_DATA.size(),
		data.name,
		data.difficulty
	)
	hud.set_completion_status(false, false)

func _on_win_screen_primary() -> void:
	if current_level_index == LEVEL_DATA.size() - 1:
		load_level(0)           # Restart Game → Tutorial
	else:
		load_level(current_level_index + 1)   # Next Level

func _on_win_screen_retry() -> void:
	restart_game()

func _on_win_screen_quit() -> void:
	get_tree().quit()
