from .create_session import parse_create_session
from .list_sessions import parse_list_sessions
from .run import parse_run_session






def parse_sessions(subparsers):
    session_parser = subparsers.add_parser("sessions")
    session_subparsers = session_parser.add_subparsers(dest="subcommand")
    parse_list_sessions(session_subparsers)
    parse_create_session(session_subparsers)
    parse_run_session(session_subparsers)
