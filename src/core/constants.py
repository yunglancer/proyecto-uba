"""
Constantes globales para el juego (Proyecto UBA).
"""

# Configuración de Ventana
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Proyecto UBA - Plataformero Asistido por IA"

# Configuración de Tiles y Escala
TILE_SIZE = 64
SPRITE_SCALING = 1.0

# Físicas
GRAVITY = 1.0
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 15
LIMITE_CAIDA_Y = -1000  # Límite donde el jugador muere al caer

# Estadísticas del Jugador
PLAYER_MAX_HP = 3
I_FRAMES_DURATION = 1.2  # Segundos de invulnerabilidad
PLAYER_SHOOT_COOLDOWN = 0.5  # Segundos entre disparos

# Estadísticas del Enemigo
ENEMY_MAX_HP = 3
ENEMY_SHOOT_COOLDOWN = 2.0  # Segundos entre disparos
ENEMY_MOVEMENT_SPEED = 2
ENEMY_DETECTION_RANGE = 600  # Píxeles de distancia para atacar

# Velocidad de Proyectiles
PROJECTILE_SPEED = 10

