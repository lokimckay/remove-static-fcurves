import subprocess
from cfg import SRC_DIR, ADDON_DIR, ADDON_NAME, BLENDER_BINARY


def symlink():
    import os

    # Ensure intermediate directories exist
    parent_dir = os.path.dirname(ADDON_DIR)
    os.makedirs(parent_dir, exist_ok=True)

    # Remove existing file/symlink/dir at target
    if os.path.exists(ADDON_DIR) or os.path.islink(ADDON_DIR):
        os.remove(ADDON_DIR)

    os.symlink(SRC_DIR, ADDON_DIR)
    print(f"Symlinked {SRC_DIR} to {ADDON_DIR}")


def start_blender():
    cmd = [BLENDER_BINARY, "scripts/dev.blend", "--addons", ADDON_NAME,
           "--no-window-focus", "-P", "scripts/watch.py"]
    print("$ %s" % " ".join(cmd))
    subprocess.run(cmd)


if __name__ == '__main__':
    symlink()
    start_blender()
