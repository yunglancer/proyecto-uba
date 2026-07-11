import arcade
import arcade.gui
from src.views.main_menu import AnimatedButton

class SettingsView(arcade.View):
    """
    Pantalla dedicada a la Configuración (Placeholder visual).
    """
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=15)
        
        title = arcade.gui.UILabel(
            text="Configuración",
            font_size=36,
            font_name=("Kenney Future", "Arial"),
            text_color=arcade.color.WHITE,
            bold=True
        )
        self.v_box.add(title)
        self.v_box.add(arcade.gui.UIWidget(height=30))
        
        # Placeholder buttons
        btn_audio = AnimatedButton(text="Volumen General: 100%", width=300)
        self.v_box.add(btn_audio)
        
        # Botón dinámico de Pantalla Completa
        # Nota: window no está disponible en __init__, así que ponemos un texto base 
        # y lo actualizamos en on_show_view
        self.btn_video = AnimatedButton(text="Pantalla Completa", width=300)
        self.btn_video.on_click = self.on_click_fullscreen
        self.v_box.add(self.btn_video)
        self.v_box.add(arcade.gui.UIWidget(height=40))
        
        btn_back = AnimatedButton(text="Volver al Menú", width=300)
        btn_back.on_click = self.on_click_back
        self.v_box.add(btn_back)
        
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )
        self.manager.add(anchor)

    def on_show_view(self) -> None:
        arcade.set_background_color((15, 15, 20))
        
        # Actualizar texto según estado actual al abrir la vista
        estado = "Activado" if self.window.fullscreen else "Desactivado"
        self.btn_video.text = f"Pantalla Completa: {estado}"
        
        self.manager.enable()
        
    def on_click_fullscreen(self, event):
        """Alterna el modo Pantalla Completa."""
        is_fullscreen = not self.window.fullscreen
        self.window.set_fullscreen(is_fullscreen)
        
        estado = "Activado" if is_fullscreen else "Desactivado"
        self.btn_video.text = f"Pantalla Completa: {estado}"
        
    def on_hide_view(self):
        self.manager.disable()

    def on_click_back(self, event):
        from src.views.main_menu import MainMenu
        main_menu = MainMenu()
        self.window.show_view(main_menu)

    def on_draw(self) -> None:
        self.clear()
        self.manager.draw()
