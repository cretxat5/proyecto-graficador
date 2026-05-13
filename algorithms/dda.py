"""
Implementación del algoritmo DDA para líneas.
"""
from utils.helpers import draw_pixel

def draw_dda(surface, x0: int, y0: int, x1: int, y1: int, color: tuple):
    """
    Dibuja una línea usando el algoritmo DDA.
    Calcula incrementos basados en la mayor diferencia.

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
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        draw_pixel(surface, x0, y0, color)
        return

    x_inc = dx / float(steps)
    y_inc = dy / float(steps)

    x = float(x0)
    y = float(y0)

    for _ in range(int(steps) + 1):
        draw_pixel(surface, round(x), round(y), color)
        x += x_inc
        y += y_inc
