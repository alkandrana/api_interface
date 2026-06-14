from pathlib import Path
import yaml, csv

def load_yaml_header(path):
    if Path(path).exists():
        with open(path, 'r') as f:
            content = f.read()
        parts = content.split('---')
        header = parts[1].strip()
        header = yaml.safe_load(header)
    else:
        header = None
    return header

def get_scenes_in_log(path):
    scenes = []
    if Path(path).exists():
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                scenes.append(row['scene_id'])
    return scenes