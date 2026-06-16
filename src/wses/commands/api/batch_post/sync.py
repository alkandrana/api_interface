import json
import sys
from pathlib import Path
import csv
from typing import Any

from .scenes import get_scene_details
from .utils import post_record
from ... import print_list_dict
from ...file.search import find_file
from wses import load_config
from .. import get_record_by_code
from ...utils import print_dict, print_list


# exctract all scenes reference in the writing sessions log file
def get_scenes_in_log():
    scenes = []
    log_file = load_config()["log_file"]
    if Path(log_file).exists():
        with open(log_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                scenes.append(row["scene_id"])
    return scenes


# using the resultant list of scenes, get all projects referenced
def get_projects_from_log() -> list[str]:
    scene_codes = get_scenes_in_log()
    booklist = []
    for scene in scene_codes:
        if "-" in scene:
            proj = scene.split("-")[0]
            if proj.lower() not in booklist:
                booklist.append(proj.lower())
        else:
            print(f"Project not found for scene: {scene}")
    return booklist


def sync_projects(book_codes: list[str]):
    books_to_add = []
    book_records = []
    for b in book_codes:
        res = get_record_by_code(b, "projects")
        if res.status_code == 404:
            books_to_add.append(b)
        else:
            book_records.append(res.json())
    return {"remote": book_records, "local": books_to_add}


def get_project_from_repo(code: str):
    path = find_file(code.upper())
    if path:
        specs = path / "novel.json"
        if specs.exists():
            with open(specs, "r", encoding="utf-8-sig") as f:
                novel = json.load(
                    f,
                )
            return novel
    return code.upper()


def get_local_project_details(project_codes: list[str]):
    local_projects = []
    for c in project_codes:
        print(f"\nGetting details for project {c}")
        project = get_project_from_repo(c)
        if not isinstance(project, str):
            local_projects.append(project)
    return local_projects


def get_unsaved_projects(
    local_codes: list[str], local_projects: list[dict[str, Any]]
) -> list[str]:
    local_keys = [p["id"] for p in local_projects]
    codes = [c.upper() for c in local_codes if c.upper() not in local_keys]
    return codes


def sync_scenes(_):
    book_codes = get_projects_from_log()
    for code in book_codes:
        code = code.upper()
        print(f"Getting scenes for project {code}")
        scenes = get_scene_details(code)
        print_list_dict(scenes)
        # print("Posting scenes to API: ")
        # for scene in scenes:
        #     print(f"\t{scene}")
        #     post_record(scene, "scenes")


def print_projects(_):
    project_codes = get_projects_from_log()
    project_status = sync_projects(project_codes)
    remote_projects = project_status["remote"]
    local_projects = get_local_project_details(project_status["local"])
    print("\nProjects already saved to the API:")
    print_list_dict(remote_projects)
    print("Projects existing locally:")
    print_list_dict(local_projects)
    unsaved = get_unsaved_projects(project_status["local"], local_projects)
    if len(unsaved) > 0:
        print("Projects for which local details cannot be found:")
        print_list(unsaved)


def parse_batch_sync(batch_subparsers):
    sync_parser = batch_subparsers.add_parser("sync")
    sync_subparsers = sync_parser.add_subparsers(dest="sub2command")
    project_parser = sync_subparsers.add_parser("projects")
    project_parser.set_defaults(func=print_projects)
    scenes_parser = sync_subparsers.add_parser("scenes")
    scenes_parser.set_defaults(func=sync_scenes)
