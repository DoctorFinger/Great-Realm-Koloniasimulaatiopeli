extends Node2D
@export var icon_rect:TextureRect = null;
var item_ID:int
var item_grids := []
var selected = false;
var grid_anchor = null;



# Called every frame. 'delta' is the elapsed time since the previous frame.
func _ready():
	load_item(3)
	selected = true;

func _process(delta):
	if selected:
		global_position = lerp(global_position, get_global_mouse_position(), 25*delta)

func load_item(item_id: int) -> void:
	var icon_path = "res://Assets/Icons/" + DataHandler.item_data[str(item_id)]["FileName"]
	var loaded_texture = load(icon_path);
	print("LOADED TEXTURE:", loaded_texture)
	icon_rect.texture = loaded_texture;
	for grid in DataHandler.item_grid_data[str(item_id)]:
		var converted_data := []
		for i in grid:
			converted_data.push_back(int(i))
		item_grids.push_back(converted_data)
	
