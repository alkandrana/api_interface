import os, sys, requests
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

def get_status_id(status):
    status_req = {
        'method': 'GET',
        'endpoint': f'{os.getenv("BASE_URL")}/status/{status}'
    }
    res = send_auth_request(status_req)
    if res.status_code == 404:
        print("Status is not valid. Make sure it matches one of the following: pending, writing, finished, aborted.")
        sys.exit(1)
    else:
        return res.json()['id']

def get_project_id(project_code, endpoint):
    project_req = {
        'method': 'GET',
        'endpoint': f'{endpoint}/{project_code}'
    }
    res = send_auth_request(project_req)
    if res.status_code == 404:
        print("Project does not exist.")
        sys.exit(1)
    else:
        return res.json()['id']

def send_request(request):
    if request['method'] == 'POST':
        res = requests.post(request['endpoint'], json=request['payload'])
    elif request['method'] == 'GET':
        res = requests.get(request['endpoint'])
    else:
        print("Request method not supported.")
        sys.exit(1)
    return res

def validate_response(res):
    if 200 <= res.status_code < 300:
        print("Request successful.")
    elif 400 <= res.status_code < 500:
        print(f"Error: {res.status_code} - {res.reason}")
        print (f"Error message: {res.json()}")
    else:
        print(f"Something went wrong. Please try again later.")

def print_list_dict(lst):
    for item in lst:
        for key, value in item.items():
            print(f"{key}: {value}")
        print("\n")