from app.crypto import compute_shared_secret


def test_ecdh_shared_secret_from_signatures(keypair_alice, keypair_bob):
    alice_priv, alice_pub = keypair_alice
    bob_priv, bob_pub = keypair_bob
    secret_alice = compute_shared_secret(alice_priv, bob_pub)
    secret_bob = compute_shared_secret(bob_priv, alice_pub)
    assert secret_alice == secret_bob
    assert len(secret_alice) == 32
