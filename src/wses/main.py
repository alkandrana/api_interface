import argparse
from .commands.api.projects import parse_project
from .commands.api.scenes import parse_scenes
from .commands.api.sessions import parse_sessions
from .commands.api.batch_post import parse_batch_post
from .commands.setup.config import parse_config


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    parse_config(subparsers)
    parse_project(subparsers)
    parse_scenes(subparsers)
    parse_sessions(subparsers)
    parse_batch_post(subparsers)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
