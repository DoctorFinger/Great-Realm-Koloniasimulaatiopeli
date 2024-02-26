extends Panel

@onready var item_sprite: Sprite2D = $CenterContainer/Panel/item

func update(item: InventoryItem):
	if !item:
		item_sprite.visible = false
	else:
		item_sprite.texture = item.texture;
		item_sprite.visible = true
		
