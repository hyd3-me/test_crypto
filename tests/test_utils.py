import os
import app.utils as utils


def test_get_project_root():
    root = utils.get_project_root()
    env_path = os.path.join(root, ".env")
    assert os.path.isfile(env_path)
