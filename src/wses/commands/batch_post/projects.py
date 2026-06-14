import os
import sys

from .. import asp_url, node_url
from .utils import transfer, batch_from_file
from ..projects.list import get_project_by_code


def get_projects_from_scenes(scenes):
    booklist = []
    for scene in scenes:
        if '-' in scene:
            proj = scene.split('-')[0]
            if proj.lower() not in booklist:
                booklist.append(proj.lower())
        else:
            print(f"Project not found for scene: {scene}")
    return booklist

def format_projects(projects):
    booklist = []
    for b in projects:
        book = {
            "code": b['code'],
            'title': b['title'],
            'series': b['seriesTitle'],
            'goal': b['goal']
        }
        booklist.append(book)
    return booklist

def batch_projects(args):
    if args.source == 'api':
        transfer(args.path, "projects", format_projects)
    elif args.source == 'file':
        batch_from_file(args.path, "projects", format_projects)
    else:
        print("Source must be one of 'api' or 'file'")
        sys.exit(1)

def parse_batch_projects(batch_subparsers):
    project_parser = batch_subparsers.add_parser('projects')
    project_parser.add_argument('--source', '-s', required=True)
    project_parser.add_argument('--path', '-p', required=True)
    project_parser.set_defaults(func=batch_projects)
