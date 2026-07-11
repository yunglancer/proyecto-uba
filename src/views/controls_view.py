import arcade
import arcade.gui
from src.views.main_menu import AnimatedButton

class ControlsView(arcade.View):
    """
    Pantalla dedicada a los Controles del juego (sin Lore).
    """
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=15)
        
        title = arcade.gui.UILabel(
            text="Controles del Juego",
            font_size=36,
            font_name=("Kenney Future", "Arial"),
            text_color=arcade.color.WHITE,
            bold=True
        )
        self.v_box.add(title)
        self.v_box.add(arcade.gui.UIWidget(height=30))
        
        controls_text = (
            "Movimiento:\n"
            "- A / D o Flechas Izq/Der: Correr\n"
            "- W o Espacio: Saltar\n"
            "- Doble Salto: Presiona saltar nuevamente en el aire\n\n"
            "Combate:\n"
            "- J, Z o Clic Izquierdo: Disparar Láser\n"
            "- Escudo Burbuja: Te protege de un impacto automáticamente"
        )
        controls_label = arcade.gui.UITextArea(
            text=controls_text,
            width=600,
            height=200,
            text_color=arcade.color.LIGHT_GRAY,
            font_size=18
        )
        self.v_box.add(controls_label)
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
