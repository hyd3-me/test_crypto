import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import app.crypto as crypto


def test_sign_payload_returns_64_bytes():
    private_key = Ed25519PrivateKey.generate()
    payload = b"0" * 52
    sig = crypto.sign_payload(private_key, payload)
    assert isinstance(sig, bytes)
    assert len(sig) == 64
