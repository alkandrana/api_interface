import os
from ..auth import send_auth_request


def get_projects():
    request = {
        "method": "GET",
        "endpoint": f"{os.getenv('BASE_URL')}/projects",
    }
    records = send_auth_request(request)
    return records


def print_projects(projects):
    print(f"Found {len(projects)} projects:\n")
    for rec in projects:
        for key, value in rec.items():
            if "author" not in key:
                print(f"{key}: {value}")
            elif key == "author":
                print(f"{key}: {value['userName']}")
        print("\n")

def view_all(args):
    projects = get_projects()
    print_projects(projects)

def get_project(code):
    request = {
        "method": "GET",
        "endpoint": f"{os.getenv('BASE_URL')}/projects/code/{code}",
    }
    record = send_auth_request(request)
    return record


def print_project(project):
    print(f"\nProject {project['id']}: {project['title']}")
    for key, value in project.items():
        if "author" not in key:
            print(f"{key}: {value}")
    print("\n")

def view_one(args):
    project = get_project(args.code)
    print_project(project)

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
        "endpoint": f"{os.getenv('BASE_URL')}/projects",
        "payload": body
    }
    response = send_auth_request(request)
    print("Response status: ", response.status_code, response.reason)

def parse_project(subparsers):
    project_parser = subparsers.add_parser("projects")
    project_subparsers = project_parser.add_subparsers(dest="subcommand")
    all_parser = project_subparsers.add_parser("all")
    all_parser.set_defaults(func=view_all)

    one_parser = project_subparsers.add_parser("one")
    one_parser.add_argument("--code", "-c", required=True)
    one_parser.set_defaults(func=view_one)

    create_parser = project_subparsers.add_parser("create")
    create_parser.add_argument("--code", "-c", required=True)
    create_parser.add_argument("--title", "-t", required=True)
    create_parser.add_argument("--series", "-s", required=False)
    create_parser.add_argument("--goal", "-g", required=False)
    create_parser.set_defaults(func=create_project)