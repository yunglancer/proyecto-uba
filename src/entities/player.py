import arcade
from typing import Optional, List
import os
from src.core.constants import PLAYER_MAX_HP, I_FRAMES_DURATION

def load_texture_pair(filename: str):
    """Carga un par de texturas (original y volteada horizontalmente)"""
    original = arcade.load_texture(filename)
    return [
        original,
        original.flip_horizontally()
    ]

class Player(arcade.Sprite):
    """
    Clase que representa al jugador (estudiante de ingeniería UBA).
    Maneja salud, escudo de burbuja, i-frames asíncronos, salto doble y animaciones.
    """
    
    def __init__(self, image_file: str, scale: float):
        """
        Inicializa al jugador cargando sus texturas de animación.
        """
        # hit_box_algorithm="Simple" forzado como regla de arquitectura
        super().__init__(filename=image_file, scale=scale, hit_box_algorithm="Simple")
        
        # Estadísticas base
        self.hp: int = PLAYER_MAX_HP
        
        # Mecánicas Especiales
        self.has_bubble_shield: bool = True
        
        # Sistema de Salto Doble
        self.can_double_jump: bool = True
        self.is_jumping: bool = False
        
        # Sistema de Invulnerabilidad (I-Frames)
        self.is_invulnerable: bool = False
        self.invulnerability_timer: float = 0.0
        
        # Sistema de Combate
        self.can_shoot: bool = True
        self.shoot_timer: float = 0.0
        self.shoot_cooldown: float = 0.5
        
        # Estado de Animación
        self.character_face_direction: int = 0  # 0 = Derecha, 1 = Izquierda
        self.facing_direction: int = 1  # Lógico: 1 = Derecha, -1 = Izquierda
        self.cur_texture: float = 0.0
        
        # Carga de Texturas (Placeholder con Robot de Arcade)
        # TODO: Cuando estén los assets, cambiar estas rutas a las imágenes reales
        main_path = ":resources:images/animated_characters/robot/robot"
        
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")
        
        self.walk_textures: List[list] = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)
            
        # Establecer textura inicial
        self.texture = self.idle_texture_pair[0]

    def take_damage(self, amount: int = 1) -> None:
        """Aplica daño considerando el escudo y los I-Frames."""
        if self.is_invulnerable:
            return
            
        if self.has_bubble_shield:
            self.has_bubble_shield = False
            self.trigger_invulnerability()
            return
            
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
            
        self.trigger_invulnerability()
        
    def trigger_invulnerability(self) -> None:
        """Activa I-Frames."""
        self.is_invulnerable = True
        self.invulnerability_timer = I_FRAMES_DURATION
        
    def reset_jump(self) -> None:
        """Reinicia la capacidad de salto (llamado al tocar suelo)."""
        self.can_double_jump = True
        self.is_jumping = False
        
    def attempt_shoot(self) -> bool:
        """Intenta disparar. Devuelve True si el cooldown lo permite."""
        if self.can_shoot:
            self.can_shoot = False
            self.shoot_timer = self.shoot_cooldown
            return True
        return False
        
    def update_animation(self, delta_time: float = 1/60) -> None:
        """Lógica para cambiar la textura según el estado de movimiento."""
        
        # Determinar dirección visual
        if self.change_x < 0 and self.character_face_direction == 0:
            self.character_face_direction = 1
        elif self.change_x > 0 and self.character_face_direction == 1:
            self.character_face_direction = 0
            
        # Animación de Salto/Caída
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Animación Idle (Quieto)
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Animación de Caminar
        # Ajustamos la velocidad de la animación según delta_time
        self.cur_texture += 15 * delta_time
        if self.cur_texture >= len(self.walk_textures):
            self.cur_texture = 0
            
        frame = int(self.cur_texture)
        self.texture = self.walk_textures[frame][self.character_face_direction]

    def on_update(self, delta_time: float = 1/60) -> None:
        """Actualización lógica del jugador en cada frame."""
        
        # I-Frames
        if self.is_invulnerable:
            self.invulnerability_timer -= delta_time
            if int(self.invulnerability_timer * 10) % 2 == 0:
                self.alpha = 100
            else:
                self.alpha = 255
                
            if self.invulnerability_timer <= 0:
                self.is_invulnerable = False
                self.alpha = 255
                
        # Cooldown de Disparo
        if not self.can_shoot:
            self.shoot_timer -= delta_time
            if self.shoot_timer <= 0:
                self.can_shoot = True
                
        # Actualización de la dirección lógica
        if self.change_x > 0:
            self.facing_direction = 1
        elif self.change_x < 0:
            self.facing_direction = -1
            
        # Ejecutar lógica de animación
        self.update_animation(delta_time)
