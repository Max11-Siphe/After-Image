extends Node2D

@export_multiline var map_string: String

@onready var tilemap_layer: TileMapLayer = $TileMapLayer
@onready var goal_sprite: Sprite2D = $Goal

var spawn_grid_pos: Vector2i
var goal_grid_pos: Vector2i
var swap_grid_pos: Vector2i = Vector2i(-1, -1)

var _glow_tween: Tween
var _flash_tween: Tween

func _ready() -> void:
	setup_maze()

func setup_maze() -> void:
	if not tilemap_layer:
		return
		
	tilemap_layer.clear()
	
	var lines = map_string.strip_edges().split("\n")
	for y in range(lines.size()):
		var line = lines[y].strip_edges()
		if line.is_empty():
			continue
		for x in range(line.length()):
			if x >= 25 or y >= 14:
				continue # Protect against bounds overflow
			var cell_char = line[x]
			var coords = Vector2i(x, y)
			
			if cell_char == "#":
				# Wall tile: Source ID 0, atlas (0,0)
				tilemap_layer.set_cell(coords, 0, Vector2i.ZERO)
			else:
				# Floor tile: Source ID 1, atlas (0,0)
				tilemap_layer.set_cell(coords, 1, Vector2i.ZERO)
				
			if cell_char == "S":
				spawn_grid_pos = coords
			elif cell_char == "G":
				goal_grid_pos = coords
				if goal_sprite:
					goal_sprite.position = Vector2(coords.x * 32 + 16, coords.y * 32 + 16)
			elif cell_char == "X":              # ADD THIS BLOCK
				swap_grid_pos = coords

func set_occupied(occupied: bool) -> void:
	if _glow_tween:
		_glow_tween.kill()
		_glow_tween = null
	
	if not goal_sprite:
		return
		
	if occupied:
		# Pulsate scale and modulate to represent a glow
		_glow_tween = create_tween().set_loops()
		_glow_tween.tween_property(goal_sprite, "scale", Vector2(1.2, 1.2), 0.4).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
		_glow_tween.parallel().tween_property(goal_sprite, "modulate", Color(1.5, 2.0, 1.5, 1.0), 0.4).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
		_glow_tween.tween_property(goal_sprite, "scale", Vector2(1.0, 1.0), 0.4).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN)
		_glow_tween.parallel().tween_property(goal_sprite, "modulate", Color(1.0, 1.2, 1.0, 1.0), 0.4).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN)
	else:
		goal_sprite.scale = Vector2(1.0, 1.0)
		goal_sprite.modulate = Color.WHITE

func play_win_flash() -> void:
	if _glow_tween:
		_glow_tween.kill()
		_glow_tween = null
	if _flash_tween:
		_flash_tween.kill()
		_flash_tween = null
		
	if not goal_sprite:
		return
		
	# Rapid flash
	_flash_tween = create_tween().set_loops()
	_flash_tween.tween_property(goal_sprite, "modulate", Color(3.0, 3.0, 3.0, 1.0), 0.1)
	_flash_tween.tween_property(goal_sprite, "modulate", Color(0.2, 0.2, 0.2, 1.0), 0.1)
