
import arcade
from typing import Optional
from src.core.constants import PLAYER_MAX_HP, I_FRAMES_DURATION

class Player(arcade.Sprite):
    """
    Clase que representa al jugador (estudiante de ingeniería UBA).
    Maneja salud, escudo de burbuja, i-frames asíncronos y estado de salto doble.
    """
    
    def __init__(self, image_file: str, scale: float):
        """
        Inicializa al jugador con sus valores predeterminados y caja de colisión simple.
        
        Args:
            image_file: Ruta de la imagen del sprite.
            scale: Escala de renderizado del sprite.
        """
        # hit_box_algorithm="Simple" forzado como regla de arquitectura
        super().__init__(filename=image_file, scale=scale, hit_box_algorithm="Simple")
        
        # Estadísticas base
        self.hp: int = PLAYER_MAX_HP
        
        # Mecánicas Especiales
        self.has_bubble_shield: bool = True  # Escudo que absorbe 1 impacto
        
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
        
        # Dirección a la que mira el jugador (1 = derecha, -1 = izquierda)
        self.facing_direction: int = 1
        
    def take_damage(self, amount: int = 1) -> None:
        """
        Aplica daño al jugador considerando el escudo y los I-Frames.
        Activa la invulnerabilidad temporal si recibe daño real.
        """
        if self.is_invulnerable:
            return
            
        # El escudo absorbe el impacto si está activo
        if self.has_bubble_shield:
            self.has_bubble_shield = False
            self.trigger_invulnerability()
            return
            
        # Aplica el daño real
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
            
        self.trigger_invulnerability()
        
    def trigger_invulnerability(self) -> None:
        """Activa el estado de invulnerabilidad (I-Frames)."""
        self.is_invulnerable = True
        self.invulnerability_timer = I_FRAMES_DURATION
        
    def reset_jump(self) -> None:
        """
        Reinicia la capacidad de salto. 
        Debe ser llamado estrictamente cuando el jugador colisiona con el suelo.
        """
        self.can_double_jump = True
        self.is_jumping = False
        
    def attempt_shoot(self) -> bool:
        """
        Intenta disparar. Devuelve True si el cooldown lo permite.
        Al disparar, reinicia el timer.
        """
        if self.can_shoot:
            self.can_shoot = False
            self.shoot_timer = self.shoot_cooldown
            return True
        return False
        
    def on_update(self, delta_time: float = 1/60) -> None:
        """
        Actualización lógica del jugador en cada frame.
        Maneja los I-Frames de forma asíncrona usando delta_time.
        """
        # Actualización de Invulnerabilidad
        if self.is_invulnerable:
            self.invulnerability_timer -= delta_time
            
            # Efecto visual de parpadeo (flickering)
            # Oscila la transparencia entre 255 (opaco) y 100 (translúcido)
            if int(self.invulnerability_timer * 10) % 2 == 0:
                self.alpha = 100
            else:
                self.alpha = 255
                
            # Fin de los I-Frames
            if self.invulnerability_timer <= 0:
                self.is_invulnerable = False
                self.alpha = 255  # Restaura la opacidad total
                
        # Actualización del Cooldown de Disparo
        if not self.can_shoot:
            self.shoot_timer -= delta_time
            if self.shoot_timer <= 0:
                self.can_shoot = True
                
        # Actualización de la dirección según el movimiento
        if self.change_x > 0:
            self.facing_direction = 1
        elif self.change_x < 0:
            self.facing_direction = -1
