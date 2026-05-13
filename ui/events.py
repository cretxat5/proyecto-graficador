"""
Gestión centralizada de eventos del usuario en el lienzo.
"""
import pygame
from utils.constants import *

class EventHandler:
    """
    Clase para manejar interacciones de dibujo.
    """
    def __init__(self, application):
        self.app = application
        self.is_drawing = False
        self.points = []
        
    def handle_event(self, event: pygame.event.Event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            if event.pos[0] < UI_PANEL_WIDTH or event.pos[1] < TOP_BAR_HEIGHT:
                return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._on_mouse_down(event.pos)
            
        elif event.type == pygame.MOUSEMOTION:
            self._on_mouse_motion(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._on_mouse_up(event.pos)

    def _on_mouse_down(self, pos: tuple):
        x, y = pos
        x -= UI_PANEL_WIDTH
        y -= TOP_BAR_HEIGHT
        
        if self.app.active_tool == TOOL_POLYGON:
            self.points.append((x, y))
            self.app.draw_preview()
            
        elif self.app.active_tool == TOOL_BEZIER:
            if len(self.points) < 4:
                self.points.append((x, y))
                self.app.draw_preview()
                if len(self.points) == 4:
                    self.app.commit_shape(self.points)
                    self.points = []
                    
        elif self.app.active_tool == TOOL_TRIANGLE:
            if len(self.points) < 3:
                self.points.append((x, y))
                self.app.draw_preview()
                if len(self.points) == 3:
                    self.app.commit_shape(self.points)
                    self.points = []
                    
        else:
            self.is_drawing = True
            self.points = [(x, y), (x, y)]

    def _on_mouse_motion(self, pos: tuple):
        if self.is_drawing and len(self.points) >= 2:
            x, y = pos
            x -= UI_PANEL_WIDTH
            y -= TOP_BAR_HEIGHT
            self.points[-1] = (x, y)
            self.app.draw_preview()

    def _on_mouse_up(self, pos: tuple):
        if self.is_drawing and self.app.active_tool not in (TOOL_POLYGON, TOOL_BEZIER, TOOL_TRIANGLE):
            self.is_drawing = False
            x, y = pos
            x -= UI_PANEL_WIDTH
            y -= TOP_BAR_HEIGHT
            self.points[-1] = (x, y)
            self.app.commit_shape(self.points)
            self.points = []

    def commit_polygon(self):
        """Finaliza polígono."""
        if self.app.active_tool == TOOL_POLYGON and len(self.points) > 2:
            self.app.commit_shape(self.points)
            self.points = []
            
    def handle_keyboard(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.commit_polygon()
            if event.key == pygame.K_ESCAPE:
                self.points = []
                self.is_drawing = False
                self.app.draw_preview()
