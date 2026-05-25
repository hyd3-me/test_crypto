import app.crypto as crypto


def test_sign_payload_returns_64_bytes(ed25519_keypair_alice):
    private_key, _ = ed25519_keypair_alice
    payload = b"0" * 52
    sig = crypto.sign_payload(private_key, payload)
    assert isinstance(sig, bytes)
    assert len(sig) == 64


def test_sign_payload_deterministic(ed25519_keypair_alice):
    private_key, _ = ed25519_keypair_alice
    payload = b"1" * 52
    sig1 = crypto.sign_payload(private_key, payload)
    sig2 = crypto.sign_payload(private_key, payload)
    assert sig1 == sig2


def test_verify_payload_valid_signature(ed25519_keypair_alice):
    private_key, public_key = ed25519_keypair_alice
    payload = b"0" * 52
    sig = crypto.sign_payload(private_key, payload)
    assert crypto.verify_payload(public_key, payload, sig) is True


def test_verify_payload_invalid_signature(ed25519_keypair_alice):
    _, public_key = ed25519_keypair_alice
    payload = b"0" * 52
    bad_sig = b"\x00" * 64
    assert crypto.verify_payload(public_key, payload, bad_sig) is False
