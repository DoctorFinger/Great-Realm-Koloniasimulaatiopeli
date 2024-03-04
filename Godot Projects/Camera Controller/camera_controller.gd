extends Camera2D

@export var zoom_min	  :float = 		0.2
@export var zoom_max 	  :float = 		4
@export var zoom_speed 	  :float = 		0.35;
@export var zoom_to_mouse :bool = 		true;

@export var pan_speed :float = 1
@export var movement_interpolation :float = 0.05
@export_category("boundaries")
@export var boundary_control_node: Control = null

var zoom_min_temp			:float = zoom_min
var zoom_level   			:Vector2 = 	Vector2.ONE;
var pan_position  			:Vector2 = position
var pan_offset	  			:Vector2 = Vector2(0, 0)
var camera_lerp			  	:float = 1.5 / max(movement_interpolation, 0.01)
var viewport_area	  	  	:Rect2 = Rect2(0, 0, 0, 0)
var boundary_area 			:Rect2 = Rect2(0, 0, 0, 0)
var viewport_resolution		:Vector2 = Vector2(0, 0)

func _ready():
	get_tree().get_root().size_changed.connect(reset_zoom) 
	zoom_min_temp = zoom_min;
	initialize()
	
func reset_zoom():
	zoom_min  		= zoom_min_temp
	zoom_level   	= Vector2.ONE;
	pan_position  	= position
	viewport_area	= Rect2(0, 0, 0, 0)
	boundary_area 	= Rect2(0, 0, 0, 0)
	
func initialize():
	if boundary_control_node:
		update_viewport_area();
		update_zoom_limits();
		limit_camera_to_bounds();
		
func create_input_action(action_name: String, physical_keycode:int):
	if not InputMap.has_action(action_name):
		var key = InputEventKey.new()
		key.physical_keycode = physical_keycode
		InputMap.add_action(action_name)
		InputMap.action_add_event(action_name, key)
		
func update_input_actions():
	create_input_action("camera_left",  KEY_A)
	create_input_action("camera_right", KEY_D)
	create_input_action("camera_up", 	KEY_W)
	create_input_action("camera_down",  KEY_S)
	
func update_zoom_limits():
		var min = max(( viewport_area.size.x / boundary_area.size.x),  ( viewport_area.size.y / boundary_area.size.y));
		print("current: ", zoom_min)
		zoom_min = max(zoom_min, min)
		print("after: ", zoom_min)
		if zoom_min > min(zoom_level.x, zoom_level.y):
			zoom_level.x = zoom_min
			zoom_level.y = zoom_min
			zoom.x = zoom_min
			zoom.y = zoom_min

			
	
func _process(delta):
	handle_keyboard_camera_movement(delta)
	update_camera_transform(delta)
	
func update_viewport_area():
	boundary_area = boundary_control_node.get_global_rect()
	var viewport_rect = get_viewport_rect()
	var scaled_size = (viewport_rect.size / zoom_level)
	var camera_rotation = -global_rotation
	var rotated_offset = pan_offset.rotated(camera_rotation)  
	var adjusted_position = (pan_position + rotated_offset) - scaled_size / 2  
	
	viewport_area.position = adjusted_position;
	viewport_area.size = scaled_size
	
	if viewport_resolution != viewport_rect.size:
		viewport_resolution = viewport_rect.size
		update_zoom_limits();
	

func limit_camera_to_bounds():
	if boundary_control_node:
		update_viewport_area()
		var distance_to_bottom_bound =  min(boundary_area.end.y - (boundary_area.end.y * (viewport_area.end.y / boundary_area.end.y)), 0)
		var distance_to_top_bound =  max(boundary_area.position.y - (boundary_area.position.y * (viewport_area.position.y / boundary_area.position.y)), 0)
		var distance_to_right_bound = min(boundary_area.end.x - (boundary_area.end.x * (viewport_area.end.x / boundary_area.end.x)), 0)
		var distance_to_left_bound = max(boundary_area.position.x - (boundary_area.position.x * (viewport_area.position.x / boundary_area.position.x)), 0)
		pan_position.x += distance_to_right_bound + distance_to_left_bound
		pan_position.y += distance_to_bottom_bound + distance_to_top_bound
		

func handle_keyboard_camera_movement(delta):
	var movement = Vector2.ZERO
	if Input.is_action_pressed("camera_left"):
		movement.x -= 1
	elif Input.is_action_pressed("camera_right"):
		movement.x += 1
	if Input.is_action_pressed("camera_up"):
		movement.y -= 1
	elif Input.is_action_pressed("camera_down"):
		movement.y += 1
		
	movement = movement.normalized() * pan_speed * (Vector2.ONE / zoom_level) * delta * 1000
	pan_position += movement
	limit_camera_to_bounds()

func _input(event):
	if event is InputEventMouseButton and event.is_pressed():
		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			zoom_camera(-zoom_speed)
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			zoom_camera(zoom_speed)
			
	if event is InputEventMouseMotion:
		if event.button_mask == MOUSE_BUTTON_MASK_MIDDLE:
			pan_camera(event)
		
func zoom_camera(zoom_change):
	var adjusted_zoom_speed = zoom_speed * zoom_level.x

	if zoom_to_mouse:
		var offset_from_mouse = get_global_mouse_position() - global_position
		var old_zoom = zoom_level
		zoom_level.x = clamp(zoom_level.x + zoom_change * adjusted_zoom_speed, zoom_min, zoom_max)
		zoom_level.y = clamp(zoom_level.y + zoom_change * adjusted_zoom_speed, zoom_min, zoom_max)
		var zoom_ratio = old_zoom / zoom_level
		pan_offset = (pan_offset - offset_from_mouse) * zoom_ratio + offset_from_mouse
	else:
		zoom_level.x = clamp(zoom_level.x + zoom_change * adjusted_zoom_speed, zoom_min, zoom_max)
		zoom_level.y = clamp(zoom_level.y + zoom_change * adjusted_zoom_speed, zoom_min, zoom_max)
		pan_offset.x = 0
		pan_offset.y = 0
		
	limit_camera_to_bounds()

func pan_camera(event):
	pan_position -= event.relative * pan_speed * (Vector2.ONE / zoom_level)
	limit_camera_to_bounds()
		

func update_camera_transform(delta):
	self.offset = offset.cubic_interpolate_in_time(pan_offset, offset, pan_offset, delta * camera_lerp, 0, 0, 1)
	self.position = position.cubic_interpolate_in_time(pan_position, position, pan_position, delta * camera_lerp, 0, 0, 1)
	self.zoom = zoom.cubic_interpolate_in_time(zoom_level, zoom, zoom_level, delta * camera_lerp, 0, 0, 1)
