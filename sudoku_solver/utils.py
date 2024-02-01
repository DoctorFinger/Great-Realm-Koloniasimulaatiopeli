import pygame
import os

def load_sound(path_to_sound: str = ""):
    sound = pygame.mixer.Sound(os.path.join(path_to_sound))
    return sound;

def load_image(path_to_image: str = "", width: int = None, height: int = None, has_alpha: bool = False):
    # Lataa kuva annetusta polusta
    image = pygame.image.load(os.path.join(path_to_image))
    
    # Jos kuvalla on läpinäkyvyyttä, muunna se
    if has_alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()

    # Skalaa kuva annettuihin mittoihin, jos mitat annettu
    if width and height:
        image = pygame.transform.scale(image, (width, height))
        
    return image
