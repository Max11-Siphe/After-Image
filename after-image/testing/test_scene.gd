extends Node2D

@onready var maze: Node2D = $Maze
@onready var character1: CharacterBody2D = $Maze/Character1
@onready var character2: CharacterBody2D = $Maze/Character2

func _ready() -> void:
	setup_input_actions()
	
	# Bind characters to the test maze
	character1.maze_layer = maze.tilemap_layer
	character1.spawn_grid_pos = maze.spawn_grid_pos
	character1.goal_grid_pos = maze.goal_grid_pos
	
	character1.reset_to_start()
	character2.reset_to_start()

func setup_input_actions() -> void:
	var actions = {
		"move_left": [KEY_LEFT, KEY_A],
		"move_right": [KEY_RIGHT, KEY_D],
		"move_up": [KEY_UP, KEY_W],
		"move_down": [KEY_DOWN, KEY_S]
	}
	for action in actions:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
			for key in actions[action]:
				var event = InputEventKey.new()
				event.physical_keycode = key
				InputMap.action_add_event(action, event)

func _unhandled_input(event: InputEvent) -> void:
	if character1.is_moving or character2.is_moving:
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
		character2.try_move(dir)
