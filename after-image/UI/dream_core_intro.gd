extends CanvasLayer

signal continue_pressed

@onready var continue_btn: Button = $Panel/VBoxContainer/ContinueButton

func _ready() -> void:
	continue_btn.pressed.connect(func(): continue_pressed.emit())
