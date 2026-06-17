import arcade
from typing import Optional
from src.core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, SPRITE_SCALING,
    GRAVITY, PLAYER_MOVEMENT_SPEED, PLAYER_JUMP_SPEED, LIMITE_CAIDA_Y
)
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.projectile import Projectile
from src.views.game_over import GameOver

class GameView(arcade.View):
    """
    Vista principal del juego.
    Maneja la carga del TileMap, físicas, cámara y lógica de la partida.
    """
    
    def __init__(self, level: int = 1, skin_path: str = ":resources:images/animated_characters/robot/robot_idle.png"):
        """
        Inicializa la vista y sus variables.
        
        Args:
            level: Identificador del nivel a cargar (1 o 2).
            skin_path: Ruta del asset del jugador seleccionado.
        """
        super().__init__()
        
        self.level_id = level
        self.player_skin = skin_path
        
        # Sistemas principales
        self.tile_map: Optional[arcade.TileMap] = None
        self.scene: Optional[arcade.Scene] = None
        self.physics_engine: Optional[arcade.PhysicsEnginePlatformer] = None
        
        # Cámaras
        self.camera: Optional[arcade.camera.Camera2D] = None
        self.gui_camera: Optional[arcade.camera.Camera2D] = None
        
        # Entidades principales
        self.player_sprite: Optional[Player] = None
        
        # Variables de progreso
        self.key_spawned: bool = False
        self.key_sprite: Optional[arcade.Sprite] = None

    def setup(self) -> None:
        """
        Inicializa (o reinicia) el nivel cargando los recursos limpiamente
        para evitar fugas de memoria, tal como exige el GDD.
        """
        # 1. Configuración de Cámaras
        self.camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        
        # 2. Reinicio de variables de control
        self.key_spawned = False
        
        # 3. Inicialización del Scene y TileMap
        import os
        map_path = f"assets/maps/nivel_{self.level_id}.json"
        
        if os.path.exists(map_path):
            # Carga real del mapa Tiled (El compañero generará estos JSON)
            self.tile_map = arcade.load_tilemap(map_path, scaling=SPRITE_SCALING)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
        else:
            # Fallback Placeholder para evitar crasheos si el artista no ha exportado el .json
            self.scene = arcade.Scene()
            self.scene.add_sprite_list("Suelo")
            # Suelo plano para pruebas
            for x in range(0, 2000, 64):
                suelo = arcade.SpriteSolidColor(64, 64, arcade.color.DARK_GREEN)
                suelo.center_x = x
                suelo.center_y = 32
                self.scene.add_sprite("Suelo", suelo)
                
        # Asegurarnos de que las capas obligatorias existan en el Scene (por si el JSON está incompleto)
        for layer in ["Player", "Enemigos", "Proyectiles", "Objetos", "Suelo"]:
            try:
                self.scene.get_sprite_list(layer)
            except KeyError:
                self.scene.add_sprite_list(layer)
        
        # Instanciar al jugador
        self.player_sprite = Player(self.player_skin, SPRITE_SCALING)
        
        # Opcional: Leer punto de Spawn desde Tiled. Por defecto fijamos 128x256
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 256
        self.scene.add_sprite("Player", self.player_sprite)
            
        # 4. Motor de Físicas (Plataformero estricto)
        # Se ancla la gravedad y se utiliza la capa "Suelo" estrictamente como pared
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene.get_sprite_list("Suelo")
        )
        
        # 5. Configurar color de fondo (Si Tiled lo trae, lo usa, si no, uno por defecto)
        if self.tile_map and self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        else:
            arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_show_view(self) -> None:
        """Se llama cuando esta vista se activa en pantalla."""
        self.setup()

    def on_draw(self) -> None:
        """Renderiza la pantalla."""
        self.clear()
        
        # 1. Dibujar el mundo con la cámara del mundo
        if self.camera:
            self.camera.use()
        
        if self.scene:
            self.scene.draw()
            
        # 2. Dibujar UI estática con la cámara de interfaz
        if self.gui_camera:
            self.gui_camera.use()
            
        # Renderizado temporal de la UI (Salud)
        if self.player_sprite:
            arcade.draw_text(f"HP: {self.player_sprite.hp}", 20, SCREEN_HEIGHT - 40, arcade.color.RED, 24, bold=True)
            if self.player_sprite.has_bubble_shield:
                arcade.draw_text("ESCUDO ACTIVO", 20, SCREEN_HEIGHT - 70, arcade.color.CYAN, 18, bold=True)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Maneja el inicio del input por teclado del jugador."""
        if not self.player_sprite or not self.physics_engine:
            return
            
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            # Lógica de Salto (Simple o Doble)
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.player_sprite.is_jumping = True
            elif self.player_sprite.can_double_jump and self.player_sprite.is_jumping:
                # El doble salto sólo se activa si fue habilitado al soltar la tecla
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.player_sprite.can_double_jump = False
        elif key == arcade.key.V:
            # Atajo de desarrollador para probar la pantalla de Victoria
            game_over_view = GameOver(is_victory=True)
            self.window.show_view(game_over_view)
                
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Maneja el input cuando se sueltan las teclas."""
        if not self.player_sprite:
            return
            
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
            
    def center_camera_to_player(self) -> None:
        """Mueve la cámara suavemente siguiendo al jugador."""
        if not self.camera or not self.player_sprite:
            return
            
        # En Arcade 3, Camera2D.position es el centro exacto de la cámara
        target_x = self.player_sprite.center_x
        target_y = self.player_sprite.center_y
        
        # Evitar que la cámara muestre la zona fuera del mapa (coordenadas negativas)
        min_x = self.camera.viewport_width / 2
        min_y = self.camera.viewport_height / 2
        
        if target_x < min_x:
            target_x = min_x
        if target_y < min_y:
            target_y = min_y
            
        # Paneo dinámico suave usando lerp
        current_x, current_y = self.camera.position
        
        # 0.1 es la velocidad de suavizado (lerp)
        new_x = arcade.math.lerp(current_x, target_x, 0.1)
        new_y = arcade.math.lerp(current_y, target_y, 0.1)
            
        self.camera.position = (new_x, new_y)

    def on_update(self, delta_time: float) -> None:
        """Actualización de la lógica del juego fotograma a fotograma."""
        if not self.physics_engine or not self.player_sprite or not self.scene:
            return
            
        # 1. Actualizar Motor Físico
        self.physics_engine.update()
        
        # 2. Reinicio del salto al tocar el suelo
        if self.physics_engine.can_jump():
            self.player_sprite.reset_jump()
            
        # 3. Actualizar la cámara para seguir al jugador
        self.center_camera_to_player()
        
        # 4. Actualizar lógica de entidades genéricas
        self.scene.update(delta_time, ["Player", "Enemigos", "Proyectiles"])
        
        # 5. Lógica de optimización de proyectiles (colisiones de entorno)
        for proj in self.scene.get_sprite_list("Proyectiles"):
            # Si el proyectil colisiona con el suelo, lo destruimos (self.kill)
            wall_hit_list = arcade.check_for_collision_with_list(proj, self.scene.get_sprite_list("Suelo"))
            if wall_hit_list:
                proj.kill()
                
        # 6. ZONA DE MUERTE: Si el jugador cae al vacío
        if self.player_sprite.center_y < LIMITE_CAIDA_Y:
            self.setup()  # Reiniciar nivel limpiamente
            
        # 7. DERROTA: Si el HP del jugador llega a 0
        if self.player_sprite.hp <= 0:
            game_over_view = GameOver(is_victory=False)
            self.window.show_view(game_over_view)
