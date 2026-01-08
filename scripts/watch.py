import bpy
import sys
import time
import subprocess
from os.path import dirname, join
from threading import Thread, Event

EXTENSION_NAME = "remove_static_fcurves"


def install_watchdog():
    import site
    site.addsitedir(site.getusersitepackages())

    try:
        import watchdog
        print("Watchdog ready")
        return
    except ImportError:
        # This can sometimes be brittle if python decides to use a different install location
        cmd = [sys.executable, '-m', 'pip', 'install', '--user', 'watchdog']
        print(" $ %s" % " ".join(cmd))
        subprocess.run(cmd, check=True)

        site.addsitedir(site.getusersitepackages())
        import watchdog


def watch(dir, on_file_change, extensions):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    print("Watching %s" % dir + " for file changes...")

    class ChangeHandler(FileSystemEventHandler):
        def __init__(self):
            super(ChangeHandler, self).__init__()
            self.has_update = False

        def on_any_event(self, event):
            source_path = event.src_path
            if source_path.endswith(extensions):
                self.has_update = True

        def clear_update(self):
            self.has_update = False

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, dir, recursive=True)
    observer.start()

    try:
        while observer.is_alive():
            time.sleep(1)
            if event_handler.has_update:
                on_file_change()
                event_handler.clear_update()
    except Exception as e:
        print(e)
    finally:
        observer.stop()
        observer.join()


def on_file_change():
    """Reload the extension"""
    import importlib

    try:
        print(f"\nReloading {EXTENSION_NAME}")

        # Unregister first
        if EXTENSION_NAME in sys.modules:
            module = sys.modules[EXTENSION_NAME]
            if hasattr(module, 'unregister'):
                print(f"  Unregistering {EXTENSION_NAME}")
                module.unregister()

        # Reload all extension modules
        modules_to_reload = [
            name for name in list(sys.modules.keys())
            if name.startswith(EXTENSION_NAME)
        ]
        modules_to_reload.sort()  # Reload parent modules before children

        for module_name in modules_to_reload:
            print(f"  Reloading: {module_name}")
            importlib.reload(sys.modules[module_name])

        # Re-register
        if EXTENSION_NAME in sys.modules:
            module = sys.modules[EXTENSION_NAME]
            if hasattr(module, 'register'):
                print(f"  Registering {EXTENSION_NAME}")
                module.register()

        print(f"{EXTENSION_NAME} reloaded successfully")

    except Exception as e:
        print(f"Error reloading {EXTENSION_NAME}: {e}")
        import traceback
        traceback.print_exc()


def start_watching():
    PROJECT_ROOT = dirname(dirname(__file__))
    SRC_DIR = join(PROJECT_ROOT, 'src')
    WATCH_EXT = ('.py', '.json')
    watch(SRC_DIR, on_file_change, WATCH_EXT)


if __name__ == '__main__':
    install_watchdog()
    keep_alive = Event()
    keep_alive.set()
    watch_thread = Thread(target=start_watching)
    watch_thread.daemon = True
    watch_thread.start()
