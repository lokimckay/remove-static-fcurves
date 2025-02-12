import subprocess
import re
from cfg import ENV_FILE


def build_package():
    subprocess.run(["mkdir", "-p", "build"])
    subprocess.run(["blender", "--command", "extension", "build",
                    "--source-dir", "src", "--output-dir", "build"])


build_package()
