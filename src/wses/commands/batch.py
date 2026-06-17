import csv
import sys
from dateutil import parser
from wses.library.file.search import get_book_path
from ..library.api.crud import get_status_values
from ..library.dates import to_zulu, normalize_date
from ..library.file.search import find_file
from .new_scene import create_scene_file, convert_yaml_to_payload, get_scenes_dir
from ..library.api.scenes.create_scene import post_scene

def import_scenes(root_path):
    csv_path = find_file("metadata", root_path)
    if csv_path and csv_path.exists():
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader]
        return rows
    else:
        print(f"Could not find metadata file for {root_path}")
        sys.exit(1)

def convert_csv_to_yaml(csv_dict, book_code):
    yaml_dict = {
        "scene_id": csv_dict["code"],
        "scene_name": csv_dict["Title"],
        "scene_order": csv_dict["sequence"],
        "word_count": csv_dict["Words"],
        "status": convert_csv_status(csv_dict["Status"]),
        "created": normalize_date(csv_dict["Created Date"]),
        "protagonist": csv_dict["plotline"],
        "project_code": book_code
    }
    return yaml_dict

def convert_csv_status(status):
    statuses = get_status_values()
    if "draft" in status.lower():
        value = "writing"
    elif "to do" in status.lower():
        value = "pending"
    elif "done" in status.lower():
        value = "finished"
    else:
        value = "pending"
    return value

def batch_scenes(args):
    novel_path = get_book_path(args.book)
    scenes_csv = import_scenes(novel_path)
    for sc in scenes_csv:
        header = convert_csv_to_yaml(sc, args.book)
        filename = get_scenes_dir(header, novel_path) / f"{header['project_code']}-{header['scene_id']}.md"
        create_scene_file(header, filename)
        payload = convert_yaml_to_payload(header)
        res = post_scene(payload)
        if 200 <= res.status_code < 300:
            print("Scene successfully saved to the API")
        elif res.status_code == 409:
            print("Scene already exists. Skipping...")
        else:
            print("There was an error: ", res.status_code, res.reason, res.json())

def parse_batch_scenes(subparsers):
    batch_parser = subparsers.add_parser("batch")
    batch_subparsers = batch_parser.add_subparsers(dest="subcommand")
    scene_parser = batch_subparsers.add_parser("scenes")
    scene_parser.add_argument("--book", "-b", required=True)
    scene_parser.set_defaults(func=batch_scenes)