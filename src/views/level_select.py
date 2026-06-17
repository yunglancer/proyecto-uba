import arcade
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.views.game_view import GameView

class LevelSelect(arcade.View):
    """
    Pantalla de selección de nivel y skin.
    Cumple con el flujo del MVP permitiendo elegir opciones no lineales.
    """
    
    def __init__(self):
        super().__init__()
        # Opciones disponibles
        self.levels = [1, 2]
        self.skins = [
            ":resources:images/animated_characters/robot/robot_idle.png",
            ":resources:images/animated_characters/zombie/zombie_idle.png"
        ]
        
        # Índices actuales
        self.current_level_idx = 0
        self.current_skin_idx = 0

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_draw(self) -> None:
        self.clear()
        
        # Título
        arcade.draw_text(
            "Selección de Nivel y Skin",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 100,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
            bold=True
        )
        
        # Selector de Nivel
        level_text = f"Nivel: {self.levels[self.current_level_idx]}"
        arcade.draw_text(
            f"<-  {level_text}  ->\n(Usa A/D o Flechas Izq/Der)",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            arcade.color.YELLOW,
            font_size=20,
            anchor_x="center",
            align="center",
            multiline=True,
            width=500
        )
        
        # Selector de Skin
        skin_name = "Estudiante (Robot)" if self.current_skin_idx == 0 else "Estudiante Trasnochado (Zombie)"
        arcade.draw_text(
            f"Skin: {skin_name}\n(Usa W/S o Flechas Arr/Aba)",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.CYAN,
            font_size=20,
            anchor_x="center",
            align="center",
            multiline=True,
            width=500
        )
        
        # Instrucción para iniciar
        arcade.draw_text(
            "Presiona [ENTER] para Jugar",
            SCREEN_WIDTH / 2,
            100,
            arcade.color.LIGHT_GREEN,
            font_size=24,
            anchor_x="center",
            bold=True
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Maneja la selección del menú mediante teclas."""
        # Cambio de Nivel (Izquierda / Derecha)
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.current_level_idx = (self.current_level_idx - 1) % len(self.levels)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.current_level_idx = (self.current_level_idx + 1) % len(self.levels)
            
        # Cambio de Skin (Arriba / Abajo)
        elif key == arcade.key.UP or key == arcade.key.W:
            self.current_skin_idx = (self.current_skin_idx - 1) % len(self.skins)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.current_skin_idx = (self.current_skin_idx + 1) % len(self.skins)
            
        # Confirmar e iniciar el GameView
        elif key == arcade.key.ENTER or key == arcade.key.RETURN:
            selected_level = self.levels[self.current_level_idx]
            selected_skin = self.skins[self.current_skin_idx]
            
            game_view = GameView(level=selected_level, skin_path=selected_skin)
            self.window.show_view(game_view)
