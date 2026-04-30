from app.crypto import derive_master_key
from eth_account.messages import encode_defunct

def test_derive_master_key_deterministic(w3, wallet):
    message = f"Test message for key derivation {wallet.address}"
    message_hash = encode_defunct(text=message)
    signature1 = w3.eth.account.sign_message(message_hash, private_key=wallet.key).signature
    signature2 = w3.eth.account.sign_message(message_hash, private_key=wallet.key).signature
    assert signature1 == signature2
    key1 = derive_master_key(signature1)
    key2 = derive_master_key(signature2)
    assert key1 == key2

def test_derive_master_key_different_for_different_signature(w3, wallet):
    message1 = f"First message {wallet.address}"
    message2 = f"Second message {wallet.address}"
    hash1 = encode_defunct(text=message1)
    hash2 = encode_defunct(text=message2)
    sig1 = w3.eth.account.sign_message(hash1, private_key=wallet.key).signature
    sig2 = w3.eth.account.sign_message(hash2, private_key=wallet.key).signature
    key1 = derive_master_key(sig1)
    key2 = derive_master_key(sig2)
    assert key1 != key2
