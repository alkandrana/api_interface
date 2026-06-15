from ..setup.config import get_store_path
import json
import sys


def load_config():
    config_path = get_store_path() / "config.json"
    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    else:
        print("Config could not be found. Set it up with 'wlogs config'.")
        sys.exit(1)
