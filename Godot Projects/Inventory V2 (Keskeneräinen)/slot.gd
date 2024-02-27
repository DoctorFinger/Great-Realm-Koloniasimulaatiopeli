extends TextureRect
signal slot_entered(slot)
signal slot_exited(slot)

@onready var filter = $SlotFilter

var slot_ID
var is_hovering := false
enum States { DEFAULT, TAKEN, FREE }
var state := States.DEFAULT
var item_stored = null

func set_color(slot_state:States = States.DEFAULT) ->void:
	match slot_state:
		States.DEFAULT:
			filter.color = Color(Color.WHITE, 0)
		States.TAKEN:
			filter.color = Color(Color.RED, 0.4)
		States.FREE:
			filter.color = Color(Color.BLUE, 0.4)

func _process(delta):
	if get_global_rect().has_point(get_global_mouse_position()):
		if !is_hovering:
			is_hovering = true;
			emit_signal("slot_entered", self)
	else:
		if is_hovering:
			is_hovering = false;
			emit_signal("slot_exited", self)


