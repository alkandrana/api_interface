from .list import parse_sync_list
from .sync import parse_batch_sync
def parse_sync(subparsers):
    sync_parser = subparsers.add_parser("sync")
    sync_subparsers = sync_parser.add_subparsers(dest="sub2command")
    parse_sync_list(sync_subparsers)
    parse_batch_sync(sync_subparsers)