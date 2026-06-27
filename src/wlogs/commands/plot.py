import sys
import pandas as pd
from wlogs import load_config
from wlogs.library.api.auth import send_auth_request


def get_plotter(book_code):
    request = {
        "method": "GET",
        "endpoint": f"{load_config()['api_url']}/projects/plotter/{book_code}",
    }
    res = send_auth_request(request)
    if 200 <= res.status_code < 300:
        return res.json()
    elif res.status_code == 404:
        print("Book not found.")
        sys.exit(1)
    else:
        print(f"Error: ", res.status_code, res.reason, res.reason)
        sys.exit(1)

def show_plotter(args):
    plotter = get_plotter(args.book)
    dataframe = pd.DataFrame(plotter)
    print(dataframe.from_dict(plotter))

def parse_plotter(subparsers):
    parser = subparsers.add_parser("plot")
    parser.add_argument("--book", "-b", required=True, help="Book code")
    parser.set_defaults(func=show_plotter)