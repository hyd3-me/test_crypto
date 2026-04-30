from eth_account.messages import encode_defunct

def test_sign_determinism(w3, wallet):
    message = f"SuperChat master key for address {wallet.address}"
    message_hash = encode_defunct(text=message)
    sig1 = w3.eth.account.sign_message(message_hash, private_key=wallet.key)
    sig2 = w3.eth.account.sign_message(message_hash, private_key=wallet.key)
    assert sig1.signature.hex() == sig2.signature.hex()
