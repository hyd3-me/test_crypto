import app.utils as utils
import app.crypto as crypto


def test_full_protocol_cycle(ed25519_keypair_alice):
    private_key, public_key = ed25519_keypair_alice

    message_id = utils.generate_nonce()
    content = b"Hello, Bob!"
    timestamp_ms = utils.generate_timestamp()

    content_hash = utils.compute_content_hash(message_id, content)
    payload = utils.build_sign_payload(message_id, timestamp_ms, content_hash)

    signature = crypto.sign_payload(private_key, payload)

    assert crypto.verify_payload(public_key, payload, signature) is True

    bad_signature = b"\x00" * 64
    assert crypto.verify_payload(public_key, payload, bad_signature) is False

    altered_content = b"Hello, Eve!"
    altered_hash = utils.compute_content_hash(message_id, altered_content)
    altered_payload = utils.build_sign_payload(message_id, timestamp_ms, altered_hash)
    assert crypto.verify_payload(public_key, altered_payload, signature) is False
