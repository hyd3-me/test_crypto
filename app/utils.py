import secrets
import hashlib
import struct
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


def compute_content_hash(message_id: bytes, content: bytes) -> bytes:
    if not message_id:
        raise ValueError("message_id must not be empty")
    if not content:
        raise ValueError("content must not be empty")
    return hashlib.sha256(message_id + content).digest()


def build_sign_payload(
    message_id: bytes, timestamp_ms: int, content_hash: bytes
) -> bytes:
    if not message_id:
        raise ValueError("message_id must not be empty")
    if not content_hash:
        raise ValueError("content_hash must not be empty")
    return message_id + struct.pack(">Q", timestamp_ms) + content_hash
