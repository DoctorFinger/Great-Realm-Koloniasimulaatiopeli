extends Control

# Constants
const DRAG_OUTLINE_WIDTH := 1.5
const DRAG_OUTLINE_COLOR := Color(0.5, 0, 0, 0.85)
const DRAG_FILL_COLOR := Color(0.5, 0, 0, 0.125)

# Dragging variables
var is_dragging := false
var drag_start := Vector2.ZERO
var drag_end := Vector2.ZERO
var drag_area := Rect2()

# Entity variables
var entities := []
var entity_sprites := []
var entity_colliders := []
var selected_entities := []

# Scene related variables
var scene_tree
var active_camera
var zoom_thickness

func _ready():
	scene_tree = self.get_tree()
	active_camera = self.get_viewport().get_camera_2d()
	entities = scene_tree.get_nodes_in_group("entities")
	entity_sprites = scene_tree.get_nodes_in_group("entity_sprites")
	entity_colliders = scene_tree.get_nodes_in_group("entity_colliders")
	selected_entities.resize(entities.size())
	selected_entities.fill(false)
	self.draw.connect(draw_selection_box)

func _unhandled_input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				start_drag()
			elif is_dragging:
				end_drag()
	elif event is InputEventMouseMotion:
		if is_dragging:
			update_drag()

func start_drag():
	drag_start = self.get_global_mouse_position()
	is_dragging = true
	update_drag()

func end_drag():
	is_dragging = false
	update_drag()

func update_drag():
	update_drag_area()
	handle_selection()
	update_entity_outlines()
	self.queue_redraw()

func update_drag_area():
	zoom_thickness = 1.0 / max(active_camera.zoom.x, active_camera.zoom.y)
	drag_end = self.get_global_mouse_position() - drag_start
	drag_area = Rect2(drag_start, drag_end).abs()

func handle_selection():
	var add_key_pressed = Input.is_key_pressed(KEY_SHIFT)
	var remove_key_pressed = Input.is_key_pressed(KEY_CTRL)
	
	if add_key_pressed:
		add_to_selection()
	elif remove_key_pressed:
		remove_from_selection()
	else:
		default_selection()


func add_to_selection():
	for i in range(entities.size()):
		var entity_rect = entity_colliders[i].get_shape().get_rect()
		entity_rect.position = entities[i].position - entity_rect.size / 2
		var is_intersecting = drag_area.intersects(entity_rect)
		if is_intersecting:
			selected_entities[i] = true

func remove_from_selection():
	for i in range(entities.size()):
		var entity_rect = entity_colliders[i].get_shape().get_rect()
		entity_rect.position = entities[i].position - entity_rect.size / 2
		var is_intersecting = drag_area.intersects(entity_rect)
		if is_intersecting:
			selected_entities[i] = false

func default_selection():
	selected_entities.fill(false)
	for i in range(entities.size()):
		var entity_rect = entity_colliders[i].get_shape().get_rect()
		entity_rect.position = entities[i].position - entity_rect.size / 2
		var is_selected = selected_entities[i]
		var is_intersecting = drag_area.intersects(entity_rect)
		if !is_selected:
			if is_intersecting:
				selected_entities[i] = true
		else:
			selected_entities[i] = false

func draw_selection_box():
	if is_dragging:
		self.draw_rect(drag_area, DRAG_FILL_COLOR, true)
		self.draw_rect(drag_area, DRAG_OUTLINE_COLOR, false, DRAG_OUTLINE_WIDTH * zoom_thickness)

func update_entity_outlines():
	for i in range(selected_entities.size()):
		if selected_entities[i]:
			entity_sprites[i].material.set_shader_parameter("line_thickness", 1.0)
		else:
			entity_sprites[i].material.set_shader_parameter("line_thickness", 0.0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
