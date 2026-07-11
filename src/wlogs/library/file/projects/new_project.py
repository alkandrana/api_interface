from pathlib import Path
from wlogs.library.file.search import find_file
import sys
import json


def get_project_details(code):
    title = input("Enter a name or title for the new book: ")
    series = input("Enter the series title for the new book (optional): ")
    goal = input("Enter your wordcount goal for the new book (100000): ")

    goal = int(goal or 100000)

    project = {
        "code": code,
        "title": title,
        "series": series if series else "N/A",
        "goal": goal,
    }
    return project


def create_book_structure(code, world):
    project_json = get_project_details(code)
    home_dir = find_file(world)
    if not home_dir or not home_dir.exists():
        print("Project directory could not be found.")
        sys.exit(1)
    else:
        scenes_home = Path(home_dir) / "books" / code.upper() / "manuscript" / "scenes"
        scenes_home.mkdir(parents=True, exist_ok=True)
        doc_file = home_dir / "books" / code.upper() / "novel.json"
        with open(doc_file, "w") as f:
            json.dump(project_json, f)
    return project_json


def new_book(args):
    create_book_structure(args.code, args.world)


def parse_file_project(file_subparsers):
    project_parser = file_subparsers.add_parser("book")
    project_subparsers = project_parser.add_subparsers(dest="sub2command")
    create_parser = project_subparsers.add_parser("create")
    create_parser.add_argument(
        "--code",
        "-c",
        required=True,
        help="Identifier for the new book, used at the folder name.",
    )
    create_parser.add_argument(
        "--world",
        "-w",
        required=True,
        help="The world or series name in which to creat the new book; should reflect the name of the parent directory.",
    )
    create_parser.set_defaults(func=new_book)
