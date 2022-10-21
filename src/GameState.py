from Enums import ScreenCodes
import json
import tkinter as tk
from tkinter import filedialog
import datetime


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

    # Yeah...this is not great, but it works.
    @classmethod
    def create_player(cls):
        print("Creating user")

        global name
        name = "unnamed player"

        # Destroys the tkinter window and assigns the name
        def destroy_tkinter_window(root, name_ent):
            global name
            name = name_ent.get()

            root.destroy()

        # Create a tkinter window to get the name
        # TODO: Refactor the nested functions
        def tkinter_ask():
            root = tk.Tk()
            root.title("Create user")

            tk.Label(root, text="Create a new user").grid(row=0, column=0, columnspan=2)
            tk.Label(root, text="Username: ").grid(row=1, column=0)

            name_ent = tk.Entry(root, width=15, borderwidth=2, relief="groove")
            name_ent.grid(row=1, column=1)

            save_btn = tk.Button(root, text="Create", width=20, borderwidth=2, relief="groove")
            save_btn["command"] = lambda: destroy_tkinter_window(root, name_ent)
            save_btn.grid(row=2, column=0, columnspan=2)

            root.mainloop()

        tkinter_ask()

        # Create the save file, and set the info

        cls.PLAYER_NAME = name
        cls.set_save_file()

        cls.select_player()

    @classmethod
    def set_save_file(cls):
        # Player name is required to be set. the other fields van have defaults,.
        save_file = {
            "player_name": cls.PLAYER_NAME,
            "player_speed": cls.PLAYER_SPEED or 15,
            "player_lives": cls.PLAYER.STARTING_LIVES if cls.PLAYER else 5,
            "player_pulse_speed": cls.PLAYER.pulse_speed if cls.PLAYER else 250,
            "created_at": cls.SAVE_CREATED_AT or cls.__get_datestamp(),
            "batteries": int(cls.PLAYER.batteries) if cls.PLAYER else 0,
            "top_score": cls.TOP_SCORE or 0
        }

        with open(f"saves/{cls.PLAYER_NAME}.json", 'w+') as handle:
            save = json.dumps(save_file, indent=4)
            handle.write(save)

    @classmethod
    def get_save_file_info(cls, filename):
        with open(filename, 'r') as handle:
            content = handle.read()

        return json.loads(content)

    @classmethod
    def set_screen(cls, screencode):
        if cls.SCREEN_CODE == ScreenCodes.BA:
            cls.ENEMY.thread.cancel()

        cls.SCREEN_CODE = screencode

    @staticmethod
    def __get_datestamp():
        now = datetime.datetime.now()
        return f"{now.day}/{now.month}/{now.year}"

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
