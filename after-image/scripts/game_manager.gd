extends Node2D

const LEVEL_DATA = [
	{
		"name": "Tutorial",
		"difficulty": "Easy",
		"maze1_scene": "res://levels/tutorial_maze_1.tscn",
		"maze2_scene": "res://levels/tutorial_maze_2.tscn"
	},
	{
		"name": "Metro Grid",
		"difficulty": "Medium",
		"maze1_scene": "res://levels/maze_1_city.tscn",
		"maze2_scene": "res://levels/maze_2_city.tscn"
	},
	{
		"name": "Castle Keep",
		"difficulty": "Hard",
		"maze1_scene": "res://levels/maze_1_dungeon.tscn",
		"maze2_scene": "res://levels/maze_2_dungeon.tscn"
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

func _ready() -> void:
	setup_input_actions()
	
	# Connect win screen signals
	win_screen.primary_pressed.connect(_on_win_screen_primary)
	win_screen.retry_pressed.connect(_on_win_screen_retry)
	win_screen.quit_pressed.connect(_on_win_screen_quit)
	
	# Load the first level
	load_level(0)

func setup_input_actions() -> void:
	var actions = {
		"move_left": [KEY_LEFT, KEY_A],
		"move_right": [KEY_RIGHT, KEY_D],
		"move_up": [KEY_UP, KEY_W],
		"move_down": [KEY_DOWN, KEY_S],
		"switch_view": [KEY_TAB]
	}
	for action in actions:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
			for key in actions[action]:
				var event = InputEventKey.new()
				event.physical_keycode = key
				InputMap.action_add_event(action, event)

func _unhandled_input(event: InputEvent) -> void:
	if is_game_won:
		return
		
	if not is_instance_valid(character1) or not is_instance_valid(character2):
		return
		
	# Ignore input while players are moving to keep them synced
	if character1.is_moving or character2.is_moving:
		return
		
	if event.is_action_pressed("switch_view"):
		toggle_view()
		get_viewport().set_input_as_handled()
		return
		
	var dir = Vector2i.ZERO
	if event.is_action_pressed("move_left"):
		dir = Vector2i.LEFT
	elif event.is_action_pressed("move_right"):
		dir = Vector2i.RIGHT
	elif event.is_action_pressed("move_up"):
		dir = Vector2i.UP
	elif event.is_action_pressed("move_down"):
		dir = Vector2i.DOWN
		
	if dir != Vector2i.ZERO:
		character1.try_move(dir)
		character2.try_move(dir) # Sent as positive, Character 2 will invert it internally
		get_viewport().set_input_as_handled()

func load_level(index: int) -> void:
	# 1. Clean up existing mazes and characters immediately
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
	
	current_level_index = index
	
	var data = LEVEL_DATA[index]
	
	# 2. Instantiate and add new mazes
	var m1_res = load(data.maze1_scene)
	maze1 = m1_res.instantiate()
	maze1.position = Vector2(80, 46)
	add_child(maze1)
	
	var m2_res = load(data.maze2_scene)
	maze2 = m2_res.instantiate()
	maze2.position = Vector2(80, 46)
	add_child(maze2)
	
	# 3. Instantiate and add characters
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
	
	# 4. Restart gameplay loop
	restart_game()

func _on_swap_zone_entered() -> void:
	if is_game_won:
		return
	character1.is_inverted = !character1.is_inverted
	character2.is_inverted = !character2.is_inverted
	character1.update_sprite()
	character2.update_sprite()
	toggle_view()

func toggle_view() -> void:
	if current_view == 1:
		current_view = 2
	else:
		current_view = 1
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
		
	# Update occupied status of goals
	if is_instance_valid(maze1):
		maze1.set_occupied(character1.has_reached_goal)
	if is_instance_valid(maze2):
		maze2.set_occupied(character2.has_reached_goal)
		
	hud.set_completion_status(character1.has_reached_goal, character2.has_reached_goal)
	check_win_condition()

func check_win_condition() -> void:
	if character1.has_reached_goal and character2.has_reached_goal:
		is_game_won = true
		
		# Play win flash animation on both goals
		if is_instance_valid(maze1):
			maze1.play_win_flash()
		if is_instance_valid(maze2):
			maze2.play_win_flash()
			
		# Show win screen after a short delay (e.g. 0.8 seconds) to let flash play
		await get_tree().create_timer(0.8).timeout
		
		# If game was restarted or changed during the timer, check if it's still won
		if not is_game_won:
			return
			
		win_screen.setup_screen(current_level_index == LEVEL_DATA.size() - 1)
		win_screen.visible = true

func restart_game() -> void:
	is_game_won = false
	win_screen.visible = false
	current_view = 1
	
	if is_instance_valid(character1):
		character1.reset_to_start()
	if is_instance_valid(character2):
		character2.reset_to_start()
		
	update_view_visibility()
	
	if is_instance_valid(maze1):
		maze1.set_occupied(false)
	if is_instance_valid(maze2):
		maze2.set_occupied(false)
		
	hud.set_level_info(
		current_level_index + 1,
		LEVEL_DATA.size(),
		LEVEL_DATA[current_level_index].name,
		LEVEL_DATA[current_level_index].difficulty
	)
	hud.set_completion_status(false, false)

func _on_win_screen_primary() -> void:
	if current_level_index == LEVEL_DATA.size() - 1:
		# Restart Game (returns to Level 1)
		load_level(0)
	else:
		# Next Level
		load_level(current_level_index + 1)

func _on_win_screen_retry() -> void:
	restart_game()

func _on_win_screen_quit() -> void:
	quit_game()

func quit_game() -> void:
	get_tree().quit()
