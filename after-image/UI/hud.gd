extends CanvasLayer

@onready var level_label: Label = $Panel/MarginContainer/VBoxContainer/TopRow/LevelLabel
@onready var maze_label: Label = $Panel/MarginContainer/VBoxContainer/TopRow/MazeLabel
@onready var status_label: Label = $Panel/MarginContainer/VBoxContainer/BottomRow/StatusLabel

func set_level_info(level_num: int, total_levels: int, theme_name: String, difficulty: String) -> void:
	if level_label:
		level_label.text = "Level %d/%d: %s (%s)" % [level_num, total_levels, theme_name, difficulty]

func set_viewing_maze(index: int) -> void:
	if maze_label:
		maze_label.text = "Viewing: Maze %d" % index

func set_completion_status(p1_done: bool, p2_done: bool) -> void:
	if status_label:
		var p1_str = "Complete" if p1_done else "Active"
		var p2_str = "Complete" if p2_done else "Active"
		status_label.text = "P1: %s  |  P2: %s" % [p1_str, p2_str]
