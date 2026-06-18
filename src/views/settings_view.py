import arcade
import arcade.gui

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
            text_color=arcade.color.WHITE,
            bold=True
        )
        self.v_box.add(title)
        self.v_box.add(arcade.gui.UIWidget(height=30))
        
        # Placeholder buttons
        btn_audio = arcade.gui.UIFlatButton(text="Volumen General: 100%", width=300)
        self.v_box.add(btn_audio)
        
        btn_video = arcade.gui.UIFlatButton(text="Pantalla Completa: Desactivado", width=300)
        self.v_box.add(btn_video)
        self.v_box.add(arcade.gui.UIWidget(height=40))
        
        btn_back = arcade.gui.UIFlatButton(text="Volver al Menú", width=250)
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
        arcade.set_background_color(arcade.color.EERIE_BLACK)
        self.manager.enable()
        
    def on_hide_view(self):
        self.manager.disable()

    def on_click_back(self, event):
        from src.views.main_menu import MainMenu
        main_menu = MainMenu()
        self.window.show_view(main_menu)

    def on_draw(self) -> None:
        self.clear()
        self.manager.draw()
