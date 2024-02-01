import pygame
from pygame import gfxdraw
import sys 
import copy
import functools
pygame.font.init() 


# Hyvin keskeneräinen kirjasto jota aloitin koodaamaan, nappien ja muiden komponenttien renderöintiin
# Tällä hetkellä vain renderöi nappeja, ja osittain kappaleita
# Yritin vähän matkia html css tyyliä rakentaa käyttöliittymiä
CHECKBOX_RECT = pygame.Rect(100, 100, 30, 30)


class Color:
    red     = 0
    green   = 0
    blue    = 0
    alpha   = 255
    rgb   = ( 0, 0, 0 )
    rgba  = ( 0, 0, 0, 255 )

    def __init__(self, red:int, green:int, blue:int, opacity: int = 255):
        self.set_color(red, green, blue, opacity)
        
    def set_color(self, red:int, green:int, blue:int, opacity:int = 255):
        self.red = red
        self.green = green
        self.blue = blue
        self.opacity = opacity
        self.rgb = ( red, green, blue )
        self.rgba = (red, green, blue, opacity)

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
    background_color:       Color               = None
    background_image:       pygame.Surface      = None
    # background_size:        Size                = None
    # background_position:    Pos                 = None
    text_color:             Color               = None
    text_align_center:      bool                = None         
    font:                   pygame.font.Font    = None
    opacity:                float               = None
    padding:                int                 = None

    def __init__(
            self,
            border_radius:          int                 =  0,
            background_color:       Color               =  Color(0, 0, 0),
            background_image:       pygame.Surface      =  None,
            # background_size:        Size                =  Size("100%", "100%"),
            # background_position:    Pos                 =  Pos(0, 0),
            text_color:             Color               =  Color(255, 255, 255),
            font:                   pygame.font.Font    =  None,
            text_align_center:      bool                =  True,
            opacity:                float               =  1,
            padding:                int                 =  0
        ):

        self.border_radius          = border_radius
        self.background_color       = background_color
        self.background_image       = background_image
        # self.background_size        = background_size
        # self.background_position    = background_position
        self.text_color             = text_color
        self.text_align_center      = text_align_center
        self.background_image       = background_image;
        self.opacity                = opacity
        self.padding                = padding

        if font is None:
            self.font = pygame.font.Font(None, 32)

        else: 
            self.font = font

# Piirtää pyöristetyn neliön reunojen pehmennyksellä
@functools.lru_cache()     
def draw_rounded_rect(bbox:Bbox, color:Color, border_radius:int) -> pygame.Surface | None:
    if color and color.opacity:
        surface = pygame.Surface((bbox.width, bbox.height), flags = pygame.SRCALPHA )
        border_radius = int(min(border_radius, bbox.width // 2 - 1, bbox.height // 2 - 1))
        
        gfxdraw.aacircle(surface, border_radius, border_radius, border_radius, color.rgb)
        gfxdraw.aacircle(surface, bbox.width - border_radius - 1, border_radius, border_radius, color.rgb)
        gfxdraw.aacircle(surface, border_radius, bbox.height - border_radius - 1, border_radius, color.rgb)
        gfxdraw.aacircle(surface, bbox.width - border_radius - 1, bbox.height - border_radius - 1, border_radius, color.rgb)
        gfxdraw.filled_circle(surface, border_radius, border_radius, border_radius, color.rgb)
        gfxdraw.filled_circle(surface, bbox.width - border_radius - 1, border_radius, border_radius, color.rgb)
        gfxdraw.filled_circle(surface, border_radius, bbox.height - border_radius - 1, border_radius, color.rgb)
        gfxdraw.filled_circle(surface, bbox.width - border_radius - 1, bbox.height - border_radius - 1, border_radius, color.rgb)
        
        rect_tmp = pygame.Rect(border_radius, 0, bbox.width - 2 * border_radius, bbox.height)
        pygame.draw.rect(surface, color.rgb, rect_tmp)
        rect_tmp = pygame.Rect(0, border_radius, bbox.width, bbox.height - 2 * border_radius)
        pygame.draw.rect(surface, color.rgb, rect_tmp)
        return surface

# Piirtää valinta ruudun
@functools.lru_cache()   
def draw_checkbox(box_size, color, outline):
    surface = pygame.Surface((box_size, box_size), pygame.SRCALPHA)
    pygame.draw.rect(surface, color.rgb, (0, 0, box_size, box_size)) 
    pygame.draw.rect(surface, (255,255, 255), (0, 0, box_size, box_size), outline) 
    return surface
    
# Piirtää valinta ruudun valinnan kuvakkeen
@functools.lru_cache()   
def draw_check_sign(check_size, color, thickness):
    if color and color.opacity:
        surface = pygame.Surface((check_size, check_size), pygame.SRCALPHA)
        pygame.draw.line(surface, color.rgb, (0.2 * check_size, 0.5 * check_size), (0.45 * check_size, 0.75 * check_size), thickness)
        pygame.draw.line(surface, color.rgb, (0.45 * check_size, 0.75 * check_size), (0.8 * check_size, 0.3 * check_size), thickness)
        return surface

# Piirtää tekstin
@functools.lru_cache()
def draw_text(font:pygame.font.Font, text:str, color:Color) -> pygame.Surface:
    text = font.render(text, True, color.rgb)
    return text

# Piirtää monirivisen tekstin
@functools.lru_cache()
def draw_multiline_text(screen, bbox: Bbox, text:str, color:Color, font: pygame.font.Font, text_align_center: bool):
        # ei pysty renderöimään uusia rivejä linebreakin avulla,
        # sanojen välejä ei pysty muuttaa
        # padding ei toimi
        words = text.split()
        space = font.size(' ')[0] 

        max_width, max_height = bbox.width, bbox.height  # Change here
        render_surface = pygame.Surface((max_width, max_height), pygame.SRCALPHA) #pygame.SRCALPHA)

        x, y = 0, 0  
        word_width, word_height = 0, 0
        sentence_width = 0;

        for word in words:
                word_surface = font.render(word, True, color.rgb)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    if x > sentence_width:
                        sentence_width = x;
                    x = 0  
                    y += word_height  

                if y + word_height >= max_height:
                    break 

                render_surface.blit(word_surface, (x, y)) 
                x += word_width + space  

        offset_x = bbox.x 
        offset_y = bbox.y 

        if x > sentence_width:
            sentence_width = x;
        
        if y < word_height:
            y = word_height
        else:
            y += word_height

        if text_align_center:
            offset_x += ((max_width - sentence_width ) // 2)
            offset_y += ((max_height - y) // 2)
        
        return offset_x, offset_y, render_surface


@functools.lru_cache()
def scale_image(image:pygame.Surface, width:int, height:int) -> pygame.Surface:
    image = pygame.transform.scale(image, ( width, height ))
    return image

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
    
    # Funktio asettaa koon, tukee absoluuttisia ja suhteellisia yksiköitä
    @functools.lru_cache()
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
    
     # Asettaa sijainnin, tukee absoluuttisia ja suhteellisia yksiköitä
    @functools.lru_cache()
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
    
    # Hakee rajoittavan neliön
    @functools.lru_cache()
    def get_bbox(self, screen: pygame.Surface):
        bbox =  Bbox(
            self.__pos.x, 
            self.__pos.y,
            self.__size.x,
            self.__size.y
        )

        screen_width = screen.get_width();
        screen_height = screen.get_height( );

        if(self.__is_size_relative[0]):
            bbox.width = int(bbox.width * screen_width)
        if(self.__is_size_relative[1]):
            bbox.height = int(bbox.height * screen_height)

        if self.__is_position_relative[0]:
            bbox.x = int((screen_width - bbox.width) * bbox.x)
        if self.__is_position_relative[1]:
            bbox.y = int((screen_height - bbox.height) * bbox.y)
        
        return bbox;

# Ei toimi vielä
class Checkbox(Element):
    state = None

    def __init__(
            self,
            state:          bool    = False,
            position:       Pos     = Pos(0, 0), 
            size:           Size    = Size(50, 100), 
            style:          Style   = Style(),
            hover_style:    Style   = None,
        ):
        super().__init__(position, size, style, hover_style);
        self.state = state;
    
    # Palauttaa valintaruudun valintatilan
    def get_state(self):
        return self.state;

    # Funktio määrittää onko hiiri calintaruudun päällä
    def is_mouse_over(self):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            return  self.bbox.x <= mouse_x <= self.bbox.x + self.bbox.width and self.bbox.y <= mouse_y <= self.bbox.y + self.bbox.height
    
    # Vaihtaa valintaruudun valintatila
    def toggle_check_state(self):
        self.state = not self.state;

    # Funktio määrittää klikkasiko käyttäjä valintaruutua
    def is_pressed(self):
            if pygame.mouse.get_pressed()[0]:
                return self.is_mouse_over()

            return False

    # Piirtää valintaruudun
    def draw(self, screen: pygame.Surface):
        self.bbox = self.get_bbox(screen)
        render_style:Style = self.style;  

        if self.hover_style and self.is_mouse_over():
            render_style = self.hover_style
    
        if render_style.background_color and render_style.opacity:
            checkbox_size = min(self.bbox.width, self.bbox.height)
            checkbox_outline = max(1, checkbox_size // 12);
            checksign_thickness = max(1, checkbox_size // 8)
            checksign_size = checkbox_size - checkbox_outline;

            checkbox = draw_checkbox(checkbox_size, Color(255, 0, 0), checkbox_outline)
            check_sign = draw_check_sign(checksign_size, Color(255, 255, 255), checksign_thickness);
            screen.blit(checkbox, (self.bbox.x, self.bbox.y))
            screen.blit(check_sign, (self.bbox.x + checkbox_outline // 2, self.bbox.y + checkbox_outline // 2))
         
        if self.is_pressed():
            self.toggle_check_state()
        

            
        
        
# Nappi elementti
class Button(Element):
    text:           str = None
    press_sound:    pygame.mixer.Sound = None

    def __init__(
            self,
            text:           str = "",
            position:       Pos     = Pos(0, 0), 
            size:           Size    = Size(50, 100), 
            style:          Style   = Style(),
            hover_style:    Style   = None,
            press_sound:    pygame.mixer.Sound = None
        ):
        super().__init__(position, size, style, hover_style);
        self.text = text
        self. press_sound = press_sound


    # Funktio piirtää napin
    def draw(self, screen: pygame.Surface):
        self.bbox = self.get_bbox(screen)
        

        render_style:Style = self.style;     
        if self.hover_style and self.is_mouse_over():
            render_style = self.hover_style
      
        if render_style.background_image and render_style.opacity:
            button_surface = scale_image( render_style.background_image, self.bbox.width, self.bbox.height )
            if render_style.opacity < 1:
                button_surface.set_alpha( 255 * render_style.opacity)

            screen.blit(button_surface, (self.bbox.x, self.bbox.y))

        elif render_style.background_color and render_style.opacity and render_style.background_color.opacity:
            button_surface = draw_rounded_rect(self.bbox, render_style.background_color, render_style.border_radius)
            if render_style.background_color.opacity < 255 or render_style.opacity < 1:
                final_opacity = render_style.background_color.opacity - render_style.background_color.opacity * (1 - render_style.opacity)
                button_surface.set_alpha(final_opacity)

            screen.blit(button_surface, (self.bbox.x, self.bbox.y))
        
        if self.style.font and render_style.opacity and render_style.text_color.opacity:
            text_surface = draw_text(self.style.font, self.text, render_style.text_color)        
            if render_style.text_color.opacity < 255 or render_style.opacity < 1:
                final_opacity = render_style.text_color.opacity - render_style.text_color.opacity * (1 - render_style.opacity)
                text_surface.set_alpha(final_opacity)

            text_rect = text_surface.get_rect(center=(self.bbox.x + self.bbox.width / 2, self.bbox.y + self.bbox.height / 2))
            screen.blit(text_surface, text_rect)


    # Funktio määrittää onko hiiri napin päällä
    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return  self.bbox.x <= mouse_x <= self.bbox.x + self.bbox.width and self.bbox.y <= mouse_y <= self.bbox.y + self.bbox.height
    
    # Funktio määrittää klikkasiko käyttäjä nappia
    def is_pressed(self):
        if pygame.mouse.get_pressed()[0]:
            if self.is_mouse_over():
                if self.press_sound:
                    self.press_sound.play();
                return True
            else:
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
        bbox = self.get_bbox(screen)

        render_style:Style = self.style;
        if self.hover_style and self.is_mouse_over():
            render_style = self.hover_style

        
        offset_x, offset_y, surface = draw_multiline_text(screen, bbox, self.text, render_style.text_color, render_style.font, render_style.text_align_center);
                
        if render_style.background_color and render_style.background_color.opacity and render_style.opacity:
            button_surface = draw_rounded_rect(bbox, render_style.background_color, render_style.border_radius)  # Adjusted here
            screen.blit(button_surface, (bbox.x, bbox.y))  # Adjusted here
        

        screen.blit(surface, (offset_x, offset_y))  

    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return  self.bbox.x <= mouse_x <= self.bbox.x + self.bbox.width and self.bbox.y <= mouse_y <= self.bbox.y + self.bbox.height
    
    def is_pressed(self):
        if pygame.mouse.get_pressed()[0]:
            return self.is_mouse_over()
        
        return False
        
