import app.constants as constants


def test_fixed_message():
    expected = "Bytestream v1: Generate messaging keys for this device."
    assert constants.FIXED_MESSAGE == expected
