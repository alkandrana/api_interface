import sys
import argparse
from .commands.projects.api import parse_project

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    parse_project(subparsers)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
