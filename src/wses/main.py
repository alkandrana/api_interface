import argparse
from wses.library.api.projects import parse_project
from wses.library.api.scenes import parse_scenes
from wses.library.api.sessions import parse_sessions
from .commands.setup.config import parse_config
from .commands.batch import parse_batch_scenes
from .commands.plot import parse_plotter
from .commands.update_project import parse_update_project
from wses.library.file import parse_file
from wses.library.api.auth import parse_auth


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    parse_config(subparsers)
    parse_auth(subparsers)
    parse_project(subparsers)
    parse_scenes(subparsers)
    parse_sessions(subparsers)
    parse_batch_scenes(subparsers)
    parse_file(subparsers)
    parse_plotter(subparsers)
    parse_update_project(subparsers)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
