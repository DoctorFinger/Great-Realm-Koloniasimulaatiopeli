extends Control
@onready var slot_scene = preload("res://slot.tscn")
@onready var item_scene = preload("res://item.tscn")
@onready var grid_container = $background/Margin/VBoxContainer/Slots/Grid

var slot_array := []
var slot_amount := 32;
var item_held = null

func _ready():
	for i in range(slot_amount):
		create_slot();
	
func create_slot():
	var new_slot = slot_scene.instantiate()
	new_slot.slot_ID = slot_array.size();
	new_slot.slot_entered.connect(on_slot_mouse_entered)
	new_slot.slot_exited.connect(on_slot_mouse_exited);
	grid_container.add_child(new_slot) 

func on_slot_mouse_entered(slot):
	slot.set_color(slot.States.FREE)

func on_slot_mouse_exited(slot):
	slot.set_color(slot.States.DEFAULT)
	
func _on_button_pressed():
	var new_item = item_scene.instantiate();
	new_item.load_item(4)
	new_item.selected = true;
	item_held = new_item;
	add_child(new_item)
	pass # Replace with function body.
