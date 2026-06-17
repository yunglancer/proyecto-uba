import arcade
from typing import Optional
from src.core.constants import TILE_SIZE

class Projectile(arcade.Sprite):
    """
    Clase para manejar proyectiles (ráfagas de grafito y ecuaciones matemáticas).
    Incorpora rutinas estrictas de optimización para evitar memory leaks.
    """
    
    def __init__(self, image_file: str, scale: float, is_enemy_projectile: bool = False):
        """
        Inicializa un proyectil genérico.
        
        Args:
            image_file: Ruta de la imagen del proyectil.
            scale: Escala de renderizado.
            is_enemy_projectile: Define si es una ecuación (True) o grafito (False).
        """
        super().__init__(filename=image_file, scale=scale, hit_box_algorithm="Simple")
        
        # Etiqueta para distinguir entre ataques del jugador y de las sumativas
        self.is_enemy_projectile: bool = is_enemy_projectile
        
        # Variables para optimización de recolección de basura
        # Se actualizarán desde el GameView cuando se cargue el mapa de Tiled
        self.limit_x_min: float = 0.0
        self.limit_x_max: float = 10000.0  # Valor por defecto grande, se sobreescribe
        self.limit_y_min: float = -2000.0
        
    def on_update(self, delta_time: float = 1/60) -> None:
        """
        Actualiza el proyectil. Si sale de los límites físicos del mapa,
        ejecuta kill() inmediatamente para destruir la instancia en la memoria RAM.
        """
        # Actualizar posición
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        # Control estricto de límites para evitar memory leaks
        if (self.center_x < self.limit_x_min or 
            self.center_x > self.limit_x_max or 
            self.center_y < self.limit_y_min):
            self.kill()
