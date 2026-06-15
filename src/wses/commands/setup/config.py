from pathlib import Path
import os, json, sys
from ..file.search import find_file


def get_store_path() -> Path:
    # Prefer XDG_STATE_HOME; fallback to ~/.local/state; then ~/.wlogs if needed.
    xdg_state = os.getenv("XDG_STATE_HOME")
    if xdg_state:
        root = Path(xdg_state)
    else:
        root = Path.home() / ".local" / "state"

    path = root / "wlogs"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def set_log_file(_):
    log = input("Enter the name of your writing sessions log file: ")
    log_path = find_file(log)
    config_file = get_store_path() / "config.json"
    if log_path.exists():
        with open(config_file, "r") as f:
            config = json.load(f)
        config["log_file"] = log
        with open(config_file, "w") as f:
            json.dump(config, f)
        print(f"Log path written to {config_file}")
    else:
        print("Log file could not be found. Check your spelling and try again.")
        sys.exit(1)


def parse_config(subparsers):
    config_parser = subparsers.add_parser("config")
    config_subparsers = config_parser.add_subparsers(dest="subcommand")
    log_parser = config_subparsers.add_parser("log")
    log_parser.set_defaults(func=set_log_file)
