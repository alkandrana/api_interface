import sys, os, dotenv
from ..auth import send_auth_request
from ..scenes.scene import get_one_scene
from ..utils import to_zulu
dotenv.load_dotenv()
def get_scene_id(code):
    print(f"Fetching scene with code {code}...")
    res = get_one_scene(code)
    if res.status_code == 404:
        print("No scene with that code.")
        sys.exit(1)
    else:
        scene = res.json()
    return scene['id']

def build_session_body(args):
    body = {
        "date": args.date,
        "words": args.words
    }
    scene_id = get_scene_id(args.code)
    body['sceneId'] = scene_id
    if args.start:
        body['startTime'] = to_zulu(args.start)
    if args.stop:
        body['stopTime'] = to_zulu(args.stop)
    if args.note:
        body['comments'] = args.note
    return body

def create_session(args):
    body = build_session_body(args)
    request = {
        "method": "POST",
        "endpoint": f"{os.getenv('BASE_URL')}/sessions",
        "payload": body
    }
    res = send_auth_request(request)
    print(f"Request status: {res.status_code, res.reason}")

def parse_create_session(session_subparsers):
    create_parser = session_subparsers.add_parser("create")
    create_parser.add_argument("--date", "-d", required=True)
    create_parser.add_argument("--words", "-w", required=True)
    create_parser.add_argument("--code", "-c", required=True, help="Code of the scene to associate with the session.")
    create_parser.add_argument("--start", "-b", required=False)
    create_parser.add_argument("--stop", "-e", required=False)
    create_parser.add_argument("--note", "-n", required=False)
    create_parser.set_defaults(func=create_session)

# date: 2026-06-06
# startTime: 2026-06-06 17:33:48
# stopTime: 2026-06-06 17:54:40
# words: 275
# comments: None