"""
Modelo de datos para representar un punto en 2D.
"""

class Point:
    """
    Clase que representa un punto en un espacio 2D.
    """
    def __init__(self, x: int, y: int):
        """
        Inicializa un punto.

        Args:
            x: Coordenada X del punto.
            y: Coordenada Y del punto.
        """
        self.x = x
        self.y = y

    def to_tuple(self):
        """
        Convierte el punto a una tupla (x, y).

        Returns:
            Tupla con coordenadas (x, y).
        """
        return (self.x, self.y)
