import os, dotenv
from typing import Any
from wlogs.library.api.auth import send_auth_request
from ..projects.list import get_project_by_code

dotenv.load_dotenv()


def get_scenes(code) -> dict[str, Any]:
    proj = get_project_by_code(code)
    project_id = proj["id"]
    request = {
        "method": "GET",
        "endpoint": f"{os.getenv('BASE_URL')}/scenes/project/{project_id}",
    }
    scenes = send_auth_request(request)
    scenes.sort(key=lambda sc: sc["sequence"])
    return {"project": proj["title"], "scenelist": scenes}


def print_scenes(project):
    print(f"\n{project['project']} contains {len(project['scenelist'])} scenes:\n")
    scenes = project["scenelist"]
    for scene in scenes:
        print(f"Scene {scene['sequence']}: ")
        for key, value in scene.items():
            if not "id" in key.lower() and not "status" in key:
                print(f"{key}: {value}")
            elif key == "status":
                print(f"{key}: {value['name']}")
        print("\n")


def view_scenes_by_project(args):
    proj = get_scenes(args.code)
    print_scenes(proj)


def parse_scenes_by_project(scene_subparsers):

    scene_project_parser = scene_subparsers.add_parser("project")
    scene_project_parser.add_argument("--code", "-c", required=True)
    scene_project_parser.set_defaults(func=view_scenes_by_project)

