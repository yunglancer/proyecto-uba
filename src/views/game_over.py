import arcade
import arcade.gui
from src.views.main_menu import AnimatedButton

class GameOver(arcade.View):
    """
    Vista de final de partida.
    Se adapta visualmente dependiendo de si fue una victoria o derrota.
    Usa arcade.gui para botones interactivos.
    """
    
    def __init__(self, is_victory: bool = False):
        """
        Inicializa la vista adaptando el mensaje.
        
        Args:
            is_victory: True si recolectó la llave, False si HP llegó a cero.
        """
        super().__init__()
        self.is_victory = is_victory
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)
        
        # Título Dinámico
        title_text = "¡VICTORIA!" if self.is_victory else "¡INFECTADO!"
        title_color = arcade.color.WHITE
        title = arcade.gui.UILabel(
            text=title_text,
            font_size=48,
            font_name=("Kenney Future", "Arial"),
            text_color=title_color,
            bold=True
        )
        self.v_box.add(title)
        self.v_box.add(arcade.gui.UIWidget(height=30))
        
        # Subtítulo
        subtitle_text = (
            "¡Has repelido la invasión!" if self.is_victory 
            else "Los zombies te han destruido."
        )
        subtitle = arcade.gui.UILabel(
            text=subtitle_text,
            font_size=20,
            font_name=("Kenney Future", "Arial"),
            text_color=arcade.color.LIGHT_GRAY
        )
        self.v_box.add(subtitle)
        self.v_box.add(arcade.gui.UIWidget(height=50))
        
        # Botón Volver al Menú
        btn_menu = AnimatedButton(text="Volver al Menú Principal", width=300)
        btn_menu.on_click = self.on_click_menu
        self.v_box.add(btn_menu)
        
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )
        self.manager.add(anchor)

    def on_click_menu(self, event):
        from src.views.main_menu import MainMenu
        main_menu = MainMenu()
        self.window.show_view(main_menu)

    def on_show_view(self) -> None:
        """Configura el color de fondo según el resultado."""
        if self.is_victory:
            arcade.set_background_color(arcade.color.FOREST_GREEN)
        else:
            arcade.set_background_color(arcade.color.DARK_RED)
        self.manager.enable()
        
    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self) -> None:
        """Renderiza la UI en pantalla."""
        self.clear()
        self.manager.draw()
