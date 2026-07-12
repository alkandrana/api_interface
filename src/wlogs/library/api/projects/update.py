from .... import load_config
from ..auth import send_auth_request
import sys

from ....commands import get_project_id


def build_project_patch(payload, project_code):
    project_id = get_project_id(project_code)
    request = {
        "method": "PATCH",
        "endpoint": f"{load_config()['api_url']}/projects/{project_id}",
        "payload": payload
    }
    return request
def patch_goal(request):
    res = send_auth_request(request)
    if not 200 <= res.status_code < 300:
        print("An error occured: ", res.status_code, res.reason, res.json())
        sys.exit(1)
    else:
        print("Successfully updated goal")