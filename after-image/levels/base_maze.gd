extends Node2D

@export_multiline var map_string: String

@onready var tilemap_layer: TileMapLayer = $TileMapLayer
@onready var goal_sprite: Sprite2D = $Goal

var spawn_grid_pos: Vector2i
var goal_grid_pos: Vector2i

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
