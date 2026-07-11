import arcade
from typing import Optional, List
from src.core.constants import ENEMY_MAX_HP, ENEMY_MOVEMENT_SPEED, ENEMY_DETECTION_RANGE, TILE_SIZE

def load_texture_pair(filename: str):
    """Carga un par de texturas (original y volteada horizontalmente)"""
    original = arcade.load_texture(filename)
    return [
        original,
        original.flip_horizontally()
    ]

class Enemy(arcade.Sprite):
    """
    Clase que representa a los enemigos ("Zombies").
    Manejan patrullaje automático, detección de bordes predictiva, disparo y animación.
    """
    
    def __init__(self):
        """
        Inicializa al enemigo cargando sus texturas animadas.
        """
        # hit_box_algorithm="Simple" forzado como regla de arquitectura
        super().__init__(hit_box_algorithm="Simple")
        
        # Estadísticas
        self.hp: int = ENEMY_MAX_HP
        self.speed: float = ENEMY_MOVEMENT_SPEED
        self.change_x = self.speed  # Comienza moviéndose a la derecha
        
        # Estado de disparo
        self.can_shoot: bool = True
        self.shoot_timer: float = 0.0
        self.shoot_cooldown: float = 4.5  # Segundos entre disparos
        
        # Estado de Animación
        self.character_face_direction: int = 0  # 0 = Derecha, 1 = Izquierda
        self.cur_texture: float = 0.0
        
        # Estado Visual de Daño
        self.is_hit: bool = False
        self.hit_timer: float = 0.0
        
        # Carga de Texturas (Placeholder con Zombie de Arcade)
        # TODO: Cuando estén los assets, cambiar estas rutas a las imágenes reales
        main_path = ":resources:images/animated_characters/zombie/zombie"
        
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        
        self.walk_textures: List[list] = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)
            
        # Establecer textura inicial
        self.texture = self.idle_texture_pair[0]
        
    def take_damage(self, amount: int = 1) -> None:
        """Resta salud al enemigo, muestra efecto de daño y lo destruye si llega a cero."""
        self.hp -= amount
        
        # Efecto de daño visual (parpadeo rojo)
        self.is_hit = True
        self.hit_timer = 0.2
        self.color = arcade.color.RED
        
        if self.hp <= 0:
            self.kill()
            
    def update_animation(self, delta_time: float = 1/60) -> None:
        """Actualiza el frame de animación del enemigo."""
        
        # Recuperación visual tras recibir daño
        if self.is_hit:
            self.hit_timer -= delta_time
            if self.hit_timer <= 0:
                self.is_hit = False
                self.color = arcade.color.WHITE
                
        # Determinar dirección visual
        if self.change_x < 0 and self.character_face_direction == 0:
            self.character_face_direction = 1
        elif self.change_x > 0 and self.character_face_direction == 1:
            self.character_face_direction = 0

        # Animación Idle (Quieto)
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Animación de Caminar
        self.cur_texture += 10 * delta_time
        if self.cur_texture >= len(self.walk_textures):
            self.cur_texture = 0
            
        frame = int(self.cur_texture)
        self.texture = self.walk_textures[frame][self.character_face_direction]
            
    def update_patrol(self, ground_list: arcade.SpriteList) -> None:
        """
        Maneja el patrullaje del enemigo.
        Calcula predictivamente si en la celda contigua (X +/- 64, Y - 64) hay suelo.
        Si está vacío o choca, da la media vuelta para evitar caídas.
        """
        direction_x = 1 if self.change_x > 0 else -1
        
        # Predicción de caída (Borde de plataforma)
        check_x = self.center_x + (TILE_SIZE * direction_x)
        check_y = self.center_y - TILE_SIZE
        
        hit_list = arcade.get_sprites_at_point((check_x, check_y), ground_list)
        
        # Predicción de choque con muro enfrente
        wall_check_x = self.center_x + (TILE_SIZE * direction_x)
        wall_check_y = self.center_y
        wall_hit_list = arcade.get_sprites_at_point((wall_check_x, wall_check_y), ground_list)
        
        # Si no hay suelo o hay pared, girar
        if not hit_list or wall_hit_list:
            self.change_x *= -1
            
    def check_and_shoot(self, player: arcade.Sprite, delta_time: float) -> bool:
        """
        Verifica si el jugador está a rango de visión para disparar.
        Retorna True si debe efectuar el disparo.
        """
        if not self.can_shoot:
            self.shoot_timer -= delta_time
            if self.shoot_timer <= 0:
                self.can_shoot = True
                
        distance_x = player.center_x - self.center_x
        distance_y = player.center_y - self.center_y
        distance = (distance_x**2 + distance_y**2)**0.5
        
        if distance <= ENEMY_DETECTION_RANGE and self.can_shoot:
            self.can_shoot = False
            self.shoot_timer = self.shoot_cooldown
            return True
            
        return False

    def on_update(self, delta_time: float = 1/60) -> None:
        """Actualización del enemigo (para compatibilidad con bucle principal)."""
        self.update_animation(delta_time)
