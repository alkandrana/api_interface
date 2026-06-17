from .projects import parse_file_project


def parse_file(subparsers):
    file_parser = subparsers.add_parser("local")
    file_subparsers = file_parser.add_subparsers(dest="subcommand")
    parse_file_project(file_subparsers)
