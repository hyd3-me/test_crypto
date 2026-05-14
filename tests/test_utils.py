import os
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
