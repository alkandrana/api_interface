import os, dotenv
from datetime import datetime
from ..auth import send_auth_request
asp_url = os.getenv("BASE_URL")
node_url = 'http://localhost:3000'

dotenv.load_dotenv()
def get_all_sessions():
    request = {
        "method": "GET",
        "endpoint": f"{node_url}/sessions"
    }
    res = send_auth_request(request)
    sessions = res.json()
    sessions.sort(key=lambda x: datetime.fromisoformat(x["startTime"]))
    return sessions


def print_sessions(sessions):
    print(f"\nYou have {len(sessions)} sessions:\n")
    for ses in sessions:
        for key, value in ses.items():
            if key == "scene":
                print(f"{key}: {value['code']}")
            elif key == "author":
                print(f"{key}: {value['userName']}")
            elif "time" in key.lower():
                value = datetime.fromisoformat(value)
                value = value.astimezone()
                print(f"{key}: {datetime.strftime(value, '%Y-%m-%d %H:%M:%S')}")
            elif not "id" in key.lower():
                print(f"{key}: {value}")
        print("\n")

def list_sessions(_):
    sessions = get_all_sessions()
    print_sessions(sessions)

def parse_list_sessions(session_subparsers):
    list_parser = session_subparsers.add_parser("list")
    list_parser.set_defaults(func=list_sessions)