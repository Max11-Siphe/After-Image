extends CanvasLayer

signal intro_finished(success: bool)

@onready var title_screen: Control = $TitleScreen
@onready var narrative_screen: Control = $NarrativeScreen
@onready var guardian_screen: Control = $GuardianScreen
@onready var game_over_screen: Control = $GameOverScreen

@onready var start_button: Button = $TitleScreen/VBoxContainer/StartButton
@onready var quit_button: Button = $TitleScreen/VBoxContainer/QuitButton

@onready var narrative_label: Label = $NarrativeScreen/VBoxContainer/NarrativeLabel
@onready var continue_button: Button = $NarrativeScreen/VBoxContainer/ContinueButton

@onready var yes_button: Button = $GuardianScreen/VBoxContainer/HBoxContainer/YesButton
@onready var no_button: Button = $GuardianScreen/VBoxContainer/HBoxContainer/NoButton

@onready var return_to_title_button: Button = $GameOverScreen/VBoxContainer/ReturnToTitleButton
@onready var game_over_quit_button: Button = $GameOverScreen/VBoxContainer/QuitButton

func _ready() -> void:
	# Connections
	start_button.pressed.connect(_on_start_pressed)
	quit_button.pressed.connect(_on_quit_pressed)
	continue_button.pressed.connect(_on_continue_pressed)
	yes_button.pressed.connect(_on_yes_pressed)
	no_button.pressed.connect(_on_no_pressed)
	return_to_title_button.pressed.connect(_on_return_to_title_pressed)
	game_over_quit_button.pressed.connect(_on_quit_pressed)
	
	show_title_screen()

func show_title_screen() -> void:
	title_screen.visible = true
	narrative_screen.visible = false
	guardian_screen.visible = false
	game_over_screen.visible = false

func _on_start_pressed() -> void:
	title_screen.visible = false
	show_narrative()

func _on_quit_pressed() -> void:
	get_tree().quit()

func show_narrative() -> void:
	narrative_screen.visible = true
	narrative_label.text = ""
	continue_button.visible = false
	
	var full_text = "One day, you fell asleep yearning to dream at night. Instead of another blank sleep, you were given the chance to fight for your dreams."
	var current_text = ""
	for i in range(full_text.length()):
		if not narrative_screen.visible:
			return
		current_text += full_text[i]
		narrative_label.text = current_text
		await get_tree().create_timer(0.04).timeout
	
	continue_button.visible = true

func _on_continue_pressed() -> void:
	narrative_screen.visible = false
	show_guardian_scene()

func show_guardian_scene() -> void:
	guardian_screen.visible = true

func _on_yes_pressed() -> void:
	guardian_screen.visible = false
	intro_finished.emit(true)

func _on_no_pressed() -> void:
	guardian_screen.visible = false
	show_game_over()

func show_game_over() -> void:
	game_over_screen.visible = true

func _on_return_to_title_pressed() -> void:
	game_over_screen.visible = false
	show_title_screen()
