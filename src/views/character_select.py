import arcade
import arcade.gui

class CharacterSelect(arcade.View):
    """
    Pantalla dedicada a la selección de personaje.
    Actualiza la variable window.current_skin.
    """
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=15)
        
        # Título
        title = arcade.gui.UILabel(
            text="Selección de Personaje",
            font_size=36,
            text_color=arcade.color.WHITE,
            bold=True
        )
        self.v_box.add(title)
        self.v_box.add(arcade.gui.UIWidget(height=30))
        
        # Label de estado
        self.status_label = arcade.gui.UILabel(
            text="Personaje Actual: Robot",
            font_size=20,
            text_color=arcade.color.YELLOW
        )
        self.v_box.add(self.status_label)
        self.v_box.add(arcade.gui.UIWidget(height=20))
        
        # Botones de Skin
        btn_robot = arcade.gui.UIFlatButton(text="Elegir Robot", width=250)
        btn_robot.on_click = self.on_click_robot
        self.v_box.add(btn_robot)
        
        btn_zombie = arcade.gui.UIFlatButton(text="Elegir Zombie", width=250)
        btn_zombie.on_click = self.on_click_zombie
        self.v_box.add(btn_zombie)
        self.v_box.add(arcade.gui.UIWidget(height=40))
        
        # Volver
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

    def update_status(self):
        # Protegernos en caso de que aún no exista la variable
        skin = getattr(self.window, "current_skin", "robot")
        if "robot" in skin:
            self.status_label.text = "Personaje Actual: Robot"
        else:
            self.status_label.text = "Personaje Actual: Zombie"

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()
        self.update_status()
        
    def on_hide_view(self):
        self.manager.disable()

    def on_click_robot(self, event):
        self.window.current_skin = ":resources:images/animated_characters/robot/robot_idle.png"
        self.update_status()
        
    def on_click_zombie(self, event):
        self.window.current_skin = ":resources:images/animated_characters/zombie/zombie_idle.png"
        self.update_status()

    def on_click_back(self, event):
        from src.views.main_menu import MainMenu
        main_menu = MainMenu()
        self.window.show_view(main_menu)

    def on_draw(self) -> None:
        self.clear()
        self.manager.draw()
