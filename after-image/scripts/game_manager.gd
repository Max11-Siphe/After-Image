extends Node2D

@onready var maze1: Node2D = $Maze1
@onready var maze2: Node2D = $Maze2
@onready var character1: CharacterBody2D = $Maze1/Character1
@onready var character2: CharacterBody2D = $Maze2/Character2
@onready var hud: CanvasLayer = $HUD
@onready var win_screen: CanvasLayer = $WinScreen

var current_view: int = 1
var is_game_won: bool = false

func _ready() -> void:
	setup_input_actions()
	
	# Connect player goal signals
	character1.goal_reached.connect(_on_character_goal_reached)
	character2.goal_reached.connect(_on_character_goal_reached)
	
	# Connect win screen signals
	win_screen.restart_pressed.connect(restart_game)
	win_screen.quit_pressed.connect(quit_game)
	
	# Initialize gameplay dependencies
	# Character 1 moves in Maze 1
	character1.maze_layer = maze1.tilemap_layer
	character1.spawn_grid_pos = maze1.spawn_grid_pos
	character1.goal_grid_pos = maze1.goal_grid_pos
	
	# Character 2 moves in Maze 2
	character2.maze_layer = maze2.tilemap_layer
	character2.spawn_grid_pos = maze2.spawn_grid_pos
	character2.goal_grid_pos = maze2.goal_grid_pos
	
	# Reset states to begin
	restart_game()

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

func toggle_view() -> void:
	if current_view == 1:
		current_view = 2
	else:
		current_view = 1
	update_view_visibility()

func update_view_visibility() -> void:
	if current_view == 1:
		maze1.visible = true
		maze2.visible = false
	else:
		maze1.visible = false
		maze2.visible = true
	hud.set_viewing_maze(current_view)

func _on_character_goal_reached() -> void:
	hud.set_completion_status(character1.has_reached_goal, character2.has_reached_goal)
	check_win_condition()

func check_win_condition() -> void:
	if character1.has_reached_goal and character2.has_reached_goal:
		is_game_won = true
		win_screen.visible = true

func restart_game() -> void:
	is_game_won = false
	win_screen.visible = false
	current_view = 1
	
	character1.reset_to_start()
	character2.reset_to_start()
	
	update_view_visibility()
	hud.set_completion_status(false, false)

func quit_game() -> void:
	get_tree().quit()
