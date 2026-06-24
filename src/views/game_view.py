import arcade
import math
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
        self.camera.zoom = 0.6  # Aleja la cámara para un plano más amplio tipo Katana Zero
        self.gui_camera = arcade.camera.Camera2D()
        
        # 2. Reinicio de variables de control
        self.key_spawned = False
        
        # Textos estáticos de UI para no generar PerformanceWarnings
        self.hp_text = arcade.Text("HP: 3", 20, SCREEN_HEIGHT - 40, arcade.color.RED, 24, bold=True)
        self.shield_text = arcade.Text("ESCUDO ACTIVO", 20, SCREEN_HEIGHT - 70, arcade.color.CYAN, 18, bold=True)
        
        # 3. Inicialización del Scene y TileMap
        import os
        map_path = f"assets/maps/nivel_{self.level_id}.json"
        
        if os.path.exists(map_path):
            # Carga real del mapa Tiled (El compañero generará estos JSON)
            try:
                self.tile_map = arcade.load_tilemap(map_path, scaling=SPRITE_SCALING)
                self.scene = arcade.Scene.from_tilemap(self.tile_map)
            except Exception as e:
                print(f"Error cargando mapa {map_path}: {e}. Usando mapa placeholder.")
                self.tile_map = None
                
        if not self.tile_map:
            # Fallback Placeholder para probar plataformas, huecos y muros
            self.scene = arcade.Scene()
            self.scene.add_sprite_list("Suelo")
            
            def crear_bloque(x, y):
                bloque = arcade.SpriteSolidColor(64, 64, arcade.color.DARK_GREEN)
                bloque.center_x = x
                bloque.center_y = y
                self.scene.add_sprite("Suelo", bloque)

            # Suelo base (con un hueco en el medio para probar caídas)
            for x in range(0, 3000, 64):
                if x < 800 or x > 1100:
                    crear_bloque(x, 32)
            
            # Plataforma 1 (Baja)
            for x in range(400, 700, 64):
                crear_bloque(x, 160)
                
            # Plataforma 2 (Alta)
            for x in range(1300, 1700, 64):
                crear_bloque(x, 288)
                
            # Muro vertical para probar bloqueo de balas
            for y in range(32, 288, 64):
                crear_bloque(2200, y)
                
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
        
        # Lista para la Llave de Aprobado
        self.scene.add_sprite_list("Llave")
        self.llave_spawned = False
        
        # Generar Enemigos (Sumativas) de prueba
        enemy1 = Enemy()
        enemy1.center_x = 550
        enemy1.bottom = 160 + 32 # Sobre la Plataforma 1
        self.scene.add_sprite("Enemigos", enemy1)
        
        enemy2 = Enemy()
        enemy2.center_x = 1500
        enemy2.bottom = 288 + 32 # Sobre la Plataforma 2
        self.scene.add_sprite("Enemigos", enemy2)
        
        enemy3 = Enemy()
        enemy3.center_x = 1800
        enemy3.bottom = 32 + 32 # En el suelo firme tras el hueco
        self.scene.add_sprite("Enemigos", enemy3)
            
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
            self.hp_text.text = f"HP: {self.player_sprite.hp}"
            self.hp_text.draw()
            if self.player_sprite.has_bubble_shield:
                self.shield_text.draw()

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
        elif key == arcade.key.J or key == arcade.key.Z:
            # Lógica de Disparo (Lápiz Mágico)
            if self.player_sprite.attempt_shoot():
                # Instanciar el proyectil (Greyboxing)
                projectile = Projectile(is_enemy_projectile=False)
                # Separar el disparo del jugador para no raspar el suelo accidentalmente
                projectile.center_x = self.player_sprite.center_x + (20 * self.player_sprite.facing_direction)
                # Apuntar el disparo a la altura del pecho de los enemigos (32px sobre su base)
                projectile.center_y = self.player_sprite.bottom + 32
                
                # Configurar límites para evitar memory leaks (del Nivel)
                projectile.limit_x_min = 0
                projectile.limit_x_max = 10000  # O el ancho de tu mapa Tiled
                projectile.limit_y_min = LIMITE_CAIDA_Y
                
                # Velocidad del proyectil (dispara hacia donde mira)
                projectile_speed = 15.0
                projectile.change_x = projectile_speed * self.player_sprite.facing_direction
                
                # Voltear la imagen si dispara hacia la izquierda
                if self.player_sprite.facing_direction < 0:
                    projectile.angle = 180
                    
                self.scene.add_sprite("Proyectiles", projectile)
                
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
        """Mueve la cámara suavemente siguiendo al jugador con estilo predictivo."""
        if not self.camera or not self.player_sprite:
            return
            
        # Offset predictivo (Katana Zero style): Mira un poco hacia adelante
        look_ahead = 0
        if self.player_sprite.change_x > 0:
            look_ahead = 150
        elif self.player_sprite.change_x < 0:
            look_ahead = -150
            
        # Apuntamos un poco arriba y hacia la dirección en la que nos movemos
        target_x = self.player_sprite.center_x + look_ahead
        target_y = self.player_sprite.center_y + 80
        
        # Evitar que la cámara muestre la zona fuera del mapa (coordenadas negativas)
        # Tomando en cuenta el zoom actual para calcular la visión real
        visible_width = self.camera.viewport_width / self.camera.zoom
        visible_height = self.camera.viewport_height / self.camera.zoom
        
        min_x = visible_width / 2
        min_y = visible_height / 2
        
        if target_x < min_x:
            target_x = min_x
        if target_y < min_y:
            target_y = min_y
            
        # Paneo dinámico suave usando lerp
        current_x, current_y = self.camera.position
        
        # 0.08 hace el movimiento un poco más "elástico/cinemático"
        new_x = arcade.math.lerp(current_x, target_x, 0.08)
        new_y = arcade.math.lerp(current_y, target_y, 0.08)
            
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
        
        # 3.5 Actualizar el on_update asíncrono del Jugador (Cooldowns e I-frames)
        self.player_sprite.on_update(delta_time)
        
        # 4. Actualizar lógica de entidades genéricas
        self.scene.update(delta_time, ["Player", "Enemigos", "Proyectiles"])
        
        # 4.5 Llamar on_update() de todos los proyectiles para chequeo de límites de mapa
        for proj in self.scene.get_sprite_list("Proyectiles"):
            proj.on_update(delta_time)
            
        # 4.6 Lógica de Enemigos (Patrullaje y Disparo)
        suelo_list = self.scene.get_sprite_list("Suelo")
        for enemy in self.scene.get_sprite_list("Enemigos"):
            # Desplazamiento horizontal del enemigo
            enemy.center_x += enemy.change_x
            
            # Chequeo predictivo de precipicios para no caer
            enemy.update_patrol(suelo_list)
            
            # Chequeo de visión y agresión hacia el jugador
            if enemy.check_and_shoot(self.player_sprite, delta_time):
                proj = Projectile(is_enemy_projectile=True)
                proj.center_x = enemy.center_x
                proj.center_y = enemy.center_y
                
                # Límites del nivel
                proj.limit_x_min = 0
                proj.limit_x_max = 10000
                proj.limit_y_min = LIMITE_CAIDA_Y
                
                # Calcular trayectoria en línea recta usando trigonometría
                dist_x = self.player_sprite.center_x - enemy.center_x
                dist_y = self.player_sprite.center_y - enemy.center_y
                angle = math.atan2(dist_y, dist_x)
                
                proj_speed = 7.0
                proj.change_x = math.cos(angle) * proj_speed
                proj.change_y = math.sin(angle) * proj_speed
                
                self.scene.add_sprite("Proyectiles", proj)
        
        # 5. Lógica de optimización de proyectiles (colisiones de entorno)
        for proj in self.scene.get_sprite_list("Proyectiles"):
            # Si el proyectil colisiona con el suelo, lo destruimos (self.kill)
            wall_hit_list = arcade.check_for_collision_with_list(proj, self.scene.get_sprite_list("Suelo"))
            if wall_hit_list:
                proj.kill()
                
        # 5.5 Lógica de Daño (Combate)
        proyectiles = self.scene.get_sprite_list("Proyectiles")
        enemigos = self.scene.get_sprite_list("Enemigos")
        
        for proj in proyectiles:
            if not proj.is_enemy_projectile:
                # Proyectil del jugador choca con enemigo
                enemigos_golpeados = arcade.check_for_collision_with_list(proj, enemigos)
                for enemigo in enemigos_golpeados:
                    enemigo.take_damage(1)
                    proj.kill()
            else:
                # Proyectil enemigo choca con el jugador
                if arcade.check_for_collision(proj, self.player_sprite):
                    self.player_sprite.take_damage(1)
                    proj.kill()
                    
        # 5.6 Condición de Victoria (Aparición de la Llave)
        if len(self.scene.get_sprite_list("Enemigos")) == 0 and not self.llave_spawned:
            self.llave_spawned = True
            llave = arcade.SpriteSolidColor(32, 32, arcade.color.GOLD)
            llave.center_x = 2400  # Más allá del muro
            llave.center_y = 64
            self.scene.add_sprite("Llave", llave)
            
        # 5.7 Colisión con la Llave (Ganar)
        if self.llave_spawned:
            if arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("Llave")):
                victory_view = GameOver(is_victory=True)
                self.window.show_view(victory_view)
                    
        # 6. ZONA DE MUERTE: Si el jugador cae al vacío
        if self.player_sprite.center_y < LIMITE_CAIDA_Y:
            self.setup()  # Reiniciar nivel limpiamente
            
        # 7. DERROTA: Si el HP del jugador llega a 0
        if self.player_sprite.hp <= 0:
            game_over_view = GameOver(is_victory=False)
            self.window.show_view(game_over_view)
