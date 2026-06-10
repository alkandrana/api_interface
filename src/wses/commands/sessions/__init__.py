from .create_session import parse_create_session
from .list_sessions import parse_list_sessions


def parse_sessions(subparsers):
    session_parser = subparsers.add_parser("sessions")
    session_subparsers = session_parser.add_subparsers(dest="sessions")
    parse_list_sessions(session_subparsers)
    parse_create_session(session_subparsers)
