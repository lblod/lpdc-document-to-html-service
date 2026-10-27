import json
from datetime import datetime
from urllib.parse import quote


def sparql_escape_uri(value: str) -> str:
    escaped_value = quote(
        value,
        safe=":/?#[]@!$&'()*+,;=%",
    )
    return f"<{escaped_value}>"


def sparql_escape_datetime(value: datetime) -> str:
    timestamp = value.isoformat()
    return (
        f"{json.dumps(timestamp)}"
        "^^<http://www.w3.org/2001/XMLSchema#dateTime>"
    )


def log(message):
    print(message, flush=True)