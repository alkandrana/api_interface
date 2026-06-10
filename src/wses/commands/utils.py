from datetime import datetime, timezone
def to_zulu(date):
    dt = datetime.fromisoformat(date)
    dtu = dt.astimezone(timezone.utc)
    return dtu.strftime('%Y-%m-%dT%H:%M:%SZ')

def to_local(date_str):
    iso = datetime.fromisoformat(date_str)
    return str(iso.astimezone())