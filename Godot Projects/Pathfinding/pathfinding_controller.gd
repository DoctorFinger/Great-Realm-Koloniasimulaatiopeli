extends Control
@export var path_tiles: TileMap = null;
@export var target: ColorRect = null;
@onready var targets = get_tree().get_nodes_in_group("NPC")

var top_tiles: Array[Vector2i] = []
var contouring_tiles: Array[Vector2i] = []
var clicked_tile: Vector2i = Vector2i.ZERO
var clicked_position: Vector2 = Vector2i.ZERO

func get_topmost_tiles() -> Array[Vector2i]:
	var topmost_tiles :Array[Vector2i] = []
	var used_cells = path_tiles.get_used_cells(0)
	
	for cell in used_cells:
		var tile_above_coords = Vector2i(cell.x, cell.y) - Vector2i(0, 1)
		if tile_above_coords not in used_cells:
			topmost_tiles.append(tile_above_coords)
			
	# sort the tiles
	var length = topmost_tiles.size()
	for i in range(length):
		for j in range(i + 1, length):
			if topmost_tiles[i].x > topmost_tiles[j].x:
				var temp = Vector2i(topmost_tiles[i].x, topmost_tiles[i].y)
				topmost_tiles[i] = topmost_tiles[j]
				topmost_tiles[j] = temp
				
	return topmost_tiles
	
func get_contouring_tiles(top_tiles: Array[Vector2i]) -> Array[Vector2i]:
	var contour_tiles: Array[Vector2i] = [top_tiles[0]]
	var contour_index = 0
	var total_length = top_tiles.size() - 1
	var index = 1
	
	while index < total_length:
		var current_tile = top_tiles[index]
		var previous_tile = top_tiles[index - 1]
		var next_tile = top_tiles[index + 1]
		
		if current_tile.y !=  contour_tiles[contour_index].y:
			if(previous_tile != contour_tiles[contour_index]):
				contour_tiles.append(previous_tile)
				contour_index += 1

			contour_tiles.append(current_tile)
			contour_index += 1
			
		if next_tile.y != current_tile.y:
			contour_tiles.append(current_tile)
			contour_tiles.append(next_tile)
			contour_index += 2

		index += 1
		
	if contour_tiles[contour_tiles.size() -1] != top_tiles[top_tiles.size() -1]:
		contour_tiles.append(top_tiles[top_tiles.size() -1]);

	return contour_tiles
	
func get_tile_positions_from_range(x_min:int, x_max:int, tiles: Array[Vector2i]) -> Array[Vector2]:
	var min = min(x_min, x_max)
	var max = max(x_min, x_max)
	var range :Array[Vector2] = []
	
	for tile in tiles:
		var global = path_tiles.map_to_local(tile)

		if global.x >= min and global.x <= max:
			range.append(global)
			
	return range;
	
func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.is_pressed():
				var _tile = path_tiles.local_to_map(get_global_mouse_position())
				for tile in top_tiles:
					if _tile.x == tile.x:
						clicked_tile = tile
						clicked_position = path_tiles.map_to_local(clicked_tile)
						for npc in targets:
							var positions = get_tile_positions_from_range(npc.position.x, clicked_position.x, contouring_tiles)
							positions.append(clicked_position)
							npc.move_to_target(positions)
				
func _ready():
	top_tiles = get_topmost_tiles();
	contouring_tiles = get_contouring_tiles(top_tiles)
	draw.connect(draw_contouring_tiles)

func draw_contouring_tiles():
	for tile in contouring_tiles:
		var global = path_tiles.map_to_local(tile)
		draw_rect(Rect2(global.x, global.y, 10, 10), Color(0.5, 0, 0, 1), true)
		
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
	

