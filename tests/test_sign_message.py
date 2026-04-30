from tests.conftest import FIXED_MESSAGE, compose_sign_message


def test_sign_message_empty_pin(sign_message):
    sig = sign_message("Test message")
    assert isinstance(sig, bytes)
    assert len(sig) == 65


def test_compose_sign_message_empty_pin():
    message = compose_sign_message(FIXED_MESSAGE, "")
    assert message == FIXED_MESSAGE


def test_compose_sign_message_with_pin():
    pin = "1234"
    message = compose_sign_message(FIXED_MESSAGE, pin)
    assert "WARNING" in message
    assert "PIN: 1234" in message


def test_sign_message_same_pin_identical(sign_message):
    message1 = compose_sign_message(FIXED_MESSAGE, "secret")
    message2 = compose_sign_message(FIXED_MESSAGE, "secret")
    sig1 = sign_message(message1)
    sig2 = sign_message(message2)
    assert sig1 == sig2
