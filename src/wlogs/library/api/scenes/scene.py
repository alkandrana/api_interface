import os, dotenv
from wlogs.library.api.auth import send_auth_request

dotenv.load_dotenv()


def get_one_scene(code: str):
    request = {
        "method": "GET",
        "endpoint": f"{os.getenv('BASE_URL')}/scenes/code/{code}",
    }
    scenes = send_auth_request(request)
    return scenes


def print_scene(scenelist):
    if len(scenelist) > 1:
        print("Multiple scenes match that scene code. Make a selection: ")
        for i, sc in enumerate(scenelist):
            print(f"{i}: {sc['name']}, {sc['project']['code']}")
        choice = input("Select the appropriate number: ")
        scene = scenelist[int(choice)]
    else:
        scene = scenelist[0]
    print("Scene {scene['code']}: {scene['name']}\n")
    for key, value in scene.items():
        if not key == "project":
            print(f"{key}: {value}")
        elif key == "project":
            print(f"project title: {value['title']}")


def view_one_scene(args):
    scenes = get_one_scene(args.code)
    print_scene(scenes)


def parse_scene(scene_subparsers):
    one_parser = scene_subparsers.add_parser("one")
    one_parser.add_argument("--code", "-c", required=True)
    one_parser.add_argument("--project", "-p", required=False)
    one_parser.set_defaults(func=view_one_scene)
