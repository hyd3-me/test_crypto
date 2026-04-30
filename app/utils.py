import secrets
import datetime
import os


def generate_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def generate_nonce() -> bytes:
    return secrets.token_bytes(12)


def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
