"""
Implementación de algoritmos para polígonos, rectángulos y triángulos.
Se basan en Bresenham.
"""
from algorithms.bresenham import draw_bresenham_line

def draw_polygon(surface, points: list, color: tuple):
    """
    Dibuja un polígono cerrado dado una lista de vértices.

    Args:
        surface: Superficie donde dibujar.
        points: Lista de tuplas (x, y).
        color: Color del polígono.

    Returns:
        None
    """
    if not points or len(points) < 2:
        return
        
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        draw_bresenham_line(surface, p1[0], p1[1], p2[0], p2[1], color)

def draw_rectangle(surface, x0: int, y0: int, x1: int, y1: int, color: tuple):
    """
    Dibuja un rectángulo dadas dos esquinas opuestas.

    Args:
        surface: Superficie donde dibujar.
        x0, y0: Esquina inicial.
        x1, y1: Esquina final.
        color: Color.

    Returns:
        None
    """
    points = [
        (x0, y0),
        (x1, y0),
        (x1, y1),
        (x0, y1)
    ]
    draw_polygon(surface, points, color)

def draw_triangle(surface, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, color: tuple):
    """
    Dibuja un triángulo dados 3 vértices.

    Args:
        surface: Superficie.
        x0, y0: Vértice 1.
        x1, y1: Vértice 2.
        x2, y2: Vértice 3.
        color: Color.

    Returns:
        None
    """
    points = [
        (x0, y0),
        (x1, y1),
        (x2, y2)
    ]
    draw_polygon(surface, points, color)

def draw_hexagon(surface, cx: int, cy: int, r: int, color: tuple):
    """
    Dibuja un hexágono regular centrado en (cx, cy) con radio r.

    Args:
        surface: Superficie.
        cx, cy: Centro.
        r: Radio (distancia al vértice).
        color: Color.

    Returns:
        None
    """
    import math
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.radians(angle_deg)
        px = int(cx + r * math.cos(angle_rad))
        py = int(cy + r * math.sin(angle_rad))
        points.append((px, py))
    
    draw_polygon(surface, points, color)
