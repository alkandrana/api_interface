import json
import sys
from pathlib import Path
import csv
from typing import Any

from wses.commands.api.batch_post.scenes import get_scene_details
from wses.commands.api.batch_post.utils import post_record
from wses.commands import print_list_dict
from wses.commands.file.search import find_file

from wses.commands.api import get_record_by_code
from wses.commands.utils import print_dict, print_list


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


def sync_scenes(args):
    if args.code:
        scenes = list_scenes_in_project(args.code)
        sync_scenes_in_project(scenes)
    else:
        book_codes = get_projects_from_log()
        for code in book_codes:
            sync_scenes_in_project(code)

def list_scenes_in_project(code: str):
    code = code.upper()
    print(f"Getting scenes for project {code}")
    scenes = get_scene_details(code)
    print_list_dict(scenes)
    return scenes
def sync_scenes_in_project(scenes):
    print("Posting scenes to API: ")
    for scene in scenes:
        post_record(scene, "scenes")
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


def parse_batch_sync(sync_subparsers):
    project_parser = sync_subparsers.add_parser("projects")
    project_parser.set_defaults(func=print_projects)
    scenes_parser = sync_subparsers.add_parser("scenes")
    scenes_parser.add_argument("--code", "-c", required=False)
    scenes_parser.set_defaults(func=sync_scenes)
