import json
import base64
import pytest
import app.utils as utils
import app.crypto as crypto

_storage = []
_key_storage = {}


def send_message(message):
    message["delivery_info"]["server_timestamp"] = utils.generate_timestamp()
    _storage.append(message)


def register_key(address, public_key):
    _key_storage[address] = public_key


def get_public_key(address):
    return _key_storage.get(address)


@pytest.fixture
def signed_message(ed25519_keypair_alice, wallet):
    alice_priv, alice_pub = ed25519_keypair_alice
    register_key(wallet.address, alice_pub)

    content_package = {
        "version": "1.0",
        "sender": wallet.address,
        "recipient": "0xBobAddressForTest",
        "client_timestamp": utils.generate_timestamp(),
        "encrypted": False,
        "type": "text/plain",
        "content": base64.b64encode(b"Hello, Bob!").decode("ascii"),
        "nonce": None,
    }

    canonical = json.dumps(content_package, sort_keys=True, separators=(",", ":"))
    signature = alice_priv.sign(canonical.encode())
    signature_b64 = base64.b64encode(signature).decode("ascii")

    delivery_info = {
        "signature": signature_b64,
        "server_timestamp": None,
    }

    message = {
        "content_package": content_package,
        "delivery_info": delivery_info,
    }

    send_message(message)
    return message


def test_valid_signature(signed_message):
    message = signed_message
    received_cp = message["content_package"]
    received_di = message["delivery_info"]

    alice_pub_from_server = get_public_key(received_cp["sender"])
    assert alice_pub_from_server is not None

    received_canonical = json.dumps(received_cp, sort_keys=True, separators=(",", ":"))
    received_signature = base64.b64decode(received_di["signature"])
    alice_pub_from_server.verify(received_signature, received_canonical.encode())


def test_invalid_signature(signed_message):
    message = signed_message
    received_cp = message["content_package"]
    received_di = message["delivery_info"]

    alice_pub_from_server = get_public_key(received_cp["sender"])

    tampered_cp = {**received_cp, "content": base64.b64encode(b"Bye").decode("ascii")}
    tampered_canonical = json.dumps(tampered_cp, sort_keys=True, separators=(",", ":"))

    received_signature = base64.b64decode(received_di["signature"])
    with pytest.raises(Exception):
        alice_pub_from_server.verify(received_signature, tampered_canonical.encode())


def test_verify_signature(signed_message, ed25519_keypair_alice):
    alice_priv, alice_pub = ed25519_keypair_alice
    received_cp = signed_message["content_package"]
    received_di = signed_message["delivery_info"]
    signature_bytes = base64.b64decode(received_di["signature"])

    assert crypto.verify_signature(alice_pub, received_cp, signature_bytes) is True

    tampered_cp = {**received_cp, "content": base64.b64encode(b"Bye").decode("ascii")}
    assert crypto.verify_signature(alice_pub, tampered_cp, signature_bytes) is False
