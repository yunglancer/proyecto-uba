import arcade
import arcade.gui

# Estilo global de madera para los botones (basado en la imagen de referencia)
WOOD_STYLE = {
    "normal": {
        "font_name": ("Arial", "calibri"),
        "font_size": 18,
        "font_color": arcade.color.WHITE,
        "border_width": 3,
        "border_color": (50, 25, 10),  # Marrón muy oscuro
        "bg_color": (160, 82, 45),     # Sienna / Madera clara
    },
    "hover": {
        "font_name": ("Arial", "calibri"),
        "font_size": 18,
        "font_color": arcade.color.WHITE,
        "border_width": 3,
        "border_color": (50, 25, 10),
        "bg_color": (205, 133, 63),    # Madera resaltada
    },
    "press": {
        "font_name": ("Arial", "calibri"),
        "font_size": 18,
        "font_color": arcade.color.WHITE,
        "border_width": 3,
        "border_color": arcade.color.WHITE,
        "bg_color": (101, 67, 33),     # Madera oscura
    }
}

class MainMenu(arcade.View):
    """
    Pantalla inicial del juego, refactorizada para flujo de menús múltiples y 
    estilizada según el concepto visual.
    """
    
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        # Contenedor vertical principal
        self.v_box = arcade.gui.UIBoxLayout(space_between=15)
        
        # Título principal
        title_label = arcade.gui.UILabel(
            text="- UBA -",
            font_size=50,
            text_color=arcade.color.WHITE,
            bold=True
        )
        self.v_box.add(title_label)
        
        subtitle_label = arcade.gui.UILabel(
            text="Combate de Sumativas",
            font_size=40,
            text_color=arcade.color.WHITE,
            bold=True
        )
        self.v_box.add(subtitle_label)
        self.v_box.add(arcade.gui.UIWidget(height=40))
        
        # Botones con estilo personalizado
        btn_play = arcade.gui.UIFlatButton(text="Jugar", width=300, style=WOOD_STYLE)
        btn_play.on_click = self.on_click_play
        self.v_box.add(btn_play)
        
        btn_char = arcade.gui.UIFlatButton(text="Selección de Personaje", width=300, style=WOOD_STYLE)
        btn_char.on_click = self.on_click_char
        self.v_box.add(btn_char)
        
        btn_controls = arcade.gui.UIFlatButton(text="Controles", width=300, style=WOOD_STYLE)
        btn_controls.on_click = self.on_click_controls
        self.v_box.add(btn_controls)
        
        btn_settings = arcade.gui.UIFlatButton(text="Configuración", width=300, style=WOOD_STYLE)
        btn_settings.on_click = self.on_click_settings
        self.v_box.add(btn_settings)
        
        # Panel de fondo oscuro translúcido detrás de los botones
        bg_panel = arcade.gui.UISpace(
            width=400, height=450, color=(30, 40, 50, 200) # Simula la "pizarra" oscura
        )
        
        # Posicionamos el VBox encima del panel
        self.panel_layout = arcade.gui.UIAnchorLayout()
        self.panel_layout.add(bg_panel, anchor_x="center_x", anchor_y="center_y")
        self.panel_layout.add(self.v_box, anchor_x="center_x", anchor_y="center_y")
        
        self.manager.add(self.panel_layout)

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
        # Color temporal simulando el cielo de atardecer
        arcade.set_background_color((214, 150, 110)) 
        self.manager.enable()

    def on_hide_view(self):
        """Se ejecuta al salir de esta vista."""
        self.manager.disable()

    def on_draw(self) -> None:
        """Renderiza la pantalla de menú y los widgets GUI."""
        self.clear()
        
        # Aquí podrías dibujar un background_sprite de la universidad en el futuro:
        # if hasattr(self, 'background_sprite'):
        #     self.background_sprite.draw()
            
        self.manager.draw()
