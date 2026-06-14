import os, dotenv
import sys

from wses.commands import get_record_id, send_auth_request

dotenv.load_dotenv()
def build_patch(args):
    scene_id = get_record_id(args.code, "scenes")
    print(f"ID for scene with code {args.code}: {scene_id}")
    payload = {
        "op": "replace",
        "path": f"/{args.property}",
        "value": args.value
    }
    print(f"Payload: {payload}")
    request = {
        "method": "PATCH",
        "endpoint": f"{os.getenv("BASE_URL")}/scenes/{scene_id}",
        "payload": payload
    }
    print(f"Request: {request}")
    return request

def send_update_request(request):
    res = send_auth_request(request)
    if 200 <= res.status_code < 300:
        print("Scene updated successfully")
    elif res.status_code == 404:
        print("Scene not found.")
        sys.exit(1)
    else:
        print("An error occurred: ", res.status_code, res.reason, res.json())
        sys.exit(1)

def update_scene(args):
    request = build_patch(args)
    send_update_request(request)

def parse_update_scene(scene_subparsers):
    update_parser = scene_subparsers.add_parser("update")
    update_parser.add_argument("--code", "-c", type=str, required=True, help="Scene Code")
    update_parser.add_argument("--property", "-p", type=str, required=True, help="Which scene property to update")
    update_parser.add_argument("--value", "-v", type=str, required=True, help="The new value to set")
    update_parser.set_defaults(func=update_scene)