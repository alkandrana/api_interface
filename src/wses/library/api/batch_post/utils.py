import sys, requests, csv, os
from wses.library.api.auth import send_auth_request
from pathlib import Path


def get_records_from_file(path):
    if Path(path).exists():
        with open(path) as f:
            reader = csv.DictReader(f)
            records = [row for row in reader]
        print(f"Retrieved {len(records)} records from {path}")
        return records
    else:
        print("Could not find file.")
        sys.exit(1)


def get_records_from_api(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            print("Successfully retrieved records to post")
            return res.json()
        else:
            print("Request failed: ", res.status_code, res.reason)
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("The server appears to be down.")
        sys.exit(1)


def transfer(base, endpoint, format_records):
    records = get_records_from_api(f"{base}/{endpoint}")
    formatted = format_records(records)
    for rec in formatted:
        post_record(rec, endpoint)


def batch_from_file(path, endpoint, format_records):
    records = get_records_from_file(path)
    formatted = format_records(records)
    for rec in formatted:
        post_record(rec, endpoint)


def post_record(data, endpoint):
    request = {
        "method": "POST",
        "endpoint": f"{os.getenv('BASE_URL')}/{endpoint}",
        "payload": data,
    }
    res = send_auth_request(request)
    if res.status_code == 409:
        print("Project already added. Skipping...")
    elif 200 <= res.status_code < 300:
        print(f"Record successfully added:\n{data}\nProceeding...")
    else:
        error = res.json()
        print("An error occured: ", res.status_code, res.reason)
        print(error)
        sys.exit(1)

