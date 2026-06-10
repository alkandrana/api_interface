import os, sys, dotenv, requests
import keyring as kr
dotenv.load_dotenv()
# AUTH WORKFLOW
# 1. User sends request
# 2. Attempt to load token from keyring
#       If token present
#           send_request()
#       If no token present
#           get_refresh_token()

# 3. send request
#       if response unauthorized
#           get_refresh_token()

def check_server_health():
    try:
        response = requests.get(os.getenv("BASE_URL"), timeout=5)
        return response.status_code < 500
        # res_dict = vars(response)
        # for key, value in res_dict.items():
        #     print(f"{key}: {value}")
    except requests.RequestException:
        return False
def send_auth_request(request):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    request["headers"] = headers
    content = validate_response(request)
    return content
def get_refresh_token():
    refresh_token = kr.get_password("wlogs", "refresh_token")
    if refresh_token:
        refresh(refresh_token)
    else:
        login()

def get_access_token():
    access_token = kr.get_password("wlogs", "access_token")
    if access_token:
        return access_token
    else:
        get_refresh_token()
        return kr.get_password("wlogs", "access_token")
def validate_response(request):
    print(f"Sending {request['method']} request...")
    # check server
    if not check_server_health():
        print("The server appears to be down.")
        sys.exit(1)
    # send request
    response = send_request(request)
    print("Response status: ", response.status_code)
    # if request succeeded
    if 200 <= response.status_code < 300 or response.status_code == 404:
        return response
    # if access token expired
    elif response.status_code == 401:
        print("Access token expired. Refreshing...")
        get_refresh_token()
        response = send_request(request)
        if 200 <= response.status_code < 300 or response.status_code == 404:
            return response
        else:
            print("Request failed.")
            print("An error occurred:", response.status_code, response.reason, response.url)
            sys.exit(1)
    # if request did not succeed
    else:
        print("Non-authorization error.")
        print("An error occurred:", response.status_code, response.reason)
        sys.exit(1)

def send_request(request) -> requests.Response | None:
    access_token = get_access_token()
    print("Access token retrieved.")
    request["headers"]["Authorization"] = f"Bearer {access_token}"
    if request["method"] == "POST":
        response = requests.post(request["endpoint"],
                                     json=request["payload"],
                                     headers=request["headers"])

    elif request["method"] == "GET":
        response = requests.get(request["endpoint"], headers=request["headers"])
    else:
        print("Method not recognized.")
        sys.exit(1)
    return response
def handle_missing_token():
    access_token = kr.get_password("wlogs", "access_token")
    if not access_token:
        refresh_token = kr.get_password("wlogs", "refresh_token")
        if not refresh_token:
            login()

def build_request(access_token, body, method, url):
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    request = {
        "method": method,
        "endpoint": url,
        "headers": header,
    }
    if body:
        request["payload"] = body
    return request

def login():
    # hit login endpoint
    payload = {
        "email": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    }
    response = requests.post(f"{os.getenv("BASE_URL")}/login", json=payload)
    #               if login success
    if 200 <= response.status_code < 300:
    #                   restart_request()
        auth = response.json()
        kr.set_password("wlogs", "access_token", auth["accessToken"])
        kr.set_password("wlogs", "refresh_token", auth["refreshToken"])
    #               if no login success
    else:
    #                   prompt user to check credentials/register
        print(
            "Login failed. Please check your credentials and try again. "
            f"You can also register for a new account at: {os.getenv('BASE_URL')}/register"
        )
    #                   terminate
        sys.exit(1)

def refresh(refresh_token):
        # hit refresh endpoint
        payload = {"refreshToken": refresh_token}
        response = requests.post(f"{os.getenv("BASE_URL")}/refresh", json=payload)
        #               if refresh success
        if 200 <= response.status_code < 300:
        #                   save tokens
            auth = response.json()
            kr.set_password("wlogs", "access_token", auth["accessToken"])
            kr.set_password("wlogs", "refresh_token", auth["refreshToken"])
        #                   send_request()
        #               if not refresh success
        elif response.status_code == 401:
            login()