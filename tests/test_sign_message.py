import pytest
from app import wallet


def test_sign_message_empty_pin():
    sig = wallet.sign_message("Test message", "")
    assert isinstance(sig, bytes)
    assert len(sig) == 65
