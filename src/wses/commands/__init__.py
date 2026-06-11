import os, sys
from .auth import send_auth_request
from dotenv import load_dotenv
load_dotenv()

asp_url = os.getenv('BASE_URL')
node_url = 'http://localhost:3000'
def get_record_id(code, endpoint):
    request = {
        "method": "GET",
        "endpoint": f"{asp_url}/{endpoint}/code/{code}",
    }
    res = send_auth_request(request)
    if res.status_code == 404:
        print("No scene with that code.")
        sys.exit(0)
    else:
        return res.json()['id']