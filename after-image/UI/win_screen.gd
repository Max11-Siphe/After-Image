extends CanvasLayer

signal restart_pressed
signal quit_pressed

func _ready() -> void:
	$Panel/VBoxContainer/RestartButton.pressed.connect(func(): restart_pressed.emit())
	$Panel/VBoxContainer/QuitButton.pressed.connect(func(): quit_pressed.emit())
