from .scenes_by_project import parse_scenes_by_project
from .scene import parse_scene
from .create_scene import parse_create_scene


def parse_scenes(subparsers):
    scene_parser = subparsers.add_parser("scenes")
    scene_subparsers = scene_parser.add_subparsers(dest="subcommand")
    parse_scenes_by_project(scene_subparsers)
    parse_scene(scene_subparsers)
    parse_create_scene(scene_subparsers)