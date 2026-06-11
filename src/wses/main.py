import sys
import argparse
from .commands.projects.projects import parse_project
from .commands.scenes import parse_scenes
from .commands.sessions import parse_sessions

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    parse_project(subparsers)
    parse_scenes(subparsers)
    parse_sessions(subparsers)
    args = parser.parse_args()
    args.func(args)
    # print(args)

if __name__ == "__main__":
    main()
