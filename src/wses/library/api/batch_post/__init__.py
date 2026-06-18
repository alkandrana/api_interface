from .sync import parse_sync
from .projects import parse_batch_projects
from .scenes import parse_batch_scenes
from wses.library.api.batch_post.sync.sync_sessions import parse_batch_sessions


def parse_batch_post(subparsers):
    batch_parser = subparsers.add_parser("batch")
    batch_subparsers = batch_parser.add_subparsers(dest="subcommand")
    parse_batch_projects(batch_subparsers)
    parse_batch_scenes(batch_subparsers)
    parse_batch_sessions(batch_subparsers)
    parse_sync(batch_subparsers)
