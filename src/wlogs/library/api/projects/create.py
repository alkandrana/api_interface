import os

from wlogs import load_config
from wlogs.library.api.auth import send_auth_request


def post_project(book):
    request = {
        "method": "POST",
        "endpoint": f"{load_config()['api_url']}/projects",
        "payload": book,
    }
    response = send_auth_request(request)
    if response.status_code == 409:
        print("Project already exists. Skipping...")
    elif 200 <= response.status_code < 300:
        print("Project successfully created.")
    else:
        print("Response status: ", response.status_code, response.reason, response.json())

def create_project(args):
    book = {
        "code": args.code,
        "title": args.title,
    }
    if not args.goal:
        book["goal"] = 100000
    else:
        book["goal"] = args.goal
    if args.series:
        book["series"] = args.series
    post_project(book)
def parse_create_project(project_subparsers):
    create_parser = project_subparsers.add_parser("create")
    create_parser.add_argument("--code", "-c", required=True)
    create_parser.add_argument("--title", "-t", required=True)
    create_parser.add_argument("--series", "-s", required=False)
    create_parser.add_argument("--goal", "-g", required=False)
    create_parser.set_defaults(func=create_project)

