extends CanvasLayer

signal restart_game_pressed
signal return_to_title_pressed
signal quit_pressed

@onready var background: ColorRect = $Background
@onready var title_label: Label = $VBoxContainer/TitleLabel
@onready var desc_label: Label = $VBoxContainer/DescLabel

@onready var restart_button: Button = $VBoxContainer/RestartButton
@onready var return_to_title_button: Button = $VBoxContainer/ReturnToTitleButton
@onready var quit_button: Button = $VBoxContainer/QuitButton

func _ready() -> void:
	restart_button.pressed.connect(func(): restart_game_pressed.emit())
	return_to_title_button.pressed.connect(func(): return_to_title_pressed.emit())
	quit_button.pressed.connect(func(): quit_pressed.emit())

func setup_ending(type: String) -> void:
	match type:
		"shared":
			background.color = Color(0.12, 0.25, 0.16, 0.98) # Greenish
			title_label.text = "THE DREAM SHARED"
			desc_label.text = "You reached the Dream Core together. The dream is shared, and both of you are whole."
		"p1_solo":
			background.color = Color(0.3, 0.12, 0.12, 0.98) # Reddish
			title_label.text = "THE DREAM CLAIMED ALONE"
			desc_label.text = "The first traveller claimed the Dream Core alone. The other was left in the void."
		"p2_solo":
			background.color = Color(0.2, 0.12, 0.3, 0.98) # Purplish
			title_label.text = "THE DREAM GIVEN AWAY"
			desc_label.text = "You stepped aside and allowed the other traveller to claim the Dream Core."
