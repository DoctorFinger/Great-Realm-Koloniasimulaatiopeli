extends Control

# Constants
@export var drag_outline_width := 1.5
@export var drag_outline_color := Color(0.5, 0, 0, 0.85)
@export var drag_fill_color := Color(0.5, 0, 0, 0.125)

# Dragging variables
var is_dragging := false
var drag_start := Vector2.ZERO
var drag_end := Vector2.ZERO
var drag_area := Rect2()

# Entity variables
var entities := []

# Scene related variables
var scene_tree: SceneTree = null;
var active_camera:Camera2D = null
var zoom_thickness:float = 0
var UI:CanvasLayer = null

func _ready():
	scene_tree = self.get_tree()
	active_camera = self.get_viewport().get_camera_2d()
	entities = scene_tree.get_nodes_in_group("entities")
	
	self.draw.connect(draw_selection_box)

func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.is_pressed():
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
		var entity_rect = entities[i].collider.get_shape().get_rect()
		entity_rect.position = entities[i].position - (entity_rect.size / 2)
		if drag_area.intersects(entity_rect):
			entities[i].selected = true

func remove_from_selection():
	for i in range(entities.size()):
		var entity_rect = entities[i].collider.get_shape().get_rect()
		entity_rect.position = entities[i].position - entity_rect.size / 2
		if drag_area.intersects(entity_rect):
			entities[i].selected = false

func default_selection():
	for i in range(entities.size()):
		entities[i].selected = false
		var entity_rect = entities[i].collider.get_shape().get_rect()
		entity_rect.position = entities[i].position - entity_rect.size / 2
		if !entities[i].selected:
			if drag_area.intersects(entity_rect):
				entities[i].selected = true
	
func draw_selection_box():
	if is_dragging:
		self.draw_rect(drag_area, drag_fill_color, true)
		self.draw_rect(drag_area, drag_outline_color, false, drag_outline_width * zoom_thickness)

func update_entity_outlines():
	for i in range(entities.size()):
		if entities[i].selected:
			entities[i].sprite.material.set_shader_parameter("line_thickness", 1.0)
		else:
			entities[i].sprite.material.set_shader_parameter("line_thickness", 0.0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	pass
