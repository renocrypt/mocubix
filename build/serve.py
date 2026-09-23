#!/usr/bin/env python3
"""Preview the site: python3 build/serve.py  ->  http://127.0.0.1:8765/

Serves site/ the way GitHub Pages will (folder addresses, index.html), but
tells the browser never to cache, so a plain reload always shows the files as
they are now. A port can be given: python3 build/serve.py 8766
"""
import functools
import http.server
import pathlib
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent / 'site'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(Handler, directory=str(SITE)))
    print(f'Mocubix at http://127.0.0.1:{PORT}/  (serving {SITE})', flush=True)
    server.serve_forever()
