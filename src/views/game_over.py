import arcade
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.views.main_menu import MainMenu

class GameOver(arcade.View):
    """
    Vista de final de partida.
    Se adapta visualmente dependiendo de si fue una victoria o derrota.
    """
    
    def __init__(self, is_victory: bool = False):
        """
        Inicializa la vista adaptando el mensaje.
        
        Args:
            is_victory: True si recolectó la llave, False si HP llegó a cero.
        """
        super().__init__()
        self.is_victory = is_victory

    def on_show_view(self) -> None:
        """Configura el color de fondo según el resultado."""
        if self.is_victory:
            arcade.set_background_color(arcade.color.FOREST_GREEN)
        else:
            arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self) -> None:
        """Renderiza los mensajes en pantalla."""
        self.clear()
        
        # Textos dinámicos
        title = "¡APROBASTE!" if self.is_victory else "¡REPROBASTE!"
        subtitle = (
            "Lograste sobrevivir al semestre." if self.is_victory 
            else "Las sumativas de la UBA te han vencido."
        )
        
        arcade.draw_text(
            title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            arcade.color.WHITE,
            font_size=60,
            anchor_x="center",
            bold=True
        )
        
        arcade.draw_text(
            subtitle,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 30,
            arcade.color.LIGHT_GRAY,
            font_size=20,
            anchor_x="center",
            align="center"
        )
        
        arcade.draw_text(
            "Presiona [ENTER] para volver al Menú Principal",
            SCREEN_WIDTH / 2,
            100,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Reinicia el flujo retornando al Menú Principal."""
        if key == arcade.key.ENTER or key == arcade.key.RETURN:
            main_menu = MainMenu()
            self.window.show_view(main_menu)
