from wses import load_config

from ..auth import send_auth_request
import os, dotenv
import sys
import requests

dotenv.load_dotenv()


def get_record_by_code(code, endpoint):
    request = {
        "method": "GET",
        "endpoint": f"{load_config()['api_url']}/{endpoint}/code/{code}",
    }
    res = send_auth_request(request)
    if 200 <= res.status_code < 300 or res.status_code == 404:
        return res
    else:
        print("An error occurred: ", res.status_code, res.reason, res.json())
        sys.exit(1)
