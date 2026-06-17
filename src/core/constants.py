"""
Módulo de constantes globales para el proyecto UBA - Sumativas.
Aquí se definen los valores estáticos fundamentales del juego.
"""

# Configuración de la Ventana
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
SCREEN_TITLE: str = "UBA - Combate de Sumativas"

# Configuración del TileMap y Escala
TILE_SIZE: int = 64
SPRITE_SCALING: float = 1.0

# Constantes del Jugador
PLAYER_MAX_HP: int = 3
PLAYER_MOVEMENT_SPEED: float = 5.0
PLAYER_JUMP_SPEED: float = 12.0
GRAVITY: float = 0.8
I_FRAMES_DURATION: float = 1.2  # Segundos de invulnerabilidad

# Constantes del Enemigo (Sumativas)
ENEMY_MAX_HP: int = 3
ENEMY_MOVEMENT_SPEED: float = 2.0
ENEMY_DETECTION_RANGE: int = 600  # Rango en píxeles para detectar al jugador

# Límites del Mundo
LIMITE_CAIDA_Y: int = -1000  # Cota Y bajo la cual el jugador muere instantáneamente
