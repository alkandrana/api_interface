import os, sys, requests
from typing import Any

from wlogs import load_config
from wlogs.library.api.auth import send_auth_request
from dotenv import load_dotenv

from wlogs.library.api.crud import get_record_id

load_dotenv()

asp_url = os.getenv("BASE_URL")
node_url = "http://localhost:3000"

def get_project_id(project_code):
    options = get_record_id(project_code, "projects")
    project = options[0]
    return project["id"]


def send_request(request):
    if request["method"] == "POST":
        res = requests.post(request["endpoint"], json=request["payload"])
    elif request["method"] == "GET":
        res = requests.get(request["endpoint"])
    else:
        print("Request method not supported.")
        sys.exit(1)
    return res


def validate_response(res):
    if 200 <= res.status_code < 300:
        print("Request successful.")
    elif 400 <= res.status_code < 500:
        print(f"Error: {res.status_code} - {res.reason}")
        print(f"Error message: {res.json()}")
    else:
        print(f"Something went wrong. Please try again later.")



