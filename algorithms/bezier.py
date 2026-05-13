"""
Implementación de algoritmo para dibujar curvas Bézier cúbicas.
"""
from utils.helpers import draw_pixel
from algorithms.bresenham import draw_bresenham_line

def draw_bezier_cubic(surface, p0: tuple, p1: tuple, p2: tuple, p3: tuple, color: tuple, segments: int = 100):
    """
    Dibuja una curva de Bézier cúbica utilizando interpolación matemática manual.

    Args:
        surface: Superficie donde dibujar.
        p0: Punto inicial.
        p1: Punto de control 1.
        p2: Punto de control 2.
        p3: Punto final.
        color: Color de la curva.
        segments: Número de segmentos para renderizar la curva.

    Returns:
        None
    """
    prev_point = p0
    
    for i in range(1, segments + 1):
        t = i / float(segments)
        
        # Coeficientes
        u = 1 - t
        u2 = u * u
        u3 = u2 * u
        t2 = t * t
        t3 = t2 * t
        
        # Ecuación polinómica
        x = u3 * p0[0] + 3 * u2 * t * p1[0] + 3 * u * t2 * p2[0] + t3 * p3[0]
        y = u3 * p0[1] + 3 * u2 * t * p1[1] + 3 * u * t2 * p2[1] + t3 * p3[1]
        
        current_point = (int(round(x)), int(round(y)))
        
        draw_bresenham_line(surface, prev_point[0], prev_point[1], current_point[0], current_point[1], color)
        
        prev_point = current_point
