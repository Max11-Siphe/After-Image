extends Node2D

var color: Color = Color.WHITE

func _draw() -> void:
	# Draw a footprint (shoe-print)
	# Sole: circle at Vector2(0, -3) with radius 5
	# Heel: circle at Vector2(0, 4) with radius 3
	draw_circle(Vector2(0, -3), 5.0, color)
	draw_circle(Vector2(0, 4), 3.0, color)
