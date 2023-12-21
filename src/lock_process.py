import portalocker

import sys
import os
import tempfile


def lock_process(func):
    def wrapper():
        def create_lock_file():
            lock_file_path = os.path.join(
                tempfile.gettempdir(), "smart_keyboard_background.lock")
            lock_file = open(lock_file_path, "w")
            try:
                portalocker.lock(
                    lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
                return lock_file, lock_file_path
            except:
                return None, lock_file_path

        lock_file, lock_file_path = create_lock_file()
        if not lock_file:
            print("Another instance is already running. Exiting.")
            sys.exit(1)

        try:
            # Program logic
            func()
        finally:
            # Release the lock and delete the lock file
            portalocker.unlock(lock_file)
            lock_file.close()
            os.remove(lock_file_path)
    return wrapper
