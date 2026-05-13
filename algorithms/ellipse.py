"""
Implementación de algoritmo para dibujar elipses usando punto medio.
"""
from utils.helpers import draw_pixel

def draw_ellipse(surface, xc: int, yc: int, rx: int, ry: int, color: tuple):
    """
    Dibuja una elipse utilizando el algoritmo de punto medio.

    Args:
        surface: Superficie donde dibujar.
        xc: Centro en x.
        yc: Centro en y.
        rx: Radio horizontal.
        ry: Radio vertical.
        color: Color de la elipse.

    Returns:
        None
    """
    # Región 1
    x = 0
    y = ry
    
    d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y
    
    while dx < dy:
        _draw_ellipse_points(surface, xc, yc, x, y, color)
        
        if d1 < 0:
            x += 1
            dx += 2 * ry * ry
            d1 += dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx += 2 * ry * ry
            dy -= 2 * rx * rx
            d1 += dx - dy + (ry * ry)
            
    # Región 2
    d2 = ((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry)
    
    while y >= 0:
        _draw_ellipse_points(surface, xc, yc, x, y, color)
        
        if d2 > 0:
            y -= 1
            dy -= 2 * rx * rx
            d2 += (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx += 2 * ry * ry
            dy -= 2 * rx * rx
            d2 += dx - dy + (rx * rx)

def _draw_ellipse_points(surface, xc: int, yc: int, x: int, y: int, color: tuple):
    """
    Dibuja los puntos simétricos en los 4 cuadrantes.
    """
    draw_pixel(surface, int(xc + x), int(yc + y), color)
    draw_pixel(surface, int(xc - x), int(yc + y), color)
    draw_pixel(surface, int(xc + x), int(yc - y), color)
    draw_pixel(surface, int(xc - x), int(yc - y), color)
