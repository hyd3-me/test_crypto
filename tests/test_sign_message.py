import app.constants as constants
import app.utils as utils


def test_sign_message_empty_pin(sign_message):
    sig = sign_message("Test message")
    assert isinstance(sig, bytes)
    assert len(sig) == 65


def test_compose_sign_message_empty_pin():
    message = utils.compose_sign_message(constants.FIXED_MESSAGE, "")
    assert message == constants.FIXED_MESSAGE


def test_compose_sign_message_with_pin():
    pin = "1234"
    message = utils.compose_sign_message(constants.FIXED_MESSAGE, pin)
    assert "WARNING" in message
    assert "PIN: 1234" in message


def test_sign_message_same_pin_identical(sign_message):
    message1 = utils.compose_sign_message(constants.FIXED_MESSAGE, "secret")
    message2 = utils.compose_sign_message(constants.FIXED_MESSAGE, "secret")
    sig1 = sign_message(message1)
    sig2 = sign_message(message2)
    assert sig1 == sig2


def test_sign_message_different_pin_different(sign_message):
    msg1 = utils.compose_sign_message(constants.FIXED_MESSAGE, "1111")
    msg2 = utils.compose_sign_message(constants.FIXED_MESSAGE, "2222")
    sig1 = sign_message(msg1)
    sig2 = sign_message(msg2)
    assert sig1 != sig2
