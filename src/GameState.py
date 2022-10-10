from ScreenCodes import ScreenCodes


class GameState:

    SCREEN_CODE = ScreenCodes.BA
    RUNNING = True

    PLAYER = None
    PLAYER_SPEED = 2

    ENEMY = None

    @classmethod
    def init(cls):
        print("Gamestate initialized")

    @classmethod
    def set_save_file(cls):
        pass

    @classmethod
    def get_save_file_info(cls):
        return None

    @classmethod
    def create_save_file(cls):
        pass
