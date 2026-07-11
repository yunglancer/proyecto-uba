import arcade
from typing import Optional, List
from src.core.constants import ENEMY_MAX_HP, ENEMY_MOVEMENT_SPEED, ENEMY_DETECTION_RANGE, TILE_SIZE, GRAVITY

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
    
    def __init__(self, enemy_type: str = "shooter"):
        """
        Inicializa al enemigo cargando sus texturas animadas.
        """
        # hit_box_algorithm="Simple" forzado como regla de arquitectura
        super().__init__(hit_box_algorithm="Simple")
        
        self.enemy_type = enemy_type
        
        # Estadísticas basadas en el tipo
        self.hp: int = ENEMY_MAX_HP if enemy_type == "shooter" else ENEMY_MAX_HP - 1
        self.speed: float = ENEMY_MOVEMENT_SPEED if enemy_type == "shooter" else ENEMY_MOVEMENT_SPEED * 2.5
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
        
        # Color distintivo para el runner
        if self.enemy_type == "runner":
            self.color = arcade.color.ORANGE_RED
        
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
            
    def update_patrol(self, ground_list: arcade.SpriteList, player: Optional[arcade.Sprite] = None) -> None:
        """
        Lógica de patrullaje, persecución, gravedad simple y detección de bordes.
        """
        # 0. Gravedad y colisión vertical
        self.change_y -= GRAVITY
        self.center_y += self.change_y
        
        # Chequeo de colisión con el suelo (usando la parte inferior del sprite)
        ground_hits = arcade.get_sprites_at_point((self.center_x, self.bottom), ground_list)
        if ground_hits:
            # Encontrar el bloque más alto
            highest_top = max([block.top for block in ground_hits])
            if self.bottom < highest_top and self.change_y < 0:
                self.bottom = highest_top
                self.change_y = 0
        
        # 1. Determinar dirección objetivo
        direction_x = 1 if self.change_x > 0 else (-1 if self.change_x < 0 else (1 if self.character_face_direction == 0 else -1))
        
        is_pursuing = False
        if self.enemy_type == "runner" and player:
            dist_x = player.center_x - self.center_x
            dist_y = player.center_y - self.center_y
            if (dist_x**2 + dist_y**2)**0.5 <= ENEMY_DETECTION_RANGE:
                direction_x = 1 if dist_x > 0 else -1
                
        # 2. Predicción de caída y paredes frontales
        check_x = self.center_x + (TILE_SIZE * direction_x)
        check_y = self.center_y - TILE_SIZE - 4  # Un poco más abajo para asegurar que entre al hitbox del bloque
        
        hit_list = arcade.get_sprites_at_point((check_x, check_y), ground_list)
        wall_hit_list = arcade.get_sprites_at_point((check_x, self.center_y), ground_list)
        
        # 3. Aplicar físicas
        if not hit_list or wall_hit_list:
            if self.enemy_type == "runner" and player and (player.center_x - self.center_x)**2 <= ENEMY_DETECTION_RANGE**2:
                # Si es runner y está persiguiendo, se tira del precipicio sin miedo (ignoramos hit_list)
                if wall_hit_list:
                    self.change_x = 0 # Pero si hay pared, se frena
                else:
                    self.change_x = self.speed * direction_x
            elif self.enemy_type == "runner":
                # Si es runner pero el jugador no está cerca, se frena en el borde
                self.change_x = 0
            else:
                # Shooter: Patrullaje normal, da la vuelta en bordes o paredes
                self.change_x = self.speed * (direction_x * -1)
        else:
            # Camino libre
            self.change_x = self.speed * direction_x
            
    def check_and_shoot(self, player: arcade.Sprite, delta_time: float) -> bool:
        """
        Verifica si el jugador está a rango de visión para disparar.
        Retorna True si debe efectuar el disparo. (Runners no disparan).
        """
        if self.enemy_type == "runner":
            return False
            
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
