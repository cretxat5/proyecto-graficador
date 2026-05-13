"""
Funciones auxiliares para el proyecto.
"""
import pygame

def draw_pixel(surface, x, y, color):
    """
    Dibuja un píxel individual en la superficie dada utilizando set_at.

    Args:
        surface: Superficie de pygame donde dibujar.
        x: Coordenada X.
        y: Coordenada Y.
        color: Tupla RGB representando el color.

    Returns:
        None
    """
    # Verificar límites de la superficie para evitar errores
    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        surface.set_at((int(x), int(y)), color)
