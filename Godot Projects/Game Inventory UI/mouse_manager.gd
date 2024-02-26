extends Control

# Exposed variables
@export_subgroup("Pointer")
@export var cursor_image: Texture2D = null
@export var use_custom_size: bool = false
@export_range(5, 100) var custom_size: int = 30
@export_enum("Nearest:0","Bilinear:1","Cubic:2","Trilinear:3") var interpolation: int = 3
@export_subgroup("Pointer options")
#@export_range(0, 5, 0.001, "or_greater") var sensitivity: float = 1

const ERROR_INVALID_TEXTURE_SIZE = '[CURSOR_MANAGER]: Invalid image size. "image_size.x > 256 or image_size.y > 256."\nPlease enable custom size or scale down the image'
const MOUSE_MODE_HIDDEN = DisplayServer.MOUSE_MODE_HIDDEN
const MOUSE_MODE_VISIBLE = DisplayServer.MOUSE_MODE_VISIBLE

var drawn_texture: Texture2D = Texture2D.new()
var mouse_pos: Vector2 = Vector2.ZERO

func _ready():
	update_cursor()
	self.draw.connect(draw_cursor)

func _input(event):
	if event is InputEventMouseMotion:
		mouse_pos = get_global_mouse_position() - global_position
		self.queue_redraw()

func draw_cursor():
	self.draw_texture(drawn_texture, mouse_pos, Color(0, 0, 0))

func update_cursor():
	if cursor_image == null:
		if DisplayServer.mouse_get_mode() == MOUSE_MODE_HIDDEN:
			DisplayServer.mouse_set_mode(MOUSE_MODE_VISIBLE)
		return
	
	var texture_size = cursor_image.get_size()
	if !use_custom_size and (texture_size.x > 256 or texture_size.y > 256):
		printerr(ERROR_INVALID_TEXTURE_SIZE)
		return
		
	if DisplayServer.mouse_get_mode() != MOUSE_MODE_HIDDEN:
		DisplayServer.mouse_set_mode(MOUSE_MODE_HIDDEN)
	
	var texture = cursor_image
	if use_custom_size:
		texture = scale_texture(cursor_image, custom_size, interpolation)
	
	drawn_texture = texture

func scale_texture(texture: Texture2D, scale_height: int, interpolation: int):
	var texture_size = texture.get_size()
	var aspect_ratio = texture_size.x / texture_size.y
	var image = texture.get_image()
	image.resize(scale_height * aspect_ratio, scale_height, interpolation)
	return ImageTexture.create_from_image(image)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
