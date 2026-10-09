"""Pytest fixtures: starts/stops mock server per session."""
import subprocess
import time
import sys
import os
import pytest
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.client import APIClient

MOCK_PORT = 9876
MOCK_URL = f"http://127.0.0.1:{MOCK_PORT}"

@pytest.fixture(scope="session", autouse=True)
def mock_server():
    proc = subprocess.Popen(
        [sys.executable, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mock_server", "server.py")],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # Wait for server to be ready
    for _ in range(30):
        try:
            requests.get(f"{MOCK_URL}/v1/health", timeout=1)
            break
        except requests.ConnectionError:
            time.sleep(0.2)
    else:
        proc.kill()
        raise RuntimeError("Mock server failed to start")
    yield proc
    proc.terminate()
    proc.wait(timeout=5)

@pytest.fixture
def api(mock_server):
    return APIClient(MOCK_URL)
