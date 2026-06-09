import os

from ..auth import send_auth_request

def get_project_id(project_code):
    project_req = {
        'method': 'GET',
        'endpoint': f'{os.getenv("BASE_URL")}/projects/code/{project_code}'
    }
    project = send_auth_request(project_req)
    return project["id"]

def build_body(args, project_id):
    body = {
        "code": args.code,
        "name": args.name,
        "projectId": project_id
    }
    if args.sequence:
        body['sequence'] = args.sequence
    if args.words:
        body['words'] = args.words
    if args.status:
        body['statusId'] = args.status
    if args.mc:
        body['plotline'] = args.mc
    return body

def post_scene(body):
    scene_req = {
        "method": "POST",
        "endpoint": f"{os.getenv('BASE_URL')}/scenes",
        "payload": body
    }
    response = send_auth_request(scene_req)
    return response

def create_scene(args):
    project_id = get_project_id(args.project)
    body = build_body(args, project_id)
    response = post_scene(body)
    print(f"Response status: {response.status_code} {response.reason}")

def parse_create_scene(scene_subparsers):
    create_parser = scene_subparsers.add_parser("create")
    create_parser.add_argument("--code", "-c", required=True)
    create_parser.add_argument("--name", "-t", required=True)
    create_parser.add_argument("--project", "-p", required=True, help="Project code")
    create_parser.add_argument("--sequence", "-n", required=False, help="The integer representing where in the story the scene falls (optional)")
    create_parser.add_argument("--words", "-w", required=False, help="Word count for the scene (default: 0)")
    create_parser.add_argument("--status", "-s", required=False, help="Status of the scene. Valid options are: pending, writing, finished, aborted. Defaults to pending.")
    create_parser.add_argument("--mc", "-ch", required=False, help="In a multi-plotline story, you can use this option to set the protagonist or viewpoint character for this scene.")
    create_parser.set_defaults(func=create_scene)

    # {
    #   'scene_id': 'SOD-032V',
    #   'scene_name': 'Terms',
    #   'chapter_title': 'Terms',
    #   'scene_order': 32,
    #   'protagonist': 'Vathyri',
    #   'status': 'written',
    #   'word_count': 3959}
    # }