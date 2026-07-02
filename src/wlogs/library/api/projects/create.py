import os

from wlogs import load_config
from wlogs.library.api.auth import send_auth_request


def create_project(args):
    body = {
        "code": args.code,
        "title": args.title,
    }
    if not args.goal:
        body["goal"] = 100000
    else:
        body["goal"] = args.goal
    if args.series:
        body["series"] = args.series
    request = {
        "method": "POST",
        "endpoint": f"{load_config()['api_url']}/projects",
        "payload": body,
    }
    response = send_auth_request(request)
    print("Response status: ", response.status_code, response.reason)


def parse_create_project(project_subparsers):
    create_parser = project_subparsers.add_parser("create")
    create_parser.add_argument("--code", "-c", required=True)
    create_parser.add_argument("--title", "-t", required=True)
    create_parser.add_argument("--series", "-s", required=False)
    create_parser.add_argument("--goal", "-g", required=False)
    create_parser.set_defaults(func=create_project)

