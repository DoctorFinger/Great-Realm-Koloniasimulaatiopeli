extends Node
var item_data := {}
var item_grid_data := {}
@onready var item_data_path = "res://Data/item_data.json"

# Called when the node enters the scene tree for the first time.
func _ready():
	load_data(item_data_path)
	set_grid_data()
	pass # Replace with function body.
	
func load_data(file_path):
	if not FileAccess.file_exists(file_path):
		printerr("Item data file not found!")
		return
	var file = FileAccess.open(file_path, FileAccess.READ)
	item_data = JSON.parse_string(file.get_as_text());
	file.close();
	print(item_data)
		
# Called every frame. 'delta' is the elapsed time since the previous frame.
func set_grid_data():
	for item in item_data.keys():
		var temp_grid_array := []
		for point in item_data[item]["Grid"].split("/"):
			temp_grid_array.push_back(point.split(","))
			
		item_grid_data[item] = temp_grid_array
	print(item_grid_data)
		
