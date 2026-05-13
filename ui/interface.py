"""
Gestión principal de la interfaz gráfica y el panel lateral.
"""
import pygame
from utils.constants import *
from utils.colors import *
from ui.controls import Button, ColorPalette

class Interface:
    """
    Clase encargada de dibujar la interfaz, panel de herramientas y gestionar su estado.
    """
    def __init__(self, set_tool_callback, clear_canvas_callback, set_color_callback):
        self.font = pygame.font.SysFont("Arial", 16)
        self.title_font = pygame.font.SysFont("Arial", 20, bold=True)
        
        self.panel_rect = pygame.Rect(0, 0, UI_PANEL_WIDTH, WINDOW_HEIGHT)
        
        self.active_tool = TOOLS[0]
        self.active_color = BLACK
        
        self.set_tool_callback = set_tool_callback
        self.clear_canvas_callback = clear_canvas_callback
        self.set_color_callback = set_color_callback
        
        self.buttons = []
        self._setup_ui()
        
    def _setup_ui(self):
        y_offset = 50
        
        for tool in TOOLS:
            btn = Button(
                x=20, 
                y=y_offset, 
                width=UI_PANEL_WIDTH - 40, 
                height=30, 
                text=tool, 
                font=self.font, 
                color=LIGHT_GRAY, 
                hover_color=GRAY,
                action=lambda t=tool: self._change_tool(t)
            )
            self.buttons.append(btn)
            y_offset += 40
            
        y_offset += 20
        
        colors = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, GRAY]
        self.palette = ColorPalette(20, y_offset, colors, self._change_color)
        
        y_offset += 100
        
        btn_clear = Button(
            x=20,
            y=y_offset,
            width=UI_PANEL_WIDTH - 40,
            height=40,
            text="Limpiar Lienzo",
            font=self.font,
            color=(255, 100, 100),
            hover_color=(200, 50, 50),
            action=self.clear_canvas_callback
        )
        self.buttons.append(btn_clear)
        
    def _change_tool(self, tool_name: str):
        self.active_tool = tool_name
        self.set_tool_callback(tool_name)
        
    def _change_color(self, color: tuple):
        self.active_color = color
        self.set_color_callback(color)
        
    def draw(self, surface: pygame.Surface):
        surface.fill((230, 230, 230), self.panel_rect)
        surface.fill(BLACK, (UI_PANEL_WIDTH - 2, 0, 2, WINDOW_HEIGHT))
        
        title = self.title_font.render("Herramientas", True, BLACK)
        surface.blit(title, (20, 15))
        
        for btn in self.buttons:
            if btn.text == self.active_tool:
                btn.color = (150, 200, 150)
            elif btn.text in TOOLS:
                btn.color = LIGHT_GRAY
                
            btn.draw(surface)
            
        color_title = self.font.render("Colores:", True, BLACK)
        surface.blit(color_title, (20, self.palette.y - 25))
        self.palette.draw(surface, self.active_color)
        
        status_y = WINDOW_HEIGHT - 60
        status_text = f"Herramienta: {self.active_tool}"
        status_surface = self.font.render(status_text, True, DARK_GRAY)
        surface.blit(status_surface, (10, status_y))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            for btn in self.buttons:
                btn.check_hover(event.pos)
                
        for btn in self.buttons:
            btn.handle_event(event)
            
        self.palette.handle_event(event)
