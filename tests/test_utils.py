import os
import pytest
import app.utils as utils


def test_get_project_root():
    root = utils.get_project_root()
    env_path = os.path.join(root, ".env")
    assert os.path.isfile(env_path)


def test_compute_content_hash_deterministic():
    msg_id = b"\x00" * 12
    content = b"hello"
    h1 = utils.compute_content_hash(msg_id, content)
    h2 = utils.compute_content_hash(msg_id, content)
    assert h1 == h2
    assert isinstance(h1, bytes)


def test_compute_content_hash_different_content():
    msg_id = b"\x00" * 12
    content1 = b"hello"
    content2 = b"world"
    h1 = utils.compute_content_hash(msg_id, content1)
    h2 = utils.compute_content_hash(msg_id, content2)
    assert h1 != h2


def test_compute_content_hash_different_message_id():
    msg_id1 = b"\x00" * 12
    msg_id2 = b"\x01" * 12
    content = b"hello"
    h1 = utils.compute_content_hash(msg_id1, content)
    h2 = utils.compute_content_hash(msg_id2, content)
    assert h1 != h2


def test_compute_content_hash_length():
    msg_id = b"\x00" * 12
    content = b"anything"
    result = utils.compute_content_hash(msg_id, content)
    assert len(result) == 32


def test_compute_content_hash_empty_content_raises():
    msg_id = b"\x00" * 12
    with pytest.raises(ValueError):
        utils.compute_content_hash(msg_id, b"")


def test_compute_content_hash_empty_message_id_raises():
    content = b"hello"
    with pytest.raises(ValueError):
        utils.compute_content_hash(b"", content)


def test_compute_content_hash_ordering():
    msg_id = b"\x00" * 12
    content = b"data"
    hash1 = utils.compute_content_hash(msg_id, content)
    hash2 = utils.compute_content_hash(content, msg_id)
    assert hash1 != hash2


def test_build_sign_payload_deterministic():
    msg_id = b"\x00" * 12
    ts = 1000
    content_hash = b"\x01" * 32
    payload1 = utils.build_sign_payload(msg_id, ts, content_hash)
    payload2 = utils.build_sign_payload(msg_id, ts, content_hash)
    assert payload1 == payload2
    assert len(payload1) == 52


def test_build_sign_payload_empty_message_id_raises():
    ts = 1000
    content_hash = b"\x01" * 32
    with pytest.raises(ValueError):
        utils.build_sign_payload(b"", ts, content_hash)


def test_build_sign_payload_empty_content_hash_raises():
    msg_id = b"\x00" * 12
    ts = 1000
    with pytest.raises(ValueError):
        utils.build_sign_payload(msg_id, ts, b"")
