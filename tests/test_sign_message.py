def test_sign_message_empty_pin(sign_message):
    sig = sign_message("Test message")
    assert isinstance(sig, bytes)
    assert len(sig) == 65


def test_compose_sign_message_empty_pin():
    from tests.conftest import FIXED_MESSAGE, compose_sign_message

    message = compose_sign_message(FIXED_MESSAGE, "")
    assert message == FIXED_MESSAGE
