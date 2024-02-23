extends Camera2D

var zoom_to_mouse :bool = 		true;
var zoom_min	  :Vector2 = 	Vector2(0.2, 0.2);
var zoom_max 	  :Vector2 = 	Vector2(4, 4);
var zoom_speed 	  :Vector2 = 	Vector2(0.35, 0.35);
var zooom_level   :Vector2 = 	zoom;

var pan_speed	  :Vector2 = Vector2(1, 1)
var pan_position  :Vector2 = position
var pan_offset	  :Vector2 = Vector2(0, 0)

var camera_interp		  :float = 0.1
var camera_lerp			  :float = 1.5 / max(camera_interp, 0.01)

# Päivittää kameran sijainnin joka frami, vaikka kamera ei liikkuisi. Tarvitsee paremman ratkaisun.
func _process(delta):
	update_camera_transform(delta)
	

func _input(event):
	if event is InputEventMouseButton and event.is_pressed():
		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			zoom_camera(-zoom_speed)
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			zoom_camera(zoom_speed)

func _unhandled_input(event):
	if event is InputEventMouseMotion:
		if event.button_mask == MOUSE_BUTTON_MASK_MIDDLE:
			pan_camera(event)
		
func zoom_camera(zoom_change):
	var adjusted_zoom_speed = zoom_speed * zooom_level.x

	if zoom_to_mouse:
		var offset_from_mouse = get_global_mouse_position() - global_position
		var old_zoom = zooom_level
		zooom_level.x = clamp(zooom_level.x + zoom_change.x * adjusted_zoom_speed.x, zoom_min.x, zoom_max.x)
		zooom_level.y = clamp(zooom_level.y + zoom_change.y * adjusted_zoom_speed.y, zoom_min.y, zoom_max.y)
		var zoom_ratio = old_zoom / zooom_level
		pan_offset = (pan_offset - offset_from_mouse) * zoom_ratio + offset_from_mouse

	else:
		zooom_level.x = clamp(zooom_level.x + zoom_change.x * adjusted_zoom_speed.x, zoom_min.x, zoom_max.x)
		zooom_level.y = clamp(zooom_level.y + zoom_change.y * adjusted_zoom_speed.y, zoom_min.y, zoom_max.y)
		pan_offset.x = 0
		pan_offset.y = 0

func pan_camera(event):
	pan_position -= event.relative * pan_speed * (Vector2(1, 1) / zooom_level)

func update_camera_transform(delta):
	self.offset = offset.cubic_interpolate_in_time(pan_offset, offset, pan_offset, delta * camera_lerp, 0, 0, 1)
	self.position = position.cubic_interpolate_in_time(pan_position, position, pan_position, delta * camera_lerp, 0, 0, 1)
	self.zoom = zoom.cubic_interpolate_in_time(zooom_level, zoom, zooom_level, delta * camera_lerp, 0, 0, 1)


