import sys
from datetime import datetime
from .utils import transfer, batch_from_file
from ..scenes.scene import get_one_scene
from wses.library.dates import to_zulu, join_date


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


def format_local_session(ses):
    print("Fetching current scene ID:")
    scene_id = get_scene_id(ses["scene_id"])
    ses["start"] = join_date(ses["start"], ses["date"])
    ses["stop"] = join_date(ses["stop"], ses["date"])
    session = {
        "date": ses["date"],
        "startTime": to_zulu(ses["start"]),
        "stopTime": to_zulu(ses["stop"]),
        "words": ses["words"],
        "sceneId": scene_id,
        "comments": ses["note"],
    }
    return session


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
        batch_from_file(args.path, "sessions", format_sessions)
    else:
        print("Source must be one of 'api' or 'file'")
        sys.exit(1)


def parse_batch_sessions(batch_subparsers):
    session_parser = batch_subparsers.add_parser("sessions")
    session_parser.add_argument("--source", "-s", required=True)
    session_parser.add_argument("--path", "-p", required=True)
    session_parser.set_defaults(func=batch_sessions)
