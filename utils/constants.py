"""
Constantes globales del proyecto.
"""

# Configuración de ventana
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
WINDOW_TITLE = "Graficador Interactivo 2D"

# Configuración de FPS
FPS = 60

# Configuración de UI
UI_PANEL_WIDTH = 250
CANVAS_WIDTH = WINDOW_WIDTH - UI_PANEL_WIDTH
CANVAS_HEIGHT = WINDOW_HEIGHT

# Herramientas disponibles
TOOL_DDA = "DDA"
TOOL_BRESENHAM_LINE = "Bresenham Línea"
TOOL_BRESENHAM_CIRCLE = "Bresenham Circunferencia"
TOOL_ELLIPSE = "Elipse"
TOOL_POLYGON = "Polígono"
TOOL_BEZIER = "Bézier"
TOOL_TRIANGLE = "Triángulo"
TOOL_RECTANGLE = "Rectángulo"

TOOLS = [
    TOOL_DDA,
    TOOL_BRESENHAM_LINE,
    TOOL_BRESENHAM_CIRCLE,
    TOOL_ELLIPSE,
    TOOL_POLYGON,
    TOOL_BEZIER,
    TOOL_TRIANGLE,
    TOOL_RECTANGLE
]
