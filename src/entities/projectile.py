import arcade
from typing import Optional
from src.core.constants import TILE_SIZE

class Projectile(arcade.SpriteSolidColor):
    """
    Clase para manejar proyectiles (ráfagas de grafito y ecuaciones matemáticas).
    Incorpora rutinas estrictas de optimización para evitar memory leaks.
    """
    
    def __init__(self, is_player_projectile: bool = True):
        """
        Inicializa un proyectil genérico (Greyboxing con color sólido).
        
        Args:
            is_player_projectile: Define si es un láser (True) o un proyectil tóxico (False).
        """
        if is_player_projectile:
            # Láser: Rectángulo amarillo
            super().__init__(16, 4, color=arcade.color.YELLOW)
        else:
            # Proyectil Tóxico (Zombie): Bola verde pequeña
            super().__init__(12, 12, color=arcade.color.GREEN)
        
        # Etiqueta para distinguir entre ataques del jugador y de los zombies
        self.is_player_projectile: bool = is_player_projectile
        
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
