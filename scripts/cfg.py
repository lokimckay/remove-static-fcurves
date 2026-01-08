import yaml
from platformdirs import user_data_dir
from os.path import dirname, join, exists

# Paths
PROJECT_ROOT = dirname(dirname(__file__))
APPDATA_DIR = user_data_dir(
    "Blender", "Blender Foundation", roaming=True)

# Load yaml config
CFG_PATH = join(PROJECT_ROOT, "config.yml")
with open(CFG_PATH, 'r') as stream:
    cfg = yaml.safe_load(stream)

# Config
ADDON_NAME = cfg["addon_name"]
BLENDER_VERSION = cfg["blender_version"]
BLENDER_DATA_HOME = cfg["blender_data_home"] or join(
    APPDATA_DIR, str(BLENDER_VERSION))

# Binary
BLENDER_BINARY = cfg["blender_binary"] or "blender"

# Symlinking
SRC_DIR = join(PROJECT_ROOT, 'src', ADDON_NAME)
if not exists(SRC_DIR):
    SRC_DIR = join(PROJECT_ROOT, 'src')
ADDON_DIR = join(BLENDER_DATA_HOME, 'scripts', 'addons', ADDON_NAME)

# Env
ENV_FILE = join(SRC_DIR, "env.py")
