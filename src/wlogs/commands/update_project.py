from wlogs.library.api.crud import get_patch_payload
from ..library.api.projects.update import build_project_patch, patch_goal
from ..library.file.projects.update import update_local_goal

def update_project(args):
    update_local_goal(args.goal, args.book)
    payload = get_patch_payload(args.goal, "/goal")
    print("Ready to patch: ", payload)
    request = build_project_patch(payload, args.book)
    print("Patch request: ", request)
    patch_goal(request)

def parse_update_project(subparsers):
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--goal", "-g", help="The new value for the goal property")
    update_parser.add_argument("--book", "-b", required=True, help="The book to update")
    update_parser.set_defaults(func=update_project)