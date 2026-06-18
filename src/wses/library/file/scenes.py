from pathlib import Path
import yaml, csv
from .search import find_file
import sys
from wses.library.file.search import fast_search


def load_yaml_header(path: Path | str) -> dict[str, str]:
    if Path(path).exists():
        with open(path, 'r') as f:
            content = f.read()
        parts = content.split('---')
        if len(parts) < 2:
            header = {}
        else:
            header = parts[1].strip()
            header = yaml.safe_load(header)
    else:
        header = {}
    return header

def get_scenes_in_log(path):
    scenes = []
    if Path(path).exists():
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                scenes.append(row['scene_id'])
    return scenes

def get_next_scene_num(path):
    scene_paths = [p for p in fast_search(".md", path)]
    next_sequence = len(scene_paths)
    return next_sequence

def get_scene_path(scene):
    path = find_file(scene)
    if not path or not path.exists():
        print("Could not find scene")
        sys.exit(1)
    else:
        return path