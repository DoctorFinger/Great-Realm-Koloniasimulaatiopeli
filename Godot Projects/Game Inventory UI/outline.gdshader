shader_type canvas_item;
render_mode unshaded;
 
uniform float line_thickness : hint_range(0.0, 16.0);
uniform vec4 line_color : source_color;
 
void fragment()
{
	if(line_thickness > 0.0){
		vec2 size = vec2(line_thickness) / vec2(textureSize(TEXTURE, 0));
	    vec4 sprite_color = texture(TEXTURE, UV);
	   
	    float alpha = sprite_color.a;
	    alpha += texture(TEXTURE, UV + vec2(0.0, -size.y)).a;
	    alpha += texture(TEXTURE, UV + vec2(size.x, -size.y)).a;
	    alpha += texture(TEXTURE, UV + vec2(size.x, 0.0)).a;
	    alpha += texture(TEXTURE, UV + vec2(size.x, size.y)).a;
	    alpha += texture(TEXTURE, UV + vec2(0.0, size.y)).a;
	    alpha += texture(TEXTURE, UV + vec2(-size.x, size.y)).a;
	    alpha += texture(TEXTURE, UV + vec2(-size.x, 0.0)).a;
	    alpha += texture(TEXTURE, UV + vec2(-size.x, -size.y)).a;
	   
	    vec3 final_color = mix(line_color.rgb, sprite_color.rgb, sprite_color.a);
	    COLOR = vec4(final_color, clamp(alpha, 0.0, 1.0));
	}
}


