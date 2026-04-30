from app.crypto import encrypt_message, decrypt_message


def test_encrypt_decrypt_with_shared_secret(shared_secret):
    plaintext = b"Hello, Bob! This is a secret message."
    ciphertext, nonce = encrypt_message(shared_secret, plaintext)
    decrypted = decrypt_message(shared_secret, ciphertext, nonce)
    assert decrypted == plaintext
