extends Control
@onready var inventory:Inventory = preload("res://inventory/inventory.tres")
@onready var slots:Array = $Background/GridContainer.get_children()

var is_open = false

func _ready():
	update_inventory()
	close_inventory()	

func _process(delta):
	if Input.is_action_just_pressed("toggle_inventory"):
		if is_open:
			close_inventory()
		else:
			open_inventory()

func open_inventory():
	visible = true;
	is_open = true;

func close_inventory():
	visible = false;
	is_open = false;
	
func update_inventory():
	for i in range(min(inventory.items.size(), slots.size())):
		slots[i].update(inventory.items[i]);
