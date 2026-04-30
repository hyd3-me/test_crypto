import secrets
import datetime


def generate_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def generate_nonce() -> bytes:
    return secrets.token_bytes(12)
