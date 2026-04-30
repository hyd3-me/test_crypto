def test_get_wallet(w3, wallet):
    assert w3.is_address(wallet.address) is True
