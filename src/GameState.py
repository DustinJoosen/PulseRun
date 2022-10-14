from Enums import ScreenCodes
import json


class GameState:

    SCREEN_CODE = ScreenCodes.BA
    RUNNING = True

    PLAYER = None

    PLAYER_SPEED = None
    PLAYER_NAME = None

    ENEMY = None

    BATTERY = None

    SAVE_CREATED_AT = None
    TOP_SCORE = None

    @classmethod
    def init(cls):
        info = cls.get_save_file_info()

        cls.PLAYER.STARTING_LIVES = info["player_lives"]
        cls.PLAYER.lives = info["player_lives"]
        cls.PLAYER.batteries = info["batteries"]
        cls.PLAYER.pulse_speed = info["player_pulse_speed"]

        cls.PLAYER_SPEED = info["player_speed"]
        cls.PLAYER_NAME = info["player_name"]
        cls.SAVE_CREATED_AT = info["created_at"]
        cls.TOP_SCORE = info["top_score"]

        print("Gamestate initialized")
        print(f"Welcome {cls.PLAYER_NAME}!")

    @classmethod
    def set_save_file(cls):
        save_file = {
            "player_name": cls.PLAYER_NAME,
            "player_speed": cls.PLAYER_SPEED,
            "player_lives": cls.PLAYER.STARTING_LIVES,
            "player_pulse_speed": cls.PLAYER.pulse_speed,
            "created_at": cls.SAVE_CREATED_AT,
            "batteries": int(cls.PLAYER.batteries),
            "top_score": cls.TOP_SCORE
        }

        with open("saves/syter6.json", 'w') as handle:
            save = json.dumps(save_file, indent=4)
            handle.write(save)

    @classmethod
    def get_save_file_info(cls):
        with open("saves/syter6.json", 'r') as handle:
            content = handle.read()

        return json.loads(content)

    @classmethod
    def create_save_file(cls):
        pass

    @classmethod
    def print_save_information(cls):
        info = cls.get_save_file_info()
        print(f"Player name: {info['player_name']}")
        print(f"Player speed: {info['player_speed']}")
        print(f"Player lives: {info['player_lives']}")
        print(f"Player pulse speed: {info['player_pulse_speed']}")
        print(f"Created at: {info['created_at']}")
        print(f"Batteries: {info['batteries']}")
        print(f"Topscore: {info['top_score']}")
