def test_sign_message_empty_pin(sign_message):
    sig = sign_message("Test message")
    assert isinstance(sig, bytes)
    assert len(sig) == 65
