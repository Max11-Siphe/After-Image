extends CharacterBody2D

signal goal_reached
signal swap_zone_entered

@export var is_inverted: bool = false
@export var spawn_grid_pos: Vector2i = Vector2i(1, 1)
@export var goal_grid_pos: Vector2i = Vector2i(23, 12)
@export var swap_grid_pos: Vector2i = Vector2i(-1, -1)
@export var maze_layer: TileMapLayer

var grid_pos: Vector2i
var is_moving: bool = false
var has_reached_goal: bool = false

func _ready() -> void:
	# Set texture dynamically based on inverted state
	var sprite = $Sprite2D
	if sprite:
		if is_inverted:
			sprite.texture = load("res://placeholder_art/char2.png")
		else:
			sprite.texture = load("res://placeholder_art/char1.png")
	reset_to_start()

func update_sprite() -> void:
	var sprite = $Sprite2D
	if sprite:
		if is_inverted:
			sprite.texture = load("res://placeholder_art/char2.png")
		else:
			sprite.texture = load("res://placeholder_art/char1.png")

func reset_to_start() -> void:
	grid_pos = spawn_grid_pos
	has_reached_goal = false
	is_moving = false
	# Center character in tile (each tile is 32x32, offset by 16, 16)
	position = Vector2(grid_pos.x * 32 + 16, grid_pos.y * 32 + 16)

func try_move(input_dir: Vector2i) -> void:
	var actual_dir = -input_dir if is_inverted else input_dir
	var target_pos = grid_pos + actual_dir
	
	if is_walkable(target_pos):
		grid_pos = target_pos
		move_to_grid_pos()

func is_walkable(coords: Vector2i) -> bool:
	# Check maze boundaries (25 tiles wide, 14 tiles high)
	if coords.x < 0 or coords.x >= 25 or coords.y < 0 or coords.y >= 14:
		return false
		
	if maze_layer:
		var tile_data = maze_layer.get_cell_tile_data(coords)
		if tile_data:
			var is_wall = tile_data.get_custom_data("is_wall")
			if is_wall:
				return false
	return true

func move_to_grid_pos() -> void:
	is_moving = true
	var target_pixel_pos = Vector2(grid_pos.x * 32 + 16, grid_pos.y * 32 + 16)
	
	var tween = create_tween()
	tween.tween_property(self, "position", target_pixel_pos, 0.12).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
	tween.tween_callback(func():
		is_moving = false
		check_goal()
		check_swap()
	)

func check_swap() -> void:
	if swap_grid_pos.x >= 0 and grid_pos == swap_grid_pos:
		swap_zone_entered.emit()

func check_goal() -> void:
	var on_goal = (grid_pos == goal_grid_pos)
	if on_goal != has_reached_goal:
		has_reached_goal = on_goal
		goal_reached.emit()
