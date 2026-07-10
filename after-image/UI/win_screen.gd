extends CanvasLayer

signal primary_pressed
signal retry_pressed
signal quit_pressed

@onready var primary_button: Button = $Panel/VBoxContainer/PrimaryButton
@onready var retry_button: Button = $Panel/VBoxContainer/RetryButton
@onready var quit_button: Button = $Panel/VBoxContainer/QuitButton
@onready var title_label: Label = $Panel/VBoxContainer/TitleLabel
@onready var desc_label: Label = $Panel/VBoxContainer/DescLabel

func _ready() -> void:
	primary_button.pressed.connect(func(): primary_pressed.emit())
	retry_button.pressed.connect(func(): retry_pressed.emit())
	quit_button.pressed.connect(func(): quit_pressed.emit())

func setup_screen(is_last_level: bool) -> void:
	# Ensure onready variables are initialized if called immediately
	if not primary_button:
		primary_button = $Panel/VBoxContainer/PrimaryButton
	if not retry_button:
		retry_button = $Panel/VBoxContainer/RetryButton
	if not quit_button:
		quit_button = $Panel/VBoxContainer/QuitButton
	if not title_label:
		title_label = $Panel/VBoxContainer/TitleLabel
	if not desc_label:
		desc_label = $Panel/VBoxContainer/DescLabel
		
	if is_last_level:
		title_label.text = "GAME COMPLETE!"
		desc_label.text = "Congratulations! You have completed all levels."
		primary_button.text = "Restart Game"
	else:
		title_label.text = "LEVEL COMPLETE!"
		desc_label.text = "Both characters reached their goals!"
		primary_button.text = "Next Level"
