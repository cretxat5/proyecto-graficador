"""
Modelo base para las figuras dibujadas en el lienzo.
"""

class Figure:
    """
    Clase que representa una figura genérica.
    Permite encapsular la información geométrica para posibles redibujos o extensiones.
    """
    def __init__(self, type_name: str, color: tuple, points: list):
        """
        Inicializa una figura.

        Args:
            type_name: Nombre del tipo de figura (ej. "DDA").
            color: Color de la figura.
            points: Lista de puntos o vértices relevantes.
        """
        self.type_name = type_name
        self.color = color
        self.points = points
        
    def get_points(self):
        """
        Devuelve los puntos de la figura.

        Returns:
            Lista de puntos.
        """
        return self.points
