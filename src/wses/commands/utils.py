import os, sys, json
from pathlib import Path
from datetime import datetime, timezone
def to_zulu(date):
    dt = datetime.fromisoformat(date)
    dtu = dt.astimezone(timezone.utc)
    return dtu.strftime('%Y-%m-%dT%H:%M:%SZ')

def to_local(date_str):
    iso = datetime.fromisoformat(date_str)
    return str(iso.astimezone())

def format_dates(dates: dict[str, str]):
    valid_dates = {}
    for key, value in dates.items():
        try:
            date = datetime.fromisoformat(value)
            valid_dates[key] = date
        except ValueError:
            print(f"Date {value} is not a valid date. "
                  f"Please check your date inputs for valid ISO formatting: YYYY-MM-DD HH:MM:SS")
            sys.exit(1)
    if valid_dates['stop'] < valid_dates['start']:
        print(f"Stop date {valid_dates['stop']} cannot be earlier than start date {valid_dates['start']}")
        sys.exit(1)

