import app.constants as constants


def test_fixed_message():
    expected = "Bytestream v1: Generate messaging keys for this device."
    assert constants.FIXED_MESSAGE == expected


def test_pin_warning():
    expected = (
        "WARNING: You have set a PIN code. You must remember it to recover your keys."
    )
    assert constants.PIN_WARNING == expected
