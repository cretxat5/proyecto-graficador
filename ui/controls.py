"""
Controles de la interfaz gráfica. Botones y paletas.
"""
import pygame
from utils.constants import *
from utils.colors import *

class Button:
    """
    Clase para representar un botón interactivo sin usar primitivas gráficas restrictivas.
    """
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font.Font, color: tuple, hover_color: tuple, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False
        
    def draw(self, surface: pygame.Surface):
        color = self.hover_color if self.is_hovered else self.color
        
        # Usamos fill() que opera sobre la memoria de superficie
        surface.fill(color, self.rect)
        
        # Bordes falsos (4 rectángulos finos en lugar de draw.rect)
        surface.fill(BLACK, (self.rect.x, self.rect.y, self.rect.width, 2))
        surface.fill(BLACK, (self.rect.x, self.rect.y + self.rect.height - 2, self.rect.width, 2))
        surface.fill(BLACK, (self.rect.x, self.rect.y, 2, self.rect.height))
        surface.fill(BLACK, (self.rect.x + self.rect.width - 2, self.rect.y, 2, self.rect.height))
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos: tuple):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                self.action()

class ColorPalette:
    """
    Paleta de colores para seleccionar el color activo.
    """
    def __init__(self, x: int, y: int, colors: list, action):
        self.x = x
        self.y = y
        self.colors = colors
        self.action = action
        self.size = 30
        self.padding = 5
        self.rects = []
        
        self._setup()
        
    def _setup(self):
        cols = 4
        for i, color in enumerate(self.colors):
            row = i // cols
            col = i % cols
            rect = pygame.Rect(
                self.x + col * (self.size + self.padding),
                self.y + row * (self.size + self.padding),
                self.size,
                self.size
            )
            self.rects.append((rect, color))
            
    def draw(self, surface: pygame.Surface, active_color: tuple):
        for rect, color in self.rects:
            surface.fill(color, rect)
            
            b_width = 3 if color == active_color else 1
            b_color = BLACK if color == active_color else GRAY
            
            surface.fill(b_color, (rect.x, rect.y, rect.width, b_width))
            surface.fill(b_color, (rect.x, rect.y + rect.height - b_width, rect.width, b_width))
            surface.fill(b_color, (rect.x, rect.y, b_width, rect.height))
            surface.fill(b_color, (rect.x + rect.width - b_width, rect.y, b_width, rect.height))
                
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, color in self.rects:
                if rect.collidepoint(event.pos):
                    self.action(color)
                    break
