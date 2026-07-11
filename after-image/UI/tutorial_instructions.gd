extends CanvasLayer

signal tutorial_started

@onready var begin_button: Button = $Panel/VBoxContainer/BeginButton

func _ready() -> void:
	begin_button.pressed.connect(func(): tutorial_started.emit())
