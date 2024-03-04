extends CharacterBody2D
var SPEED = 100
@onready var sprite: 		AnimatedSprite2D = $AnimatedSprite2D;
var gravity = 		ProjectSettings.get_setting("physics/2d/default_gravity")
var should_move = 	false
var npc_path: 		Array[Vector2] = []
var path_index = 0;
var npc_direction: 	int = 0;

# Called when the node enters the scene tree for the first time.
func _physics_process(delta):
	velocity.y += gravity * delta
	if should_move:	
		if npc_direction == 1 and position.x <= npc_path[path_index].x:
			sprite.play("Walk")
			sprite.flip_h = false;
			
			#position.x = npc_direction * SPEED
			velocity.x = npc_direction * SPEED
		
		elif npc_direction == 1:
			velocity.x = 0
			sprite.play("Idle")
			
		if npc_direction == -1 and position.x >= npc_path[path_index].x:
			sprite.play("Walk")
			sprite.flip_h = true;
			velocity.x = npc_direction * SPEED
			
		elif npc_direction == -1: 
			sprite.play("Idle")
			velocity.x = 0;

			
	move_and_slide()
	
func _ready():
	var sprite = $AnimatedSprite2D;
	pass # Replace with function body.

 
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func move_to_target(positions: Array[Vector2]):
	should_move = true;
	print("hello")
	npc_path = positions;
	
	var direction = (positions[0] - self.position).normalized()
	
	if direction.x > 0:
		npc_direction = 1
	else:
		npc_direction = -1
	print(npc_direction)
