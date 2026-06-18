from ..library.api.batch_post.sync.list import get_scene_id
from ..library.api.scenes.create_scene import post_scene
from ..library.dates import to_zulu
from ..library.file.scenes import get_next_scene_num
from ..library.file.search import get_book_path
from ..library.api.crud import get_status_values, get_record_id
import yaml
import sys

def get_scenes_dir(details, book_path):
    scene_path = book_path / "manuscript" / "scenes"
    if "plotline" in details:
        scene_path = scene_path / details["plotline"]
    if "chapter_title" in details:
        scene_path = scene_path / details["chapter_title"]
    return scene_path
def create_scene_file(details, filename):
    header = {}
    for key, value in details.items():
        if "project" not in key:
            header[key] = value
    if not filename.exists():
        with open(filename, "w") as f:
            f.write("---\n")
            yaml.dump(header, f, default_flow_style=False)
            f.write("---\n\n")
            f.write(f"# {details['scene_name']}")
        print(f"Yaml header written to {filename}")
    else:
        print("Scene already exists. Skipping...")

def convert_yaml_to_payload(header):
    statuses = get_status_values()
    codes = get_scene_id(header["scene_id"])
    project_id = get_record_id(codes["project"], "projects")
    if not project_id:
        print("Project doesn't exist yet. Create it with 'wlogs projects new'")
        sys.exit(1)
    status = [st["id"] for st in statuses if st["name"].lower() == header["status"]]
    payload = {
        "code": header["scene_id"],
        "sequence": header["scene_order"],
        "name": header["scene_name"],
        "words": header["word_count"],
        "statusId": status[0] if len(status) > 0 else None,
        "plotline": header["protagonist"] if "protagonist" in header else None,
        "created": to_zulu(header["created"]) if "created" in header else None,
        "projectId": project_id
    }
    return payload
def get_scene_details(args):
    scene_details = {
        "scene_id": f"{args.project}-{args.code}",
        "scene_name": args.name,
        "project_code": args.project,
    }
    if args.chapter:
        scene_details["chapter_title"] = args.chapter
    if args.plotline:
        scene_details["protagonist"] = args.plotline
    if args.sequence:
        scene_details["scene_order"] = args.sequence
    else:
        book_path = get_book_path(args.project)
        path = get_scenes_dir(scene_details, book_path)
        scene_details["scene_order"] = get_next_scene_num(path)
    if args.words:
        scene_details["word_count"] = args.words
    else:
        scene_details["word_count"] = 0
    scene_details["status"] = "pending"
    return scene_details

def create_scene(args):
    scene_details = get_scene_details(args)
    book_path = get_book_path(scene_details["project_code"])
    filename = get_scenes_dir(scene_details, book_path) / f"{scene_details["project_code"]}-{scene_details['scene_id']}.md"
    create_scene_file(scene_details, filename)
    payload = convert_yaml_to_payload(scene_details)
    res = post_scene(payload)
    if 200 <= res.status_code < 300:
        print("Scene successfully saved to the API")
    else:
        print("There was an error: ", res.status_code, res.reason, res.json())

def parse_new_scene(subparsers):
    scene_parser = subparsers.add_parser("scene")
    scene_subparsers = scene_parser.add_subparsers(dest="subcommand")
    create_parser = scene_subparsers.add_parser("create")
    create_parser.add_argument("--code", "-c", required=True)
    create_parser.add_argument("--name", "-t", required=True)
    create_parser.add_argument("--project", "-b", required=True)
    create_parser.add_argument("--chapter", "-ch", required=False)
    create_parser.add_argument("--plotline", "-p", required=False)
    create_parser.add_argument("--sequence", "-n", required=False)
    create_parser.add_argument("--words", "-w", required=False)
    create_parser.set_defaults(func=create_scene)