import subprocess
import re
from cfg import ENV_FILE


def update_env(new_env):
    with open(ENV_FILE, 'r') as file:
        data = file.read()
        data = re.sub("ENV = .*\n", f"ENV = \"{new_env}\"\n", data)

    with open(ENV_FILE, 'w') as file:
        file.write(data)


def build_package():
    subprocess.run(["mkdir", "-p", "build"])
    subprocess.run(["blender", "--command", "extension", "build",
                    "--source-dir", "src", "--output-dir", "build"])


update_env("PROD")
build_package()
update_env("DEV")
