import arcade
import arcade.gui

class AnimatedButton(arcade.gui.UIFlatButton):
    def __init__(self, text="", width=300, height=50, **kwargs):
        super().__init__(text=text, width=width, height=height, **kwargs)
        self.clear()  # Elimina el UILabel interno para evitar el texto doble
        
    def do_render(self, surface: arcade.gui.Surface):
        self.prepare_render(surface)
        
        # Limpiar el fondo con transparencia
        surface.clear(arcade.color.TRANSPARENT_BLACK)
        
        # Determinar estado y offset
        # Estado presionado: el botón baja.
        # Estado hover: el botón se ilumina.
        if self.pressed:
            bg_color = (41, 128, 185)      # Azul más oscuro
            shadow_color = (31, 97, 141)
            bottom_offset = 0              # Baja al nivel del suelo
        elif self.hovered:
            bg_color = (93, 173, 226)      # Azul claro iluminado
            shadow_color = (31, 97, 141)
            bottom_offset = 6              # Se levanta ligeramente
        else:
            bg_color = (52, 152, 219)      # Azul estándar
            shadow_color = (31, 97, 141)
            bottom_offset = 4              # Altura normal

        rect_height = self.height - 6      # Altura del botón visual

        # 1. Dibujar sombra (siempre en la parte inferior)
        if bottom_offset > 0:
            arcade.draw_lbwh_rectangle_filled(
                0, 0, 
                self.width, rect_height, 
                shadow_color
            )

        # 2. Dibujar el cuerpo del botón
        arcade.draw_lbwh_rectangle_filled(
            0, bottom_offset, 
            self.width, rect_height, 
            bg_color
        )
        
        # 3. Dibujar borde si está en hover (para resaltarlo más)
        if self.hovered and not self.pressed:
            arcade.draw_lbwh_rectangle_outline(
                0, bottom_offset, 
                self.width, rect_height, 
                arcade.color.WHITE, 
                border_width=2
            )

        # 4. Dibujar texto centrado en el cuerpo del botón
        text_y = bottom_offset + (rect_height / 2)
        text = arcade.Text(
            self.text,
            self.width / 2,
            text_y,
            arcade.color.WHITE,
            font_size=16,
            font_name=("Arial", "sans-serif"),
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        text.draw()

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
        btn_play = AnimatedButton(text="Jugar", width=300)
        btn_play.on_click = self.on_click_play
        self.v_box.add(btn_play)
        
        btn_char = AnimatedButton(text="Selección de Personaje", width=300)
        btn_char.on_click = self.on_click_char
        self.v_box.add(btn_char)
        
        btn_controls = AnimatedButton(text="Controles", width=300)
        btn_controls.on_click = self.on_click_controls
        self.v_box.add(btn_controls)
        
        btn_settings = AnimatedButton(text="Configuración", width=300)
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
