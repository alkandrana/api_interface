import sys
from datetime import datetime

from .. import print_list_dict
from ..auth import send_auth_request
from ...commands import get_record_id, asp_url
from ..projects.list import get_project_by_id

def get_all_sessions():
    request = {
        "method": "GET",
        "endpoint": f"{asp_url}/sessions"
    }
    res = send_auth_request(request)
    sessions = res.json()
    sessions.sort(key=lambda x: datetime.fromisoformat(x["startTime"]))
    return sessions


def print_sessions(sessions, wpm=False):
    print(f"\n{len(sessions)} sessions match the criteria:\n")
    for ses in sessions:
        print(build_session_title(ses) + ":")
        for key, value in ses.items():
            if key == "scene" and value and "code" in value:
                print(f"{key}: {value['code']}")
            elif key == "author" and value and "userName" in value:
                print(f"{key}: {value['userName']}")
            elif "time" in key.lower():
                value = datetime.fromisoformat(value)
                value = value.astimezone()
                print(f"{key}: {datetime.strftime(value, '%Y-%m-%d %H:%M:%S')}")
            elif key == "duration" or key == "wpm":
                print(f"{key}: {round(value)}")
            elif not "id" in key.lower():
                print(f"{key}: {value}")
        print("\n")

def build_session_title(session):
    project = session["scene"]["project"]["code"]
    scene = session["scene"]["code"]
    date = session["date"]
    duration = round(session["duration"])
    title = f"{duration} minute session in {project} {scene} on {date}"
    return title

def get_by_date(date, sessions):
    filtered = [s for s in sessions if s['date'].startswith(date)]
    return filtered

def get_by_scene(scene):
    scene_id = get_record_id(scene, "scenes")
    request = {
        "method": "GET",
        "endpoint": f"{asp_url}/sessions/scene/{scene_id}"
    }
    res = send_auth_request(request)
    return res.json()

def get_by_project(project):
    project_id = get_record_id(project, "projects")
    request = {
        "method": "GET",
        "endpoint": f"{asp_url}/sessions/project/{project_id}"
    }
    res = send_auth_request(request)
    return res.json()

def count_sessions(sessions):
    count = 0
    for ses in sessions:
        count += ses["words"]
    return count
def calc_wpm(session):
    if not session["startTime"] or not session["stopTime"]:
        print("Wpm cannot be calculated: missing time data")
        sys.exit(1)
    words = session["words"]
    start = datetime.fromisoformat(session["startTime"])
    stop = datetime.fromisoformat(session["stopTime"])
    duration = (stop - start).total_seconds() / 60
    return round(words / duration, 2)
def list_sessions(args):
    if args.scene:
        sessions = get_by_scene(args.scene)
    elif args.project:
        sessions = get_by_project(args.project)
    elif args.date:
        print(args.date)
        sessions = get_all_sessions()
        sessions = get_by_date(args.date, sessions)
    elif args.today:
        date = datetime.strftime(datetime.today(), "%Y-%m-%d")
        sessions = get_all_sessions()
        sessions = get_by_date(date, sessions)
    else:
        sessions = get_all_sessions()
    if args.count:
        word_count = count_sessions(sessions)
        print(f"\n{word_count:,} words written in all sessions.")
    else:
        print_sessions(sessions, args.wpm)

def parse_list_sessions(session_subparsers):
    list_parser = session_subparsers.add_parser("list")
    list_parser.add_argument("--today", "-t", action="store_true")
    list_parser.add_argument("--date", "-d", required=False)
    list_parser.add_argument("--scene", "-s", required=False)
    list_parser.add_argument("--project", "-p", required=False)
    list_parser.add_argument("--count", "-c", action="store_true", required=False)
    list_parser.add_argument('--wpm', "-w", action="store_true", required=False)
    list_parser.set_defaults(func=list_sessions)