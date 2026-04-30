import os
from dotenv import load_dotenv, set_key
from eth_account import Account

Account.enable_unaudited_hdwallet_features()

ENV_FILE = os.path.join(os.path.dirname(__file__), "..", ".env")


def _save_private_key(private_key_hex):
    set_key(
        dotenv_path=ENV_FILE,
        key_to_set="WEB3_PRIVATE_KEY",
        value_to_set=private_key_hex,
    )
    os.environ["WEB3_PRIVATE_KEY"] = private_key_hex


def _load_private_key():
    load_dotenv(dotenv_path=ENV_FILE)
    return os.environ.get("WEB3_PRIVATE_KEY")


def _create_new_wallet():
    account = Account.create()
    _save_private_key(account.key.hex())
    return account


def _restore_wallet_from_key(private_key_hex):
    return Account.from_key(private_key_hex)


def get_wallet():
    private_key = _load_private_key()
    if private_key is None:
        return _create_new_wallet()
    else:
        return _restore_wallet_from_key(private_key)
