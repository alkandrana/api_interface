from .create_session import parse_create_session






def parse_sessions(subparsers):
    session_parser = subparsers.add_parser("sessions")
    session_subparsers = session_parser.add_subparsers(dest="subcommand")
    parse_create_session(session_subparsers)
