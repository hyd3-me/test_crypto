import secrets
import time
import os
import app.constants as constants


def generate_timestamp():
    return time.time_ns() // 1_000_000


def generate_nonce() -> bytes:
    """Return 12 random bytes for use as message_id and AES-GCM nonce."""
    return secrets.token_bytes(12)


def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def compose_sign_message(fixed_message, pin_code=""):
    if pin_code:
        return (
            f"{fixed_message}\n{constants.PIN_WARNING}\n{constants.PIN_LABEL}{pin_code}"
        )
    return fixed_message
