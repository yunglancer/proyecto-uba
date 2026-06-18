import arcade
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from src.views.main_menu import MainMenu

def main() -> None:
    """Función principal de entrada del programa."""
    # Inicializamos la ventana usando nuestras constantes
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    # Variables globales del juego a nivel de ventana
    window.current_skin = ":resources:images/animated_characters/robot/robot_idle.png"  # type: ignore
    
    # Cargamos el Menú Principal (Inicio del flujo MVP)
    start_view = MainMenu()
    window.show_view(start_view)
    
    # Iniciamos el bucle principal del juego
    arcade.run()

if __name__ == "__main__":
    main()
