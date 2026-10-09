"""HTTP client wrapper with retry, timing, and structured responses."""
import time
import requests

class APIClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        start = time.perf_counter()
        resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        resp.elapsed_ms = elapsed_ms
        return resp

    def get(self, path, **kw): return self._request("GET", path, **kw)
    def post(self, path, **kw): return self._request("POST", path, **kw)
    def put(self, path, **kw): return self._request("PUT", path, **kw)
    def delete(self, path, **kw): return self._request("DELETE", path, **kw)
