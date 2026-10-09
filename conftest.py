# Root conftest: expose framework fixtures (mock server, api client) to all tests.
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from framework.fixtures import mock_server, api  # noqa: F401,E402