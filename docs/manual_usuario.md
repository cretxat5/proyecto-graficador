# Manual de Usuario - Graficador Interactivo 2D

## Uso de herramientas
El panel izquierdo contiene todas las herramientas disponibles. Haz clic en una herramienta para activarla.

## Controles
- **DDA / Bresenham / Elipse / Rectángulo**: Haz clic en el lienzo (mantén presionado) y arrastra para dibujar la figura. Suelta el clic para finalizar.
- **Polígono**: Haz clic para agregar vértices. Presiona `Enter` para cerrar el polígono y dibujarlo de forma permanente.
- **Triángulo**: Haz clic en 3 puntos distintos del lienzo. Al marcar el tercer punto, el triángulo se dibujará automáticamente.
- **Bézier**: Haz clic en 4 puntos distintos. El primer y último punto serán los extremos, los dos intermedios serán los puntos de control de la curva Bézier cúbica.
- **Escape (ESC)**: Presiona esta tecla para cancelar la figura en progreso (por ejemplo, al crear un polígono o curva Bézier).
- **Colores**: Haz clic en cualquier color de la paleta para activarlo.
- **Limpiar Lienzo**: Borra todo el área de dibujo.

## Explicación de Figuras
- **DDA / Bresenham Línea**: Trazan líneas rectas entre dos puntos con algoritmos de rasterización.
- **Circunferencia Bresenham**: Traza un círculo perfecto utilizando enteros (simetría de octantes).
- **Elipse**: Traza elipses con el algoritmo del punto medio.
- **Bézier**: Genera curvas suaves utilizando 4 puntos de control e interpolación matemática.
