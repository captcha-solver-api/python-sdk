"""
Fixtures for integration tests: a real HTTP server on localhost that records
incoming requests, so tests can check what the SDK actually sends over the wire.
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest


class _RecordingHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        self.server.requests.append(
            {
                "path": self.path,
                "headers": dict(self.headers),
                "json": json.loads(body) if body else None,
            }
        )

        response = json.dumps(self.server.response).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        pass


@pytest.fixture
def api_server(monkeypatch):
    """Local API stub. Point the client at `api_server.url`; inspect `api_server.requests`."""
    # Make sure a system proxy doesn't intercept requests to localhost.
    for var in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        monkeypatch.delenv(var, raising=False)

    server = ThreadingHTTPServer(("127.0.0.1", 0), _RecordingHandler)
    server.requests = []
    server.response = {"errorId": 0, "balance": 5.0}
    server.url = f"http://127.0.0.1:{server.server_address[1]}"

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
