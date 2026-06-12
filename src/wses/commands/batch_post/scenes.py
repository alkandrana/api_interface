import sys

from .utils import transfer, batch_from_file
from .. import get_status_id, get_project_id, send_request, node_url
import os, dotenv
from ..projects.list import get_project_by_id
dotenv.load_dotenv()

def get_project_relation(sc):
    req = {
        "method": "GET",
        "endpoint": f"{node_url}/projects/{sc['projectId']}",
    }
    code = get_project_by_id(req, send_request)
    project_id = get_project_id(code, f"{os.getenv('BASE_URL')}/projects/code")
    return project_id

def format_scenes(scenes):
    scenelist = []
    for s in scenes:
        scene = {
            "code": s['code'],
            "sequence": s['sequence'],
            "name": s['name'],
            "words": s['words'],
            "statusId": get_status_id(s['status']),
            "plotline": s['plotline'],
            "projectId": get_project_relation(s)
        }
        scenelist.append(scene)
    return scenelist

def batch_scenes(args):
    if args.source == 'api':
        transfer(node_url, "scenes", format_scenes)
    elif args.source == 'file':
        batch_from_file(args.path, "scenes", format_scenes)
    else:
        print("Source must be one of 'api' or 'file'")
        sys.exit(1)

def parse_batch_scenes(batch_subparsers):
    scene_parser = batch_subparsers.add_parser('scenes')
    scene_parser.add_argument('--source', '-s', required=True)
    scene_parser.add_argument('--path', '-p', required=True)
    scene_parser.set_defaults(func=batch_scenes)
