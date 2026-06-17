import arcade
from typing import Optional
from src.core.constants import ENEMY_MAX_HP, ENEMY_MOVEMENT_SPEED, ENEMY_DETECTION_RANGE, TILE_SIZE

class Enemy(arcade.Sprite):
    """
    Clase que representa a los enemigos ("Sumativas").
    Manejan patrullaje automático, detección de bordes predictiva y disparo.
    """
    
    def __init__(self, image_file: str, scale: float):
        """
        Inicializa al enemigo con sus valores predeterminados y caja de colisión simple.
        
        Args:
            image_file: Ruta de la imagen del sprite.
            scale: Escala de renderizado del sprite.
        """
        super().__init__(filename=image_file, scale=scale, hit_box_algorithm="Simple")
        
        # Estadísticas
        self.hp: int = ENEMY_MAX_HP
        self.speed: float = ENEMY_MOVEMENT_SPEED
        self.change_x = self.speed  # Comienza moviéndose a la derecha
        
        # Estado de disparo
        self.can_shoot: bool = True
        self.shoot_timer: float = 0.0
        self.shoot_cooldown: float = 2.0  # Segundos entre disparos
        
    def take_damage(self, amount: int = 1) -> None:
        """Resta salud al enemigo y lo destruye si llega a cero."""
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
            
    def update_patrol(self, ground_list: arcade.SpriteList) -> None:
        """
        Maneja el patrullaje del enemigo.
        Calcula predictivamente si en la celda contigua (X +/- 64, Y - 64) hay suelo.
        Si está vacío, da la media vuelta para evitar caídas.
        
        Args:
            ground_list: SpriteList que contiene las plataformas o el suelo.
        """
        # Calcular el punto predictivo a revisar (+64X si va a la derecha, -64X si va a la izquierda)
        direction_x = 1 if self.change_x > 0 else -1
        
        # Calculamos la coordenada del centro de la próxima celda inferior
        check_x = self.center_x + (TILE_SIZE * direction_x)
        check_y = self.center_y - TILE_SIZE
        
        # Verificamos si existe un bloque en ese punto
        hit_list = arcade.get_sprites_at_point((check_x, check_y), ground_list)
        
        # Si no hay suelo (está a punto de caer), damos la vuelta
        if not hit_list:
            self.change_x *= -1
            
    def check_and_shoot(self, player: arcade.Sprite, delta_time: float) -> bool:
        """
        Verifica si el jugador está a rango de visión (< 600px) para disparar.
        Retorna True si debe efectuar el disparo (se instancia el proyectil en game_view).
        """
        # Actualizamos timer
        if not self.can_shoot:
            self.shoot_timer -= delta_time
            if self.shoot_timer <= 0:
                self.can_shoot = True
                
        # Calculamos distancia al jugador
        distance_x = player.center_x - self.center_x
        distance_y = player.center_y - self.center_y
        distance = (distance_x**2 + distance_y**2)**0.5
        
        # Si está en rango, visible y tiene cooldown listo, dispara
        if distance <= ENEMY_DETECTION_RANGE and self.can_shoot:
            self.can_shoot = False
            self.shoot_timer = self.shoot_cooldown
            return True
            
        return False
