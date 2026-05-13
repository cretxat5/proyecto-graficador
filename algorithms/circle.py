"""
Implementación del algoritmo de Bresenham para circunferencias.
"""
from utils.helpers import draw_pixel

def draw_bresenham_circle(surface, xc: int, yc: int, r: int, color: tuple):
    """
    Dibuja una circunferencia usando el algoritmo de Bresenham.
    Aprovecha la simetría de 8 octantes.

    Args:
        surface: Superficie donde dibujar.
        xc: Centro de la circunferencia en x.
        yc: Centro de la circunferencia en y.
        r: Radio de la circunferencia.
        color: Color de la circunferencia.

    Returns:
        None
    """
    x = 0
    y = r
    d = 3 - 2 * r

    _draw_circle_points(surface, xc, yc, x, y, color)

    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        
        _draw_circle_points(surface, xc, yc, x, y, color)

def _draw_circle_points(surface, xc: int, yc: int, x: int, y: int, color: tuple):
    """
    Dibuja los puntos simétricos en los 8 octantes.

    Args:
        surface: Superficie.
        xc, yc: Centro.
        x, y: Desplazamientos.
        color: Color.
    """
    draw_pixel(surface, xc + x, yc + y, color)
    draw_pixel(surface, xc - x, yc + y, color)
    draw_pixel(surface, xc + x, yc - y, color)
    draw_pixel(surface, xc - x, yc - y, color)
    draw_pixel(surface, xc + y, yc + x, color)
    draw_pixel(surface, xc - y, yc + x, color)
    draw_pixel(surface, xc + y, yc - x, color)
    draw_pixel(surface, xc - y, yc - x, color)
