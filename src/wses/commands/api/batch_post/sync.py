from pathlib import Path
import csv
from ...file.utils import load_config
from .. import get_record_by_code
from ...utils import print_dict, print_list


# exctract all scenes reference in the writing sessions log file
def get_scenes_in_log(path):
    scenes = []
    if Path(path).exists():
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                scenes.append(row["scene_id"])
    return scenes


# using the resultant list of scenes, get all projects referenced
def get_projects_from_scenes(scenes: list[str]):
    booklist = []
    for scene in scenes:
        if "-" in scene:
            proj = scene.split("-")[0]
            if proj.lower() not in booklist:
                booklist.append(proj.lower())
        else:
            print(f"Project not found for scene: {scene}")
    return booklist


def print_projects(_):
    config = load_config()
    log_file = config["log_file"]
    scenes = get_scenes_in_log(log_file)
    books = get_projects_from_scenes(scenes)
    books_to_add = []
    for b in books:
        b_obj = get_record_by_code(b, "projects")
        if not b_obj:
            books_to_add.append(b)
        else:
            print_dict(b_obj)
    print("Found {len(books_to_add)} projects to create: ")
    print_list(books_to_add)


def parse_batch_sync(batch_subparsers):
    sync_parser = batch_subparsers.add_parser("sync")
    sync_parser.add_argument("--book", "-b", action="store_true")

    sync_parser.set_defaults(func=print_projects)
