import sys
from .utils import transfer, batch_from_file
from ..scenes.scene import get_one_scene
from ..utils import to_zulu, join_date


def get_scene_id(code):
    res = get_one_scene(code)
    if 200 <= res.status_code < 300:
        scene = res.json()
        return scene['id']
    else:
        print("An error occurred: ", res.status_code, res.reason)
        sys.exit(1)
def format_sessions(sessions):
    sessionlist = []
    for ses in sessions:
        # different between api and file
        scene_id = get_scene_id(ses['scene']['code'])
        ses['startTime'] = join_date(ses['startTime'], ses['date'])
        ses['stopTime'] = join_date(ses['stopTime'], ses['date'])
        session = {
            'date': ses['date'],
            'startTime': to_zulu(ses['startTime']),
            'stopTime': to_zulu(ses['stopTime']),
            'words': ses['words'],
            'sceneId': scene_id,
            'comments': ses['comments']
        }
        sessionlist.append(session)
    return sessionlist

def batch_sessions(args):
    if args.source == 'api':
        transfer(args.path, "sessions", format_sessions)
    elif args.source == 'file':
        batch_from_file(args.path, "sessions", format_sessions)
    else:
        print("Source must be one of 'api' or 'file'")
        sys.exit(1)

def parse_batch_sessions(batch_subparsers):
    session_parser = batch_subparsers.add_parser('sessions')
    session_parser.add_argument('--source', '-s', required=True)
    session_parser.add_argument('--path', '-p', required=True)
    session_parser.set_defaults(func=batch_sessions)
