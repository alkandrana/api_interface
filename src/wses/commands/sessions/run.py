import csv
from datetime import datetime
from pathlib import Path
from ..utils import to_zulu
from .create_session import get_scene_id, post_session
import sys, os, json

def initialize(scene):
    session_data = {
        "date": datetime.strftime(datetime.today(), "%Y-%m-%d"),
        "start_time": datetime.strftime(
            datetime.now(),
            '%Y-%m-%dT%H:%M:%S'
        ),
        "scene": scene
    }
    return session_data
def tmp_save(data):
    path = Path(os.getenv("TMP_PATH"))
    if path.exists():
        print(f"Session already running.")
        sys.exit(1)
    else:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)


def build_session(words):
    path = Path(os.getenv("TMP_PATH"))
    if path.exists():
        with open(path, "r") as f:
            data = json.load(f)
        if not "stop_time" in data:
            data["stop_time"] = (
                    datetime.strftime(
                        datetime.now(),
                        "%Y-%m-%dT%H:%M:%S"
                    )
                )
        data["words"] = words
    else:
        print("No session running.")
        sys.exit(1)
    return data

def get_next_id():
    path = Path(os.getenv("LOG_FILE"))
    if path.exists():
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                id = int(row["session_id"])
        return id
    else:
        print("Log file not found.")
        sys.exit(1)
def save_local(data):
    path = Path(os.getenv("LOG_FILE"))
    id = get_next_id()
    csv_str = f"{id},{data['date']},{data['start_time']},{data['stop_time']},{data['scene']},{data['words']},\n"
    if path.exists():
        with open(path, "a") as f:
            f.write(csv_str)
        print(f"Session saved to {path}")
    else:
        print("Log file not found.")
        sys.exit(1)

def convert_to_session(data):
    code = data["scene"].split("-")[1]
    scene_id = get_scene_id(code)
    return {
        "date": data["date"],
        "startTime": to_zulu(data["start_time"]),
        "stopTime": to_zulu(data["stop_time"]),
        "words": data["words"],
        "sceneId": scene_id
    }

def start(args):
    data = initialize(args.scene)
    tmp_save(data)
    print("Session started: ")
    for key, value in data.items():
        print(f"{key}: {value}")
def stop(args):
    data = build_session(args.words)
    print("Session to save: ", data)
    save_local(data)
    session = convert_to_session(data)
    post_session(session)
    path = Path(os.getenv("TMP_PATH"))
    path.unlink(missing_ok=True)
    print("Session saved")

def cancel(_):
    path = Path(os.getenv("TMP_PATH"))
    if path.exists():
        with open(path, "r") as f:
            data = json.load(f)
        path.unlink()
        print("Session cancelled: ")
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("No session running.")

def parse_run_session(session_subparsers):
    run_parser = session_subparsers.add_parser("run")
    run_subparsers = run_parser.add_subparsers(dest="sub2command")

    start_parser = run_subparsers.add_parser("start")
    start_parser.add_argument("--scene", "-s", help="Scene Code")
    start_parser.set_defaults(func=start)

    stop_parser = run_subparsers.add_parser("stop")
    stop_parser.add_argument("--words", "-w", help="Words Written")
    stop_parser.set_defaults(func=stop)

    cancel_parser = run_subparsers.add_parser("cancel")
    cancel_parser.set_defaults(func=cancel)
