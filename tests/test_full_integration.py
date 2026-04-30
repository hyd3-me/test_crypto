import base64
import app.crypto as crypto
import app.utils as utils

_storage = []


def send_message(message):
    message["delivery_info"]["server_timestamp"] = utils.generate_timestamp()
    _storage.append(message)


def test_full_private_chat_cycle(shared_secret, wallet):
    bob_address = "0xBobAddressForTest"
    original_text = "Hello, Bob! This is a secret message."
    encrypted_flag = True
    nonce_b64 = None

    content_bytes = original_text.encode("utf-8")

    if encrypted_flag:
        content_bytes, nonce = crypto.encrypt_message(shared_secret, content_bytes)
        nonce_b64 = base64.b64encode(nonce).decode("ascii")
    content_b64 = base64.b64encode(content_bytes).decode("ascii")

    content_package = {
        "version": "1.0",
        "sender": wallet.address,
        "recipient": bob_address,
        "client_timestamp": utils.generate_timestamp(),
        "encrypted": encrypted_flag,
        "type": "text/plain",
        "content": content_b64,
        "nonce": nonce_b64,
    }

    delivery_info = {
        "signature": None,
        "server_timestamp": None,
    }

    message = {
        "content_package": content_package,
        "delivery_info": delivery_info,
    }

    send_message(message)

    received_message = _storage[0]
    received_cp = received_message["content_package"]
    received_di = received_message["delivery_info"]

    received_encrypted = received_cp["encrypted"]
    received_content_b64 = received_cp["content"]
    received_nonce_b64 = received_cp["nonce"]

    received_content_b64 = base64.b64decode(received_content_b64)

    if received_encrypted:
        nonce = base64.b64decode(received_nonce_b64)
        received_content_b64 = crypto.decrypt_message(
            shared_secret, received_content_b64, nonce
        )

    decrypted_text = received_content_b64.decode("utf-8")
    assert decrypted_text == original_text
