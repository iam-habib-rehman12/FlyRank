from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._respond(200, {"message": "Hello, world!"})
        elif self.path == "/health":
            self._respond(200, {"status": "ok"})
        else:
            self._respond(404, {"error": "not found"})

    def _respond(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), APIHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()
