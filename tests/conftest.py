import pytest
from web3 import Web3
from app.wallet import get_wallet
from eth_account import Account
from eth_account.messages import encode_defunct
import app.crypto as crypto

FIXED_MESSAGE = "SuperChat fixed message for Alice"


@pytest.fixture
def w3():
    return Web3()


@pytest.fixture
def wallet():
    return get_wallet()


@pytest.fixture
def sign_message(w3, wallet):
    def _sign(message):
        message_hash = encode_defunct(text=message)
        return w3.eth.account.sign_message(
            message_hash, private_key=wallet.key
        ).signature

    return _sign


@pytest.fixture
def signature_alice(w3, wallet):
    message = FIXED_MESSAGE
    message_hash = encode_defunct(text=message)
    return w3.eth.account.sign_message(message_hash, private_key=wallet.key).signature


@pytest.fixture
def signature_bob():
    return bytes.fromhex(
        "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a4708d4f5d9c2b7e5c2e5f8c5c2e5f8c5c2e5f8c5c2e5f8c5c2e5f8c5c2e5f8c5c2e5f8c5c2e5f8c5c2e5f8c5c2e5f8c5c"
    )


@pytest.fixture
def master_key_alice(signature_alice):
    return crypto.derive_master_key(signature_alice)


@pytest.fixture
def master_key_bob(signature_bob):
    return crypto.derive_master_key(signature_bob)


@pytest.fixture
def keypair_alice(master_key_alice):
    return crypto.derive_x25519_keypair(master_key_alice)


@pytest.fixture
def keypair_bob(master_key_bob):
    return crypto.derive_x25519_keypair(master_key_bob)


@pytest.fixture
def shared_secret(keypair_alice, keypair_bob):
    alice_priv, alice_pub = keypair_alice
    bob_priv, bob_pub = keypair_bob
    secret_alice = crypto.compute_shared_secret(alice_priv, bob_pub)
    return secret_alice


@pytest.fixture
def ed25519_keypair_alice(master_key_alice):
    return crypto.derive_ed25519_keypair(master_key_alice)


def compose_sign_message(fixed_message, pin_code=""):
    if pin_code:
        warning = "WARNING: You have set a PIN code. You must remember it to recover your keys."
        return f"{fixed_message}\n{warning}\nPIN: {pin_code}"
    return fixed_message
