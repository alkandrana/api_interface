import sys
import csv
from pathlib import Path

from wses import load_config
from wses.library.api.batch_post.utils import transfer, batch_from_file
from wses.library.api.crud import post_record
from wses.library.api.scenes.scene import get_one_scene
from wses.library.dates import to_zulu, join_date

# 1. get sessions from log
def get_records_from_csv(path):
    if Path(path).exists():
        with open(path) as f:
            reader = csv.DictReader(f)
            records = [row for row in reader]
        print(f"Retrieved {len(records)} records from {path}")
        return records
    else:
        print("Could not find file.")
        sys.exit(1)
# 2. format sessions, accounting for variations in data
def format_local_session(ses):
    print("Fetching current scene ID:")
    scene_id = get_scene_id(ses["scene_id"])
    ses["start"] = join_date(ses["start"], ses["date"])
    ses["stop"] = join_date(ses["stop"], ses["date"])
    session = {
        "date": ses["date"],
        "startTime": to_zulu(ses["start"]) if ses["start"] else None,
        "stopTime": to_zulu(ses["stop"]) if ses["stop"] else None,
        "words": ses["words"],
        "sceneId": scene_id,
        "comments": ses["note"],
    }
    return session
#3. convert sessions to payload

#4 batch post to the api
# post_record(payload, "sessions")
def get_scene_id(code):
    if "-" in code:
        parts = code.split("-")
        project_code = parts[0]
        code = parts[1]
    res = get_one_scene(code)
    if 200 <= res.status_code < 300:
        scene = res.json()
        return scene["id"]
    else:
        print("An error occurred: ", res.status_code, res.reason)
        sys.exit(1)





def format_node_session(ses):
    scene_id = get_scene_id(ses["scene"]["code"])
    del (ses["scene"], ses["id"])
    ses["startTime"] = to_zulu(join_date(ses["startTime"], ses["date"]))
    ses["stopTime"] = to_zulu(join_date(ses["stopTime"], ses["date"]))
    ses["sceneId"] = scene_id
    return ses


def format_sessions(sessions, formatter):
    sessionlist = []
    for ses in sessions:
        # different between api and file
        session = formatter(ses)
        sessionlist.append(session)
    return sessionlist


def batch_sessions(args):
    if args.source == "api":
        transfer(args.path, "sessions", format_sessions)
    elif args.source == "file":
        sessions = get_records_from_csv(load_config()['log_file'])
        batch = []
        for s in sessions:
            batch.append(format_local_session(s))
        for p in batch:
            post_record(p, "sessions")
    else:
        print("Source must be one of 'api' or 'file'")
        sys.exit(1)


def parse_batch_sessions(sync_subparsers):
    session_parser = sync_subparsers.add_parser("sessions")
    session_parser.add_argument("--source", "-s", required=True)
    session_parser.set_defaults(func=batch_sessions)
