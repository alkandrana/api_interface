import os, sys, requests
from typing import Any

from wses import load_config
from wses.library.api.auth import send_auth_request
from dotenv import load_dotenv

load_dotenv()

asp_url = os.getenv("BASE_URL")
node_url = "http://localhost:3000"


def get_project_id(project_code, endpoint):
    project_req = {"method": "GET", "endpoint": f"{endpoint}/{project_code}"}
    res = send_auth_request(project_req)
    if res.status_code == 404:
        print("Project does not exist.")
        sys.exit(1)
    else:
        return res.json()["id"]


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



