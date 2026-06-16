from .list import parse_sync_list
def parse_sync(batch_subparsers):
    sync_parser = batch_subparsers.add_parser("sync")
    sync_subparsers = sync_parser.add_subparsers(dest="sub2command")
    parse_sync_list(sync_subparsers)