import pygame
from pygame import gfxdraw
from collections import namedtuple
import sys 

pygame.font.init() 


# Hyvin keskeneräinen kirjasto jota aloitin koodaamaan, nappien ja muiden komponenttien renderöintiin
# Tällä hetkellä vain renderöi nappeja, ja osittain kappaleita
# Yritin vähän matkia html css tyyliä rakentaa käyttöliittymiä


class Color:
    red     = 0
    green   = 0
    blue    = 0
    tuple   = (0, 0, 0)

    def __init__(self, red:int, green:int, blue:int):
        self.set_color(red, green, blue)
        
    def set_color(self, red:int, green:int, blue:int):
        self.red = red
        self.green = green
        self.blue = blue
        self.tuple = (red, green, blue)

class Path:
    target = ""
    extension = ""
    def __init__(self, target:str):
        self.extension = target[target.rfind('.') + 1:].strip().lower()
        self.target = target

class Size:
    x = 0
    y = 0
    def __init__(self, x:int | str , y:int | str):
        self.x = x
        self.y = y
    
class Pos:
    x = 0
    y = 0
    def __init__(self, x:int | str , y:int | str):
        self.x = x
        self.y = y

class Bbox:
    x = 0
    y = 0
    width = 0
    height = 0
    def __init__(self, x:int, y:int, width:int, height:int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Style:
    border_radius:          int                 = None
    border_color:           Color               = None
    border_width:           int                 = None
    background_color:       Color               = None
    background_image:       pygame.Surface      = None
    background_size:        Size                = None
    background_position:    Pos                 = None
    text_color:             Color               = None
    text_align_center:      bool                = None         
    font:                   pygame.font.Font    = None

    def __init__(
            self,
            border_width:           int                 =  0,
            border_radius:          int                 =  0,
            border_color:           Color               =  Color(0, 0, 0),
            background_color:       Color               =  Color(0, 0, 0),
            background_image:       Path                =  None,
            background_size:        Size                =  Size("100%", "100%"),
            background_position:    Pos                 =  Pos(0, 0),
            text_color:             Color               =  Color(255, 255, 255),
            font:                   pygame.font.Font    =  None,
            text_align_center:      bool                =  True  
        ):

        self.border_radius          = border_radius
        self.border_color           = border_color
        self.border_width           = border_width
        self.background_color       = background_color
        self.background_image       = background_image
        self.background_size        = background_size
        self.background_position    = background_position
        self.text_color             = text_color
        self.text_align_center      = text_align_center
        
        if background_image:
            if(background_image.extension == "png"):
                self.background_image = pygame.image.load(background_image.target).convert_alpha()
            else:
                self.background_image = pygame.image.load(background_image.target).convert()

        if font is None:
            self.font = pygame.font.Font(None, 32)

        else: 
            self.font = font
            
def draw_rounded_rect(surface, bbox:Bbox, color:Color, border_radius:int):
    if color:
        _color = (color.red, color.green, color.blue)
        border_radius = int(min(border_radius, bbox.width // 2 - 1, bbox.height // 2 - 1))
        gfxdraw.aacircle(surface, bbox.x + border_radius, bbox.y + border_radius, border_radius, _color)
        gfxdraw.aacircle(surface, bbox.x + bbox.width - border_radius - 1, bbox.y + border_radius, border_radius, _color)
        gfxdraw.aacircle(surface, bbox.x + border_radius, bbox.y + bbox.height - border_radius - 1, border_radius, _color)
        gfxdraw.aacircle(surface, bbox.x + bbox.width - border_radius - 1,    bbox.y + bbox.height - border_radius - 1, border_radius, _color)
        gfxdraw.filled_circle(surface, bbox.x + border_radius, bbox.y + border_radius, border_radius, _color)
        gfxdraw.filled_circle(surface, bbox.x + bbox.width - border_radius - 1, bbox.y + border_radius, border_radius, _color)
        gfxdraw.filled_circle(surface, bbox.x + border_radius, bbox.y + bbox.height - border_radius - 1, border_radius, _color)
        gfxdraw.filled_circle(surface, bbox.x + bbox.width - border_radius - 1, bbox.y + bbox.height - border_radius - 1, border_radius, _color)

        rect_tmp = pygame.Rect(bbox.x + border_radius, bbox.y, bbox.width - 2 * border_radius, bbox.height)
        pygame.draw.rect(surface, _color, rect_tmp)
        rect_tmp = pygame.Rect(bbox.x, bbox.y + border_radius, bbox.width, bbox.height - 2 * border_radius)
        pygame.draw.rect(surface, _color, rect_tmp)

# Pohja luokka jonka jokainen elementti jakaa
class Element:
    style:                  Style       = None
    position:               Pos         = None
    size:                   Size        = None
    bbox:                   int         = Bbox(0, 0, 0, 0)
    callback:               object      = None
    state:                  list        = (0, 0)
    hover_style:            Style       = None

    # Alusta muuttujat ja aseta sijainti ja koko
    def __init__(
            self, 
            position:       Pos     = Pos(0, 0), 
            size:           Size    = Size(50, 100), 
            style:          Style   = Style(),
            hover_style:    Style   = None
        ):
        
        self.__pos:                   Pos        = Pos(0, 0)
        self.__size:                  Size       = Size(0, 0)
        self.__is_position_relative:  list       = [0, 0]
        self.__is_size_relative:      list       = [0, 0]

        self.set_position(position)
        self.set_size(size)
        self.style = style
        self.hover_style = hover_style

    # Funktio palauttaa sijainnin x- ja y-koordinaatit
    def get_position(self):
        return self.position.x, self.position.y
    
    # Funktio palauttaa koon leveys ja korkeus
    def get_size(self):
        return self.size.x, self.size.y

    # Funktio asettaa teksti
    def set_text(self, text:str):
        self.text = text
    
    # Funktio aseta elementin koon, tukee absoluuttisia ja suhteellisia yksiköitä
    def set_size(self, size: Size = Size(0, 0)):
        if isinstance(size.x, str):
            width = size.x.strip()
            if width.endswith("%"):
                self.__is_size_relative[0] = 1
                self.__size.x = float(width[:-1]) / 100
            else:
                self.__is_size_relative[0] = 0
                self.__size.x = int(width)
        else:
            self.__is_size_relative[0] = 0
            self.__size.x = int(size.x)

        if isinstance(size.y, str):
            height = size.y.strip()
            if height.endswith("%"):
                self.__is_size_relative[1] = 1
                self.__size.y = float(height[:-1]) / 100
            else:
                self.__is_size_relative[1] = 0
                self.__size.y = int(height)
        else:
            self.__is_size_relative[1] = 0
            self.__size.y = int(size.y)

        self.size = size;
    
     # Aseta sijainti, tukee absoluuttisia ja suhteellisia yksiköitä
    def set_position(self, position: Pos = Size(0, 0)):
        if isinstance(position.x, str) and position.x.endswith("%"):
            self.__is_position_relative[0] = 1
            self.__pos.x = float((position.x.strip())[:-1]) / 100
        else:
            self.__is_position_relative[0] = 0
            self.__pos.x = int(position.x)

        if isinstance(position.y, str) and position.y.endswith("%"):
            self.__is_position_relative[1] = 1
            self.__pos.y = float((position.y.strip())[:-1]) / 100
        else:
            self.__is_position_relative[1] = 0
            self.__pos.y = int(position.y)

        self.position = position;
    
    # Hae rajoittava neliö
    def get_bbox(self, screen: pygame.Surface):
        bbox: Bbox = Bbox(
            self.__pos.x, 
            self.__pos.y,
            self.__size.x,
            self.__size.y
        )

        screen_width = screen.get_width();

        if(self.__is_size_relative[0]):
            bbox.width = int(bbox.width * screen_width)
        if(self.__is_size_relative[1]):
            bbox.height = int(bbox.height * screen_width)

        if self.__is_position_relative[0]:
            bbox.x = int((screen_width - bbox.width) * bbox.x)
        if self.__is_position_relative[1]:
            bbox.y = int((screen_width - bbox.height) * bbox.y)
        
        return bbox;

# Nappi elementti
class Button(Element):
    text: str = None
    def __init__(
            self,
            text:           str = "",
            position:       Pos     = Pos(0, 0), 
            size:           Size    = Size(50, 100), 
            style:          Style   = Style(),
            hover_style:    Style   = None,
        ):
        super().__init__(position, size, style, hover_style) 
        self.text = text
        
    # Funktio piirtää napin
    def draw(self, screen: pygame.Surface):
        self.bbox = self.get_bbox(screen)

        render_style:Style = self.style;
        if self.hover_style and self.is_mouse_over():
            render_style = self.hover_style

        draw_rounded_rect(screen, self.bbox, render_style.background_color, render_style.border_radius)

        if self.style.font != None:
            text_surface = self.style.font.render(self.text, True, (render_style.text_color.red, render_style.text_color.green, render_style.text_color.blue))
            text_rect = text_surface.get_rect(center=(self.bbox.x + self.bbox.width / 2, self.bbox.y + self.bbox.height / 2))
            screen.blit(text_surface, text_rect)

    # Funktio määrittää onko hiiri napin päällä
    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return  self.bbox.x <= mouse_x <= self.bbox.x + self.bbox.width and self.bbox.y <= mouse_y <= self.bbox.y + self.bbox.height
    
    # Funktio määrittää klikkasiko käyttäjä nappia
    def is_pressed(self):
        if pygame.mouse.get_pressed()[0]:
            return self.is_mouse_over()
        
        return False
    
# Keskeneräinen luokka, olisin käyttänyt help menun renderöintiin
class Paragraph(Element):
    text: str = None
    def __init__(
            self,
            text:           str = "",
            position:       Pos     = Pos(0, 0), 
            size:           Size    = Size(50, 100), 
            style:          Style   = Style(),
            hover_style:    Style   = None,
        ):
        super().__init__(position, size, style, hover_style) 
        self.text = text
        
    # sori en jaksanut kommentoida
    def draw(self, screen: pygame.Surface):
        words = self.text.split()
        space = self.style.font.size(' ')[0] 

        max_width, max_height = self.size.x, self.size.y 
        render_surface = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
        
        render_style:Style = self.style;
        if self.hover_style and self.is_mouse_over():
            render_style = self.hover_style

        x, y = 0, 0  
        setence_width = 0;

        for word in words:

            if(word == '\\n'): # Eipä toimi
                print("123")
                x = 0  
                y += word_height
            else:
                word_surface = self.style.font.render(word, True, render_style.text_color.tuple)
                word_width, word_height = word_surface.get_size()

                if x + word_width >= max_width:
                    if x > setence_width:
                        setence_width = x;
                    x = 0  
                    y += word_height  

                if y + word_height >= max_height:
                    break 

                render_surface.blit(word_surface, (x, y)) 
                x += word_width + space  


        offset_x = self.position.x
        if self.style.text_align_center:
            offset_x += ((max_width - setence_width) / 2)

        self.bbox = Bbox(self.position.x, self.position.y, max_width, max_height)
        draw_rounded_rect(screen, Bbox(self.position.x, self.position.y, max_width, max_height), render_style.background_color, render_style.border_radius)
        screen.blit(render_surface, (offset_x, self.position.y))



    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return  self.bbox.x <= mouse_x <= self.bbox.x + self.bbox.width and self.bbox.y <= mouse_y <= self.bbox.y + self.bbox.height
    
    def is_pressed(self):
        if pygame.mouse.get_pressed()[0]:
            return self.is_mouse_over()
        
        return False
        
