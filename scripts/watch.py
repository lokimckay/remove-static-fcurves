import bpy
import sys
import time
import subprocess
from os.path import dirname, join
from threading import Thread, Event


def install_watchdog():
    try:
        import watchdog
        print("Watchdog ready")
        return
    except:
        # This can sometimes be brittle if python decides to use a different install location
        cmd = [sys.executable, '-m', 'pip', 'install', 'watchdog']
        print(" $ %s" % " ".join(cmd))
        subprocess.run(cmd)


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
    bpy.ops.script.reload()


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
