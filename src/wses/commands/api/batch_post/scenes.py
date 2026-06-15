import csv
import sys, os, dotenv
from pathlib import Path
from .utils import transfer, batch_from_file, post_record
from ... import get_status_id, get_project_id, send_request, node_url, get_record_id
from ...file.scenes import load_yaml_header
from ...file.search import find_file, fast_search
from ..projects.list import get_project_by_id

dotenv.load_dotenv()


def build_scene_from_file(scene_header, project_id):
    status_id = get_status_id("writing")
    try:
        scene = {
            "code": scene_header["scene_id"].split("-")[1],
            "sequence": scene_header["scene_order"],
            "name": scene_header["scene_name"],
            "words": scene_header["word_count"],
            "statusId": status_id,
            "plotline": scene_header["protagonist"],
            "projectId": project_id,
        }
        return scene
    except KeyError:
        print(f"Malformed scene header for scene: {scene_header}")
        sys.exit(1)


def get_scene_details(book_code):
    # check whether project exists
    project_id = get_record_id(book_code, "projects")
    if not project_id:
        print("Project doesn't exist yet.")
        sys.exit(1)
    path = find_file(book_code, full_name=True)
    scenes_path = Path(path) / "manuscript" / "scenes"
    scenes = [p for p in fast_search(".md", scenes_path)]
    batch = []
    for path in scenes:
        print(f"\nGetting post details for scene: {path.name}")
        header = load_yaml_header(path)
        payload = build_scene_from_file(header, project_id)
        batch.append(payload)
    batch.sort(key=lambda x: x["sequence"])
    return batch


def get_project_relation(sc):
    req = {
        "method": "GET",
        "endpoint": f"{node_url}/projects/{sc['projectId']}",
    }
    code = get_project_by_id(req)
    project_id = get_project_id(code, f"{os.getenv('BASE_URL')}/projects/code")
    return project_id


def format_scenes(scenes):
    scenelist = []
    for s in scenes:
        scene = {
            "code": s["code"],
            "sequence": s["sequence"],
            "name": s["name"],
            "words": s["words"],
            "statusId": get_status_id(s["status"]),
            "plotline": s["plotline"],
            "projectId": get_project_relation(s),
        }
        scenelist.append(scene)
    return scenelist


def batch_scenes(args):
    if args.source == "api":
        transfer(node_url, "scenes", format_scenes)
    elif args.source == "file":
        scenes_to_post = get_scene_details(args.code)
        for sc in scenes_to_post:
            post_record(sc, "scenes")
    else:
        print("Source must be one of 'api' or 'file'")
        sys.exit(1)


def parse_batch_scenes(batch_subparsers):
    scene_parser = batch_subparsers.add_parser("scenes")
    scene_parser.add_argument("--source", "-s", required=True)
    scene_parser.add_argument("--code", "-c", required=True)
    scene_parser.set_defaults(func=batch_scenes)
