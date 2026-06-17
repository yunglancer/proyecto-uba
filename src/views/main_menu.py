import arcade
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu(arcade.View):
    """
    Pantalla inicial del juego.
    Muestra el título, la premisa (Lore) y los controles básicos (Tutorial).
    """
    
    def on_show_view(self) -> None:
        """Se ejecuta al mostrar la vista por primera vez."""
        arcade.set_background_color(arcade.color.UBA_BLUE if hasattr(arcade.color, "UBA_BLUE") else arcade.color.DARK_MIDNIGHT_BLUE)

    def on_draw(self) -> None:
        """Renderiza la pantalla de menú."""
        self.clear()
        
        # Título del juego
        arcade.draw_text(
            "UBA - Combate de Sumativas",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 150,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
            bold=True
        )
        
        # Lore / Premisa
        lore_text = (
            "Eres un estudiante de ingeniería armado con un lápiz mágico.\n"
            "Las evaluaciones (Sumativas) han cobrado vida en formato de papel.\n"
            "¡Sobrevive a las ecuaciones matemáticas y llega hasta el final!"
        )
        arcade.draw_text(
            lore_text,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 300,
            arcade.color.LIGHT_GRAY,
            font_size=18,
            anchor_x="center",
            align="center",
            multiline=True,
            width=800
        )
        
        # Controles (Tutorial)
        controls_text = (
            "[ CONTROLES ]\n\n"
            "A / D o Flechas: Moverse\n"
            "W o Espacio: Saltar (Presiona en el aire para Doble Salto)\n"
            "Nota: Tu Escudo Burbuja te protege de un impacto."
        )
        arcade.draw_text(
            controls_text,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 480,
            arcade.color.YELLOW,
            font_size=16,
            anchor_x="center",
            align="center",
            multiline=True,
            width=600
        )
        
        # Instrucción para avanzar
        arcade.draw_text(
            "Presiona [ENTER] para Continuar",
            SCREEN_WIDTH / 2,
            100,
            arcade.color.CYAN,
            font_size=24,
            anchor_x="center",
            bold=True
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Maneja los inputs en el menú."""
        if key == arcade.key.ENTER or key == arcade.key.RETURN:
            # Aquí importamos y llamamos a LevelSelect
            from src.views.level_select import LevelSelect
            level_select_view = LevelSelect()
            self.window.show_view(level_select_view)
