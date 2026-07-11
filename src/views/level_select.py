import arcade
import arcade.gui
from src.views.main_menu import AnimatedButton
from src.views.game_view import GameView

class LevelSelect(arcade.View):
    """
    Pantalla dedicada para elegir el Nivel a jugar.
    """
    
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=15)
        
        # Título
        title = arcade.gui.UILabel(
            text="Selección de Nivel",
            font_size=36,
            font_name=("Kenney Future", "Arial"),
            text_color=arcade.color.WHITE,
            bold=True
        )
        self.v_box.add(title)
        self.v_box.add(arcade.gui.UIWidget(height=30))
        
        # Botones de Nivel
        btn_tut = AnimatedButton(text="Jugar Tutorial", width=300)
        btn_tut.on_click = lambda e: self.start_level(0)
        self.v_box.add(btn_tut)
        
        btn_lvl1 = AnimatedButton(text="Jugar Nivel 1", width=300)
        btn_lvl1.on_click = lambda e: self.start_level(1)
        self.v_box.add(btn_lvl1)
        
        btn_lvl2 = AnimatedButton(text="Jugar Nivel 2", width=300)
        btn_lvl2.on_click = lambda e: self.start_level(2)
        self.v_box.add(btn_lvl2)
        self.v_box.add(arcade.gui.UIWidget(height=40))
        
        # Volver
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

    def start_level(self, level_id: int):
        """Inicia el GameView usando el nivel indicado y la skin elegida globalmente."""
        skin = getattr(self.window, "current_skin", ":resources:images/animated_characters/robot/robot_idle.png")
        game_view = GameView(level=level_id, skin_path=skin)
        self.window.show_view(game_view)

    def on_change_level(self, event):
        pass # Reemplazado por los botones individuales

    def on_change_skin(self, event):
        pass # Removido

    def on_play(self, event):
        pass # Removido

    def on_click_back(self, event):
        from src.views.main_menu import MainMenu
        main_menu = MainMenu()
        self.window.show_view(main_menu)
        
    def on_show_view(self) -> None:
        arcade.set_background_color((15, 15, 20))
        self.manager.enable()
        
    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self) -> None:
        self.clear()
        self.manager.draw()
