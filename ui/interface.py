"""
Gestión principal de la interfaz gráfica y el panel lateral.
"""
import pygame
from utils.constants import *
from utils.colors import *
from ui.controls import Button, ColorPalette
"""
Colores usados para la interfaz
"""
_PANEL_BG= ( 28,  28,  48)   # fondo del panel lateral
_PANEL_BORDER= ( 53,  53,  90)   # línea divisoria panel / lienzo
 
_TOPBAR_BG         = ( 37,  37,  64)   # fondo barra superior
_TOPBAR_BORDER     = ( 53,  53,  90)   # línea inferior de la barra
 
_BTN_NORMAL        = ( 37,  37,  64)   # botón herramienta normal
_BTN_HOVER         = ( 46,  46,  82)   # botón herramienta hover
_BTN_ACTIVE        = ( 45,  58, 106)   # botón herramienta activo
_BTN_TEXT          = (192, 192, 216)   # texto de botones normales
_BTN_ACTIVE_TEXT   = (144, 184, 248)   # texto del botón activo
 
_TOP_BTN_NORMAL    = ( 50,  50,  90)   # botón barra superior normal
_TOP_BTN_HOVER     = ( 61,  61, 110)   # botón barra superior hover
 
_BTN_DANGER        = ( 74,  37,  53)   # botón destructivo normal
_BTN_DANGER_HOVER  = (100,  45,  65)   # botón destructivo hover
_BTN_DANGER_TEXT   = (240, 128, 128)   # texto botón destructivo
 
_TITLE_COLOR       = (112, 112, 192)   # "Herramientas" y etiquetas
_STATUS_COLOR      = (100, 100, 160)   # texto de la barra de estado

class Interface:
    """
    Clase encargada de dibujar la interfaz, panel de herramientas y gestionar su estado.
    """
    def __init__(self, set_tool_callback, clear_canvas_callback, set_color_callback, 
                 undo_callback, open_callback, save_callback, manual_callback):
        self.font = pygame.font.SysFont("Arial", 16)
        self.title_font = pygame.font.SysFont("Arial", 20, bold=True)
        
        self.panel_rect = pygame.Rect(0, TOP_BAR_HEIGHT, UI_PANEL_WIDTH, WINDOW_HEIGHT - TOP_BAR_HEIGHT)
        self.top_bar_rect = pygame.Rect(0, 0, WINDOW_WIDTH, TOP_BAR_HEIGHT)
        
        self.active_tool = TOOLS[0]
        self.active_color = BLACK
        
        self.set_tool_callback = set_tool_callback
        self.clear_canvas_callback = clear_canvas_callback
        self.set_color_callback = set_color_callback
        self.undo_callback = undo_callback
        self.open_callback = open_callback
        self.save_callback = save_callback
        self.manual_callback = manual_callback
        
        self.buttons = []
        self.top_buttons = []
        self._setup_ui()
        
    def _setup_ui(self):
        y_offset = TOP_BAR_HEIGHT + 50
        
        for tool in TOOLS:
            btn = Button(
                x=20, 
                y=y_offset, 
                width=UI_PANEL_WIDTH - 40, 
                height=30, 
                text=tool, 
                font=self.font, 
                color=_BTN_NORMAL, 
                hover_color=_BTN_HOVER,
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
            color=_BTN_DANGER,
            hover_color=_BTN_DANGER_HOVER,
            action=self.clear_canvas_callback
        )
        self.buttons.append(btn_clear)
        
        # Botones de la barra superior
        top_btn_width = 120
        top_btn_height = 30
        x_offset = 10
        
        actions = [
            ("Deshacer",   self.undo_callback,         False),
            ("Limpiar",    self.clear_canvas_callback,  True),
            ("Abrir PNG",  self.open_callback,          False),
            ("Guardar PNG",self.save_callback,          False),
            ("Manual",     self.manual_callback,        False),
        ]
        
        for text, action, is_danger in actions:
            btn = Button(
                x=x_offset,
                y=(TOP_BAR_HEIGHT - top_btn_height) // 2,
                width=top_btn_width,
                height=top_btn_height,
                text=text,
                font=self.font,
                color=_BTN_DANGER      if is_danger else _TOP_BTN_NORMAL,
                hover_color=_BTN_DANGER_HOVER if is_danger else _TOP_BTN_HOVER,
                action=action
            )
            self.top_buttons.append(btn)
            x_offset += top_btn_width + 10
        
    def _change_tool(self, tool_name: str):
        self.active_tool = tool_name
        self.set_tool_callback(tool_name)
        
    def _change_color(self, color: tuple):
        self.active_color = color
        self.set_color_callback(color)
        
    def draw(self, surface: pygame.Surface):
        # Dibujar Panel Lateral
        surface.fill(_PANEL_BG, self.panel_rect)
        surface.fill(_PANEL_BORDER, (UI_PANEL_WIDTH - 2, TOP_BAR_HEIGHT, 2, WINDOW_HEIGHT - TOP_BAR_HEIGHT))
        
        # Dibujar Barra Superior
        surface.fill(_TOPBAR_BG, self.top_bar_rect)
        surface.fill(_TOPBAR_BORDER, (0, TOP_BAR_HEIGHT - 2, WINDOW_WIDTH, 2))
        
        title = self.title_font.render("Herramientas", True, _TITLE_COLOR)
        surface.blit(title, (20, TOP_BAR_HEIGHT + 15))
        
        for btn in self.buttons:
            if btn.text == self.active_tool:
                btn.color = _BTN_ACTIVE
            elif btn.text in TOOLS:
                btn.color = _BTN_NORMAL
 
            # Texto del botón activo en color diferenciado
            if btn.text == self.active_tool:
                original_render = btn.font.render
                text_color = _BTN_ACTIVE_TEXT
            elif btn.text == "Limpiar Lienzo":
                text_color = _BTN_DANGER_TEXT
            else:
                text_color = _BTN_TEXT
 
            # Dibujamos con el color de texto correcto sobrescribiendo temporalmente
            _draw_button_with_text_color(surface, btn, text_color)
            
        for btn in self.top_buttons:
            is_danger_btn = btn.color in (_BTN_DANGER, _BTN_DANGER_HOVER)
            text_color = _BTN_DANGER_TEXT if is_danger_btn else _BTN_TEXT
            _draw_button_with_text_color(surface, btn, text_color)
                
        color_title = self.font.render("Colores:", True, _TITLE_COLOR)
        surface.blit(color_title, (20, self.palette.y - 25))
        self.palette.draw(surface, self.active_color)
        
        status_y = WINDOW_HEIGHT - 60
        status_text = f"Herramienta: {self.active_tool}"
        status_surface = self.font.render(status_text, True, _STATUS_COLOR)
        surface.blit(status_surface, (10, status_y))
 
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            for btn in self.buttons + self.top_buttons:
                btn.check_hover(event.pos)
                
        for btn in self.buttons + self.top_buttons:
            btn.handle_event(event)
            
        self.palette.handle_event(event)
 
 
def _draw_button_with_text_color(surface: pygame.Surface, btn, text_color: tuple):
    """
    Dibuja el botón usando su lógica original pero con un color de texto específico.
    Reemplaza internamente el render del texto sin modificar la clase Button.
    """
    color = btn.hover_color if btn.is_hovered else btn.color
 
    surface.fill(color, btn.rect)
 
    # Bordes del botón
    surface.fill(_PANEL_BORDER, (btn.rect.x, btn.rect.y, btn.rect.width, 2))
    surface.fill(_PANEL_BORDER, (btn.rect.x, btn.rect.y + btn.rect.height - 2, btn.rect.width, 2))
    surface.fill(_PANEL_BORDER, (btn.rect.x, btn.rect.y, 2, btn.rect.height))
    surface.fill(_PANEL_BORDER, (btn.rect.x + btn.rect.width - 2, btn.rect.y, 2, btn.rect.height))
 
    text_surface = btn.font.render(btn.text, True, text_color)
    text_rect = text_surface.get_rect(center=btn.rect.center)
    surface.blit(text_surface, text_rect)
 