from ..auth import send_auth_request
import os, dotenv
import sys

dotenv.load_dotenv()


def get_record_by_code(code, endpoint):
    request = {
        "method": "GET",
        "endpoint": f"{os.getenv('BASE_URL')}/{endpoint}/code/{code}",
    }
    res = send_auth_request(request)
    if 200 <= res.status_code < 300:
        return res.json()
    else:
        print("An error occurred: ", res.status_code, res.reason, res.json())
        sys.exit(1)
