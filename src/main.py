import globals

from keyboard_executor import KeyboardExecutor
from scripts_updater import ScriptsUpdater
from stray import StrayIcon
from lock_process import lock_process


@lock_process
def main():
    ScriptsUpdater().run()

    StrayIcon().run()

    KeyboardExecutor().run()

    while globals.is_running:
        pass


if __name__ == "__main__":
    main()
