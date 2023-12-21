from threading import Thread
import json
from time import sleep
import globals


def read_and_decode_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


class ScriptsUpdater:
    def __init__(self):
        pass

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(ScriptsUpdater, self).__new__(self)
        return self.instance

    def run(self):
        daemon = Thread(target=self.__update_scripts,
                        daemon=True, name='BackgroundRead')
        daemon.start()

    def __update_scripts(self):
        while True:
            globals.scripts = read_and_decode_json("scripts.txt")
            sleep(3)
