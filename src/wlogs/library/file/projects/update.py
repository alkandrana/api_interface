import json
import sys

from ..scenes import load_yaml_header, get_scene_path
from ..search import get_book_path
from ...dates import load_json


def update_local_goal(value, book):
    print(f"Locating novel.json for {book}...")
    path = get_book_path(book) / "novel.json"
    book_details = load_json(path)
    book_details['goal'] = value
    with open(path, 'w') as f:
        json.dump(book_details, f)
    print(f"Updated goal in {path}: {book_details}")

