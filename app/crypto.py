import os
import json
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidSignature
import app.utils as utils

SALT = b"bytestream_salt_v1"
KEY_LENGTH = 32


def derive_master_key(signature_bytes: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=b"superchat_salt_v1",
        info=b"master_key",
    )
    return hkdf.derive(signature_bytes)


def derive_x25519_keypair(master_key: bytes):
    private_key = x25519.X25519PrivateKey.from_private_bytes(master_key)
    public_key = private_key.public_key()
    return private_key, public_key


def compute_shared_secret(private_key, peer_public_key):
    return private_key.exchange(peer_public_key)


def encrypt_message(key: bytes, plaintext: bytes):
    nonce = utils.generate_nonce()
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return ciphertext, nonce


def decrypt_message(key: bytes, ciphertext: bytes, nonce: bytes):
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)


def derive_ed25519_keypair(master_key: bytes):
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(master_key)
    public_key = private_key.public_key()
    return private_key, public_key


def verify_signature(public_key, content_package, signature_bytes):
    canonical = json.dumps(content_package, sort_keys=True, separators=(",", ":"))
    try:
        public_key.verify(signature_bytes, canonical.encode())
        return True
    except InvalidSignature:
        return False
