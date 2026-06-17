from wses import load_config
from ...crud import check_record_exists
from pathlib import Path
import csv
def get_scene_id(compound_id):
    codes = {}
    if "-" in compound_id:
        parts = compound_id.split("-")
        codes["project"] = parts[0]
        codes["scene"] = parts[1]
    return codes

def get_scenes_in_log():
    scenes = []
    log_file = load_config()["log_file"]
    if Path(log_file).exists():
        with open(log_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                scenes.append(row["scene_id"])
    return scenes


# 2. using the resultant list of scenes, get all projects referenced
def get_projects_from_log(scene_codes) -> list[str]:
    booklist = []
    for scene in scene_codes:
        proj = get_scene_id(scene)["project"]
        if not proj:
            print(f"Project not found for scene: {scene}")
        if proj.lower() not in booklist:
            booklist.append(proj.lower())
    return booklist

# 3. get all unique scenes for a given project
def get_scenes_for_project(scenes: list[str], code: str) -> list[str]:
    book_scenes = []
    for s in scenes:
        codes = get_scene_id(s)
        if codes["project"].lower().startswith(code.lower()):
            book_scenes.append(codes["scene"].upper())
    unique_book_scenes = list(dict.fromkeys(book_scenes))
    return unique_book_scenes

#4. print out by project
def print_all_scenes(args) -> dict[str, list[str]]:
    projects = {}
    all_scene_codes = get_scenes_in_log()
    project_codes = get_projects_from_log(all_scene_codes)
    for code in project_codes:
        print(f"Scenes for project: {code.upper()}")
        unique_scene_codes = get_scenes_for_project(all_scene_codes, code)
        print(unique_scene_codes)
        projects[code] = unique_scene_codes
    if args.sync:
        check_sync_status(projects)
    return projects

def check_sync_status(projects: dict[str, list[str]]):
    scenes_to_create = {}
    for key, value in projects.items():
        if key not in scenes_to_create:
            scenes_to_create[key] = []
        for code in value:
            if not check_record_exists(code, "scenes"):
                if code not in scenes_to_create[key]:
                    scenes_to_create[key].append(code)
    print(f"Scenes that need to be synced {scenes_to_create}")
    return scenes_to_create



def parse_sync_list(sync_subparsers):
    list_parser = sync_subparsers.add_parser("list")
    list_parser.add_argument("--sync", "-s", action="store_true", help="Check which scenes need to be added to the API")
    list_parser.set_defaults(func=print_all_scenes)