from pathlib import Path
import csv


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
def get_projects_from_scenes(scenes):
    booklist = []
    for scene in scenes:
        if "-" in scene:
            proj = scene.split("-")[0]
            if proj.lower() not in booklist:
                booklist.append(proj.lower())
        else:
            print(f"Project not found for scene: {scene}")
    return booklist


# def print_projects():


def parse_batch_sync(batch_subparsers):
    sync_parser = batch_subparsers.add_parser("sync")
    sync_parser.add_argument("--book", "-b", store_action=True)

    sync_parser.add_defaults(print_projects)
