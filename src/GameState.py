from Enums import ScreenCodes
import json
import tkinter as tk
from tkinter import filedialog


class GameState:

    SCREEN_CODE = ScreenCodes.MA
    RUNNING = True

    PLAYER = None

    PLAYER_SPEED = None
    PLAYER_NAME = None

    ENEMY = None

    BATTERY = None

    SAVE_CREATED_AT = None
    TOP_SCORE = None

    INIT_BATTLE = lambda: print("method not declared yet")

    @classmethod
    def exit(cls):
        cls.RUNNING = False

    @classmethod
    def select_player(cls):
        if cls.PLAYER_NAME is None:
            root = tk.Tk()
            root.withdraw()

            filename = filedialog.askopenfilename()
            info = cls.get_save_file_info(filename)

            cls.PLAYER_NAME = info["player_name"]
        else:
            info = cls.get_save_file_info(f"saves/{cls.PLAYER_NAME}.json")

        cls.INIT_BATTLE()

        cls.PLAYER.STARTING_LIVES = info["player_lives"]
        cls.PLAYER.lives = info["player_lives"]
        cls.PLAYER.batteries = info["batteries"]
        cls.PLAYER.pulse_speed = info["player_pulse_speed"]

        cls.PLAYER_SPEED = info["player_speed"]
        cls.SAVE_CREATED_AT = info["created_at"]
        cls.TOP_SCORE = info["top_score"]

        print("Welcome " + cls.PLAYER_NAME)
        cls.SCREEN_CODE = ScreenCodes.BA

    @classmethod
    def create_player(cls):
        print("Creating user")

        user = None
        cls.select_player()

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

        with open(f"saves/{cls.PLAYER_NAME}.json", 'w') as handle:
            save = json.dumps(save_file, indent=4)
            handle.write(save)

    @classmethod
    def get_save_file_info(cls, filename):
        with open(filename, 'r') as handle:
            content = handle.read()

        return json.loads(content)

    # @classmethod
    # def print_save_information(cls):
    #     info = cls.get_save_file_info()
    #     print(f"Player name: {info['player_name']}")
    #     print(f"Player speed: {info['player_speed']}")
    #     print(f"Player lives: {info['player_lives']}")
    #     print(f"Player pulse speed: {info['player_pulse_speed']}")
    #     print(f"Created at: {info['created_at']}")
    #     print(f"Batteries: {info['batteries']}")
    #     print(f"Topscore: {info['top_score']}")
