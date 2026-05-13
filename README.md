# Graficador Interactivo 2D en Python

Este proyecto implementa algoritmos gráficos clásicos para la rasterización de figuras geométricas 2D desde cero, sin utilizar primitivas de dibujo.

## Instalación

1. Clona el repositorio.
2. Instala Python 3.8+
3. Instala pygame:
   ```bash
   pip install pygame
   ```

## Ejecución

Ejecuta el archivo principal desde la raíz del proyecto:
```bash
python main.py
```

## Dependencias
- Python 3.8 o superior
- Pygame (`pip install pygame`)

## Controles
- Clic y arrastrar para la mayoría de las figuras.
- Clics sucesivos para Polígonos, Triángulos y Bézier.
- `Enter` para cerrar un polígono en edición.
- `ESC` para cancelar edición actual.

## Arquitectura
El proyecto sigue una arquitectura modular estricta que separa la interfaz gráfica de la lógica de los algoritmos y los modelos de datos.
