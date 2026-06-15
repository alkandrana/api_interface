from .sync import parse_batch_sync
from .projects import parse_batch_projects
from .scenes import parse_batch_scenes
from .sessions import parse_batch_sessions


def parse_batch_post(subparsers):
    batch_parser = subparsers.add_parser("batch")
    batch_subparsers = batch_parser.add_subparsers(dest="subcommand")
    parse_batch_projects(batch_subparsers)
    parse_batch_scenes(batch_subparsers)
    parse_batch_sessions(batch_subparsers)
    parse_batch_sync(batch_subparsers)
