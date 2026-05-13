"""
Implementación del algoritmo de Bresenham para líneas.
"""
from utils.helpers import draw_pixel

def draw_bresenham_line(surface, x0: int, y0: int, x1: int, y1: int, color: tuple):
    """
    Dibuja una línea usando el algoritmo de Bresenham.
    Solo utiliza aritmética entera para mayor eficiencia.

    Args:
        surface: Superficie donde dibujar.
        x0: Coordenada x inicial.
        y0: Coordenada y inicial.
        x1: Coordenada x final.
        y1: Coordenada y final.
        color: Color de la línea.

    Returns:
        None
    """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x = x0
    y = y0

    while True:
        draw_pixel(surface, x, y, color)
        
        if x == x1 and y == y1:
            break
            
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
