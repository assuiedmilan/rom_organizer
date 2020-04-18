import mock
import pytest


@pytest.fixture()
def generator():
    with mock.patch('os.path.isfile') as is_file:
        is_file.return_value = False

