extends CharacterBody2D
@export var selected = false
@export var collider: CollisionShape2D
@export var sprite: AnimatedSprite2D
#const SPEED = 300.0
#const JUMP_VELOCITY = -400.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
#var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _ready():
	get_node("AnimatedSprite2D").play("default")

