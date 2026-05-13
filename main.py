"""
Punto de entrada principal para la aplicación Graficador Interactivo 2D.

Módulo que contiene la clase Application, la cual orquesta la inicialización
de pygame, interfaz gráfica, manejo de eventos y renderizado de formas
geométricas usando diversos algoritmos de rasterización.
"""
import pygame
import sys
import math
import tkinter as tk
from tkinter import filedialog

from utils.constants import *
from utils.colors import *
from ui.interface import Interface
from ui.events import EventHandler

from algorithms.dda import draw_dda
from algorithms.bresenham import draw_bresenham_line
from algorithms.circle import draw_bresenham_circle
from algorithms.ellipse import draw_ellipse
from algorithms.polygon import draw_polygon, draw_rectangle, draw_triangle, draw_hexagon
from algorithms.bezier import draw_bezier_cubic


class Application:
    """
    Clase principal de la aplicación Graficador Interactivo 2D.
    
    Gestiona el ciclo de renderizado, la interfaz de usuario, el manejo de eventos
    y la comunicación entre componentes. Coordina el dibujo de formas geométricas
    en el lienzo mediante diferentes algoritmos.
    """

    def __init__(self):
        """
        Inicializa la aplicación.
        
        Configura pygame, crea la ventana principal, superficies de canvas y preview,
        inicializa la interfaz gráfica y el manejador de eventos.
        
        Parámetros:
            No recibe parámetros.
        
        Retorna:
            No retorna valor.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        self.canvas_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.canvas_surface.fill(WHITE)
        
        self.preview_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.preview_surface.set_colorkey((0, 255, 0))  # Transparente
        
        # Historial para deshacer (pila de estados)
        self.history_stack = []
        
        self.active_tool = TOOL_DDA
        self.active_color = BLACK
        
        self.ui = Interface(
            set_tool_callback=self.set_tool,
            clear_canvas_callback=self.clear_canvas,
            set_color_callback=self.set_color,
            undo_callback=self.undo_action,
            open_callback=self.open_image,
            save_callback=self.save_image,
            manual_callback=self.open_manual
        )
        
        self.event_handler = EventHandler(self)

    def set_tool(self, tool_name: str):
        """
        Cambia la herramienta de dibujo activa.
        
        Actualiza la herramienta seleccionada, reinicia los puntos acumulados
        y redibuja la vista previa.
        
        Parámetros:
            tool_name (str): Nombre de la herramienta a activar.
        
        Retorna:
            No retorna valor.
        """
        self.active_tool = tool_name
        self.event_handler.points = []
        self.draw_preview()

    def set_color(self, color: tuple):
        """
        Establece el color activo para dibujar.
        
        Parámetros:
            color (tuple): Tupla RGB (R, G, B) representando el color.
        
        Retorna:
            No retorna valor.
        """
        self.active_color = color

    def clear_canvas(self):
        """
        Limpia el lienzo de dibujo.
        
        Rellena la superficie del canvas con color blanco y reinicia la vista previa.
        
        Parámetros:
            No recibe parámetros.
        
        Retorna:
            No retorna valor.
        """
        self.save_history()
        self.canvas_surface.fill(WHITE)
        self.draw_preview()

    def commit_shape(self, points: list):
        """
        Confirma y dibuja una forma en el lienzo principal.
        
        Renderiza la forma actual en la superficie del canvas usando los puntos
        y la herramienta activa, y limpia la vista previa.
        
        Parámetros:
            points (list): Lista de tuplas (x, y) representando los puntos de la forma.
        
        Retorna:
            No retorna valor.
        """
        self.save_history()
        self._render_shape(self.canvas_surface, self.active_tool, points, self.active_color)
        self.preview_surface.fill((0, 255, 0))

    def draw_preview(self):
        """
        Redibuja la vista previa con la forma actual siendo dibujada.
        
        Limpia la superficie de preview y dibuja una representación de la forma
        que se está construyendo en tiempo real, mostrando puntos de control
        y líneas preliminares según la herramienta activa.
        
        Parámetros:
            No recibe parámetros.
        
        Retorna:
            No retorna valor.
        """
        self.preview_surface.fill((0, 255, 0))
        points = self.event_handler.points
        if not points:
            return
            
        if self.active_tool in (TOOL_POLYGON, TOOL_BEZIER, TOOL_TRIANGLE):
            for p in points:
                rect = pygame.Rect(p[0] - 2, p[1] - 2, 4, 4)
                self.preview_surface.fill(RED, rect)
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    draw_dda(self.preview_surface, points[i][0], points[i][1], 
                             points[i+1][0], points[i+1][1], GRAY)
        else:
            if len(points) >= 2:
                self._render_shape(self.preview_surface, self.active_tool, points, 
                                   self.active_color)

    def _render_shape(self, surface: pygame.Surface, tool: str, points: list, 
                      color: tuple):
        """
        Renderiza una forma geométrica en la superficie especificada.
        
        Utiliza el algoritmo de dibujo correspondiente a la herramienta activa
        para dibujar la forma con los puntos proporcionados.
        
        Parámetros:
            surface (pygame.Surface): Superficie de pygame donde dibujar.
            tool (str): Nombre de la herramienta/algoritmo a usar.
            points (list): Lista de tuplas (x, y) con los puntos de la forma.
            color (tuple): Tupla RGB del color a usar en el dibujo.
        
        Retorna:
            No retorna valor.
        
        Notas:
            - Para líneas (DDA, Bresenham): usa primer y último punto.
            - Para círculo: calcula radio a partir de los dos puntos.
            - Para elipse: calcula radios horizontal y vertical.
            - Para rectángulo: usa dos esquinas opuestas.
            - Para polígono: dibuja líneas entre todos los puntos consecutivos.
            - Para triángulo: requiere exactamente 3 puntos.
            - Para Bézier: requiere exactamente 4 puntos de control.
        """
        if tool == TOOL_DDA:
            draw_dda(surface, points[0][0], points[0][1], points[-1][0], 
                     points[-1][1], color)
            
        elif tool == TOOL_BRESENHAM_LINE:
            draw_bresenham_line(surface, points[0][0], points[0][1], points[-1][0], 
                                points[-1][1], color)
            
        elif tool == TOOL_BRESENHAM_CIRCLE:
            dx = points[-1][0] - points[0][0]
            dy = points[-1][1] - points[0][1]
            r = int(math.sqrt(dx*dx + dy*dy))
            if r > 0:
                draw_bresenham_circle(surface, points[0][0], points[0][1], r, color)
                
        elif tool == TOOL_ELLIPSE:
            dx = abs(points[-1][0] - points[0][0])
            dy = abs(points[-1][1] - points[0][1])
            if dx > 0 and dy > 0:
                draw_ellipse(surface, points[0][0], points[0][1], dx, dy, color)
                
        elif tool == TOOL_RECTANGLE:
            draw_rectangle(surface, min(points[0][0], points[-1][0]), 
                          min(points[0][1], points[-1][1]), 
                          max(points[0][0], points[-1][0]), 
                          max(points[0][1], points[-1][1]), color)
            
        elif tool == TOOL_POLYGON:
            draw_polygon(surface, points, color)
            
        elif tool == TOOL_TRIANGLE:
            if len(points) == 3:
                draw_triangle(surface, points[0][0], points[0][1], points[1][0], 
                             points[1][1], points[2][0], points[2][1], color)
                
        elif tool == TOOL_BEZIER:
            if len(points) == 4:
                draw_bezier_cubic(surface, points[0], points[1], points[2], 
                                 points[3], color)
                
        elif tool == TOOL_HEXAGON:
            dx = points[-1][0] - points[0][0]
            dy = points[-1][1] - points[0][1]
            r = int(math.sqrt(dx*dx + dy*dy))
            if r > 0:
                draw_hexagon(surface, points[0][0], points[0][1], r, color)

    def save_history(self):
        """Guarda una copia del estado actual del lienzo para permitir deshacer."""
        self.history_stack.append(self.canvas_surface.copy())
        # Limitar el historial a 20 estados para no consumir demasiada memoria
        if len(self.history_stack) > 20:
            self.history_stack.pop(0)

    def undo_action(self):
        """Restaura el lienzo al estado previo a la última acción."""
        if self.history_stack:
            last_state = self.history_stack.pop()
            self.canvas_surface.blit(last_state, (0, 0))
            self.draw_preview()

    def open_manual(self):
        """Abre el archivo manual_usuario.md en una ventana independiente sin bloquear."""
        import threading
        import os
        
        def show_window():
            from tkinter import scrolledtext, WORD, BOTH, INSERT, messagebox
            
            path = os.path.join("docs", "manual_usuario.md")
            if not os.path.exists(path):
                # Necesitamos un root temporal para el messagebox
                temp_root = tk.Tk()
                temp_root.withdraw()
                messagebox.showerror("Error", f"No se encontró el archivo: {path}")
                temp_root.destroy()
                return

            manual_win = tk.Tk()
            manual_win.title("Manual de Usuario")
            manual_win.geometry("600x500")
            
            text_area = scrolledtext.ScrolledText(manual_win, wrap=WORD, width=80, height=30)
            text_area.pack(padx=10, pady=10, fill=BOTH, expand=True)
            
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                text_area.insert(INSERT, content)
                text_area.configure(state='disabled')
            except Exception as e:
                text_area.insert(INSERT, f"Error al leer el archivo: {e}")
            
            manual_win.mainloop()

        # Ejecutar en un hilo separado para no bloquear pygame
        thread = threading.Thread(target=show_window, daemon=True)
        thread.start()

    def open_image(self):
        """Abre un cuadro de diálogo para cargar una imagen PNG como fondo del lienzo."""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen PNG",
            filetypes=[("Archivos PNG", "*.png")]
        )
        root.destroy()
        
        if file_path:
            try:
                self.save_history()
                img = pygame.image.load(file_path).convert()
                # Ajustar imagen al tamaño del lienzo manteniendo la relación de aspecto si es necesario
                # Por simplicidad y según requerimientos, se blitea directamente
                self.canvas_surface.blit(img, (0, 0))
                self.draw_preview()
            except pygame.error as e:
                print(f"Error al cargar la imagen: {e}")

    def save_image(self):
        """Guarda el contenido actual del lienzo en un archivo PNG."""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            title="Guardar lienzo como PNG",
            defaultextension=".png",
            filetypes=[("Archivos PNG", "*.png")]
        )
        root.destroy()
        
        if file_path:
            try:
                pygame.image.save(self.canvas_surface, file_path)
            except pygame.error as e:
                print(f"Error al guardar la imagen: {e}")

    def run(self):
        """
        Inicia el ciclo principal de la aplicación.
        
        Ejecuta el bucle de eventos, procesa interacciones del usuario,
        actualiza la interfaz gráfica y el lienzo en tiempo real, manteniendo
        la velocidad de fotogramas especificada en FPS.
        
        Parámetros:
            No recibe parámetros.
        
        Retorna:
            No retorna valor.
        
        Notas:
            Se ejecuta indefinidamente hasta que el usuario cierre la ventana.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                self.ui.handle_event(event)
                self.event_handler.handle_event(event)
                self.event_handler.handle_keyboard(event)

            self.screen.fill((200, 200, 200))
            self.ui.draw(self.screen)
            self.screen.blit(self.canvas_surface, (UI_PANEL_WIDTH, TOP_BAR_HEIGHT))
            self.screen.blit(self.preview_surface, (UI_PANEL_WIDTH, TOP_BAR_HEIGHT))
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = Application()
    app.run()
