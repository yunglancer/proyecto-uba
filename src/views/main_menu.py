import arcade
import arcade.gui

class MainMenu(arcade.View):
    """
    Pantalla inicial del juego, refactorizada para flujo de menús múltiples.
    """
    
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=15)
        
        # Título
        title_label = arcade.gui.UILabel(
            text="UBA - Combate de Sumativas",
            font_size=40,
            text_color=arcade.color.WHITE,
            bold=True
        )
        self.v_box.add(title_label)
        self.v_box.add(arcade.gui.UIWidget(height=40))
        
        # Botón Jugar
        btn_play = arcade.gui.UIFlatButton(text="Jugar", width=250)
        btn_play.on_click = self.on_click_play
        self.v_box.add(btn_play)
        
        # Botón Personaje
        btn_char = arcade.gui.UIFlatButton(text="Selección de Personaje", width=250)
        btn_char.on_click = self.on_click_char
        self.v_box.add(btn_char)
        
        # Botón Controles
        btn_controls = arcade.gui.UIFlatButton(text="Controles", width=250)
        btn_controls.on_click = self.on_click_controls
        self.v_box.add(btn_controls)
        
        # Botón Configuración
        btn_settings = arcade.gui.UIFlatButton(text="Configuración", width=250)
        btn_settings.on_click = self.on_click_settings
        self.v_box.add(btn_settings)
        
        # Añadir el VBox al manager centrado en pantalla
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )
        self.manager.add(anchor)

    def on_click_play(self, event):
        from src.views.level_select import LevelSelect
        level_select_view = LevelSelect()
        self.window.show_view(level_select_view)
        
    def on_click_char(self, event):
        from src.views.character_select import CharacterSelect
        self.window.show_view(CharacterSelect())
        
    def on_click_controls(self, event):
        from src.views.controls_view import ControlsView
        self.window.show_view(ControlsView())
        
    def on_click_settings(self, event):
        from src.views.settings_view import SettingsView
        self.window.show_view(SettingsView())

    def on_show_view(self) -> None:
        """Se ejecuta al mostrar la vista por primera vez."""
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)
        self.manager.enable()

    def on_hide_view(self):
        """Se ejecuta al salir de esta vista."""
        self.manager.disable()

    def on_draw(self) -> None:
        """Renderiza la pantalla de menú y los widgets GUI."""
        self.clear()
        self.manager.draw()
