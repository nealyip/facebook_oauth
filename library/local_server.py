import socketserver
import traceback
from http.server import BaseHTTPRequestHandler
from datetime import datetime as dt


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = ('query-string:%s' % (self.path[2:])).encode('utf-8')
        self.ok(body)

    def ok(self, body, *, code=200, content_type: str = 'text/html', charset: str = 'utf-8', headers=None,
           last_modified: str = None):
        body = body if isinstance(body, bytes) else body.encode(charset)
        self.send_response(code)
        if charset:
            self.send_header("Content-type", '%s; charset=%s' % (content_type, charset))
        else:
            self.send_header("Content-type", content_type)
        self.send_header("Content-Length", '{}'.format(len(body)))
        self.send_header("Cache-Control", 'public, max-age=30, must-revalidate')
        self.send_header(
            "Last-modified",
            last_modified if last_modified else dt.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        )
        if headers is not None:
            for header in headers:
                self.send_header(header[0], header[1])
        self.end_headers()
        self.wfile.write(body)

    def redirect(self, url, *, code=302, headers=None):
        self.send_response(code)
        if headers is not None:
            for header in headers:
                self.send_header(header[0], header[1])
        self.send_header("Location", url)
        self.end_headers()

    def error(self, exception: BaseException, *, code=500):
        self.send_response(code)
        print(traceback.format_exc())
        body = str(exception).encode('utf-8')
        body += '<br /><a href="/">Home</a>'.encode()
        self.send_header("Content-type", 'text/html; charset=utf-8')
        self.send_header("Content-Length", '{}'.format(len(body)))
        self.send_header("Cache-Control", 'private,no-cache,no-store,must-revalidate')
        self.end_headers()
        self.wfile.write(body)

    def log_request(self, *args, **kwargs):
        print('[%-17s] %s' % (self.__class__.__name__, self.requestline))


def serve(port, Handler):
    httpd = socketserver.ThreadingTCPServer(("", port), Handler)
    httpd.serve_forever()
