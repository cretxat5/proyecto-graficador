"""
Punto de entrada principal para la aplicación Graficador Interactivo 2D.
"""
import pygame
import sys
import math

from utils.constants import *
from utils.colors import *
from ui.interface import Interface
from ui.events import EventHandler

from algorithms.dda import draw_dda
from algorithms.bresenham import draw_bresenham_line
from algorithms.circle import draw_bresenham_circle
from algorithms.ellipse import draw_ellipse
from algorithms.polygon import draw_polygon, draw_rectangle, draw_triangle
from algorithms.bezier import draw_bezier_cubic

class Application:
    """
    Clase principal de la aplicación.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        self.canvas_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.canvas_surface.fill(WHITE)
        
        self.preview_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.preview_surface.set_colorkey((0, 255, 0)) # Transparente
        
        self.active_tool = TOOL_DDA
        self.active_color = BLACK
        
        self.ui = Interface(
            set_tool_callback=self.set_tool,
            clear_canvas_callback=self.clear_canvas,
            set_color_callback=self.set_color
        )
        
        self.event_handler = EventHandler(self)
        
    def set_tool(self, tool_name: str):
        self.active_tool = tool_name
        self.event_handler.points = []
        self.draw_preview()
        
    def set_color(self, color: tuple):
        self.active_color = color
        
    def clear_canvas(self):
        self.canvas_surface.fill(WHITE)
        self.draw_preview()
        
    def commit_shape(self, points: list):
        self._render_shape(self.canvas_surface, self.active_tool, points, self.active_color)
        self.preview_surface.fill((0, 255, 0))

    def draw_preview(self):
        self.preview_surface.fill((0, 255, 0))
        points = self.event_handler.points
        if not points:
            return
            
        if self.active_tool in (TOOL_POLYGON, TOOL_BEZIER, TOOL_TRIANGLE):
            for p in points:
                rect = pygame.Rect(p[0] - 2, p[1] - 2, 4, 4)
                self.preview_surface.fill(RED, rect)
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    draw_dda(self.preview_surface, points[i][0], points[i][1], points[i+1][0], points[i+1][1], GRAY)
        else:
            if len(points) >= 2:
                self._render_shape(self.preview_surface, self.active_tool, points, self.active_color)
                
    def _render_shape(self, surface: pygame.Surface, tool: str, points: list, color: tuple):
        if tool == TOOL_DDA:
            draw_dda(surface, points[0][0], points[0][1], points[-1][0], points[-1][1], color)
            
        elif tool == TOOL_BRESENHAM_LINE:
            draw_bresenham_line(surface, points[0][0], points[0][1], points[-1][0], points[-1][1], color)
            
        elif tool == TOOL_BRESENHAM_CIRCLE:
            dx = points[-1][0] - points[0][0]
            dy = points[-1][1] - points[0][1]
            r = int(math.sqrt(dx*dx + dy*dy))
            if r > 0:
                draw_bresenham_circle(surface, points[0][0], points[0][1], r, color)
                
        elif tool == TOOL_ELLIPSE:
            dx = abs(points[-1][0] - points[0][0])
            dy = abs(points[-1][1] - points[0][1])
            if dx > 0 and dy > 0:
                draw_ellipse(surface, points[0][0], points[0][1], dx, dy, color)
                
        elif tool == TOOL_RECTANGLE:
            draw_rectangle(surface, min(points[0][0], points[-1][0]), min(points[0][1], points[-1][1]), max(points[0][0], points[-1][0]), max(points[0][1], points[-1][1]), color)
            
        elif tool == TOOL_POLYGON:
            draw_polygon(surface, points, color)
            
        elif tool == TOOL_TRIANGLE:
            if len(points) == 3:
                draw_triangle(surface, points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], color)
                
        elif tool == TOOL_BEZIER:
            if len(points) == 4:
                draw_bezier_cubic(surface, points[0], points[1], points[2], points[3], color)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                self.ui.handle_event(event)
                self.event_handler.handle_event(event)
                self.event_handler.handle_keyboard(event)

            self.screen.fill((200, 200, 200))
            self.ui.draw(self.screen)
            self.screen.blit(self.canvas_surface, (UI_PANEL_WIDTH, 0))
            self.screen.blit(self.preview_surface, (UI_PANEL_WIDTH, 0))
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = Application()
    app.run()
