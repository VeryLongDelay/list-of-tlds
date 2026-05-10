#!/usr/bin/env python3

from __future__ import annotations

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 3000
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)


def main() -> None:
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        url = f"http://127.0.0.1:{PORT}"

        print(f"Serving {PUBLIC_DIR}")
        print(f"Open {url}")

        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping preview server")


if __name__ == "__main__":
    main()
