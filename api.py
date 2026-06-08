import os, sys, requests
from wsgiref import headers

import keyring as kr
from argparse import ArgumentParser
from typing import Any
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
base_url = os.getenv("BASE_URL")
def check_server_health():
    try:
        response = requests.get(base_url, timeout=5)
        return response.status_code < 500
        # res_dict = vars(response)
        # for key, value in res_dict.items():
        #     print(f"{key}: {value}")
    except requests.RequestException:
        return False


def send_post_request(payload, endpoint):
    response = requests.post(f"{base_url}/{endpoint}", json=payload, timeout=5)
    return response

def login():
    if not check_server_health():
        print("Server appears to be down.")
        sys.exit(1)
    payload = {"email": username, "password": password}
    response = send_post_request(payload,"login")
    if 200 <= response.status_code < 300:
        content = response.json()
        kr.set_password("wlogs", "access_token", content["accessToken"])
        kr.set_password("wlogs", "refresh_token", content["refreshToken"])
        print(f"Successfully logged in user {payload['email']}")
    elif response.status_code == 401:
        print("Username or password incorrect. Please try again.")
        sys.exit(1)
    else:
        print("An error occured: ", response.status_code, response.reason)

def refresh() -> None:
    if not check_server_health():
        print("Server appears to be down.")
        sys.exit(1)
    payload = {"refresh_token": kr.get_password("wlogs", "refresh_token")}
    response = send_post_request(payload, f"{base_url}/refresh")
    if 200 <= response.status_code < 300:
        content = response.json()
        kr.set_password("wlogs", "access_token", content["access_token"])
    elif response.status_code == 401:
        print("Refresh token expired. Logging in again...")
        login()


def check_response(response, method, payload) -> dict[str, Any] | None:
    if 200 <= response.status_code < 300:
        print("Request succeeded")
        return response.json()
    elif response.status_code == 401:
        refresh()
        response = send_verified_request(method, response.url, payload)
        if 200 <= response.status_code < 300:
            return response.json()
        else:
            print(f"An error occured: ", response.status_code, response.reason)
            sys.exit(1)
    else:
        print("An error occured: ", response.status_code, response.reason)
        sys.exit(1)

def send_verified_request(method, endpoint, payload=None):
    if not check_server_health():
        print("Server appears to be down.")
        sys.exit(1)
    access_token = kr.get_password("wlogs", "access_token")
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {access_token}"}
    if method == "POST":
        if payload:
            response = requests.post(f"{base_url}/{endpoint}", json=payload, headers=headers)
            return check_response(response, method, payload)
        else:
            print("Error: No post data submitted.")
            sys.exit(1)
    elif method == "GET":
        response = requests.get(f"{base_url}/{endpoint}", headers=headers)
        return check_response(response)
    else:
        print("Error: Method not recognized.")
        sys.exit(1)

def get_records(args):
    records = send_verified_request("GET", args.type)
    print(f"Found {len(records)} {args.type}:\n")
    for rec in records:
        for key, value in rec.items():
            if "author" not in key:
                print(f"{key}: {value}")
            elif key == "author":
                print(f"{key}: {rec[key]['userName']}")
        print("\n")
def health(_):
    print(check_server_health())
def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    health_parser = subparsers.add_parser("health")
    health_parser.set_defaults(func=health)

    get_parser = subparsers.add_parser("geta")
    get_parser.add_argument("--type")
    get_parser.set_defaults(func=get_records)
    args = parser.parse_args()
    args.func(args)
    # print(args)

if __name__ == "__main__":
    main()